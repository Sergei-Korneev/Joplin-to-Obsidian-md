import sqlite3, sys, os, shutil, re, codecs
import datetime
import markdownify
import functools
import random


def cmdhelp():
    print("\nUse python3 convert.py [path to exported joplin profile]\n")
    sys.exit(1)
    
def  chkpath(p):
    if not (os.path.exists(p)):
       print("\nThe path " + str(p) + " does not exist.")
       cmdhelp()

def makepath(p):
    try: 
        os.makedirs(p, exist_ok=True)
    except OSError as error:
        if error.errno != 17:
          print(error)  
          sys.exit(1)

# Replace Windows/Linux filesystem reserved symbols
def repl_forb(string):
  forbidden_char={'<': '\u2770',
                 '>': '\u2771',
                 ':': '\u003a',
                 '"': '\u275d',
                 '/': '\u27cb',
                 '\\': '\u27cd',
                 '|': '\u2758',
                 '#': '\u27da',
                 '?': '\u2754',
                 '*': '\u2731'
                 }


  for   rep in forbidden_char:
                 string=string.replace(rep,forbidden_char[rep])
  if len(string) > 250:
      string=string[0:240]+"~"

  return string


def findfiles(filename, search_path):
       result = []

       for root, dir, files in os.walk(search_path):
           for f in files:
               if  filename in f:
                 result.append(os.path.join(root, f))
       return result

def getDirs(parent,cur):
        path = []
        while  parent:

            for  res in  cur.execute('SELECT title,parent_id FROM folders WHERE id = \"' + parent+'\"'):

                title=repl_forb(res[0])
                parent=res[1]
                path.append(title) 
        return functools.reduce(os.path.join,list(reversed(path)))

def main():

    if (len(sys.argv)==1) or (len(sys.argv)>2):
            cmdhelp()
    chkpath(sys.argv[1]) 

    path=sys.argv[1]
    pathres=os.path.join(path,'resources')
    dbpathm=os.path.join(path,'joplin.sqlite')
    dbpathd=os.path.join(path,'database.sqlite')
    expath=os.path.join(path,'Obsidian')
    respath=os.path.join(expath,'resources')
    dbpath=""
    if  (os.path.exists(dbpathm)):
        dbpath=dbpathm
    elif  (os.path.exists(dbpathd)):
        dbpath=dbpathd
    else:
        print("No db file [mobile or desktop] found in "+path+"\r\n")
        exit(1)

    chkpath(pathres)

    try:
        con = sqlite3.connect(dbpath)
        cur = con.cursor()
        cur2 = con.cursor()
    except OSError as error:
        print(error)
        sys.exit(1)

    makepath(expath)
    makepath(respath)
    
    print("Exporting to: " + expath )
    meta=""
    fol=""

    cur1 = cur.execute('SELECT title,body,parent_id,id,source_url,created_time,source FROM notes')
    for row in cur1:
    
        fol = os.path.join(expath,getDirs(row[2],cur2))
        makepath(fol)

        print ("----\r\nFolder: "+fol+"\r\n")
        print("Note: \'" +  row[0]+"\'" )
        filetmp=markdownify.markdownify(row[1], heading_style="ATX").replace("](:/","](").replace("\\*","*").replace("\\_","_")
        for line in re.findall("(\!\[.+?\]\(.+?\)|\!\[.*\]\(.*\))", filetmp):
          jop_res=re.sub('^\:\/', '', line.split("(")[1::2][0].split(")")[0]).split(" ")[0]
          #print("att: "+jop_res)
          if jop_res[0:4]!="http":
              try:
                  f_list=findfiles(jop_res, pathres)
                  if (len(f_list) > 0):
                      obs_res=os.path.basename(f_list[0])
                    #  print("file: " +obs_res)
                      shutil.copyfile(os.path.join(pathres,obs_res),os.path.join(respath,obs_res))
                      filetmp=re.sub("\("+jop_res+"\)", "("+obs_res+")", filetmp) 
                      filetmp=re.sub("\("+jop_res+" ", "("+obs_res+" ", filetmp) 
                  else:
                      print("Warning: Attachement "+jop_res+", note: \'"+row[0]+"\' not found in: "+pathres)


              except OSError as error:
                print(error)

          date_t= datetime.datetime.fromtimestamp(row[5] // 1000).strftime("%m/%d/%Y, %H:%M:%S")
          meta="\r\n***\r\nNote id: "+row[3]+"\r\nUrl: "+row[4]+"\r\nCreated time (db, local): "+date_t+"\r\nSource app: "+row[6]
       
        ind = 0
        n_path = os.path.join(fol, repl_forb(row[0]) + ".md")
        while (os.path.exists(n_path)):
            ind=ind+1
            n_path = os.path.join(fol, repl_forb(row[0]) + "("+str(ind)+")" + ".md")

        note_file=codecs.open(n_path, "w", "utf-8")   

        note_file.write(filetmp)
        note_file.write(meta)
        note_file.close()
    con.close()
    print("\r\n-----Finished!------")




if __name__ == "__main__":
        main()

