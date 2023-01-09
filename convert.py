import sqlite3, sys, os, shutil, re, codecs
import datetime
import markdownify

def cmdhelp():
    print("\nUse python3 convert.py [path to exported joplin profile]\n")
    sys.exit(1)
    
def  chkpath(p):
    if not (os.path.exists(p)):
       print("\nThe path " + str(p) + " does not exist.")
       cmdhelp()

def makepath(p):
    try: 
        os.mkdir(p)
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

def main():

    if (len(sys.argv)==1) or (len(sys.argv)>2):
            cmdhelp()
    chkpath(sys.argv[1]) 

    path=sys.argv[1]
    pathres=os.path.join(path,'resources')
    dbpath=os.path.join(path,'joplin.sqlite')
    expath=os.path.join(path,'Obsidian')
    respath=os.path.join(expath,'resources')
    
    chkpath(dbpath)
    chkpath(pathres)

    try:
        con = sqlite3.connect(os.path.join(path,'joplin.sqlite'))
        cur = con.cursor()
    except OSError as error:
        print(error)
        sys.exit(1)

    makepath(expath)
    makepath(respath)

    folders = {}
    for row in cur.execute('SELECT id,title FROM folders'):
        folders[row[0]] = repl_forb(row[1])
        makepath(os.path.join(expath,folders[row[0]]))

    print("Exporting to :" + expath + "\n\nNotebook\tNote\n")
    meta=""
    fol=""
    for row in cur.execute('SELECT title,body,parent_id,id,source_url,created_time,source FROM notes'):
        if row[2] in folders:
                fol=folders[row[2]]
        else:
            fol=""
        print(fol + "\t" +  row[0])
        filetmp=markdownify.markdownify(row[1], heading_style="ATX").replace("](:/","](").replace("\\*","*").replace("\\_","_")
        for line in re.findall("\!\[.*\]\(.*\)", filetmp):
          jop_res=re.sub('^\:\/', '', line.split("(")[1::2][0].split(")")[0]).split(" ")[0]
          #print("att: "+jop_res)
          if jop_res[0:4]!="http":
              #print("Downloading an attachement:\r\n"+t+"\r\n")
             # t=Download(t,True,pathres+'/')
              try:
                  f_list=findfiles(jop_res, pathres) 
                  if (len(f_list) > 0):
                      obs_res=os.path.basename(f_list[0])
                    #  print("file: " +obs_res)
                      shutil.copyfile(os.path.join(pathres,obs_res),os.path.join(respath,obs_res))
                      filetmp=re.sub("\("+jop_res+"\)", "("+obs_res+")", filetmp) 
                      filetmp=re.sub("\("+jop_res+" ", "("+obs_res+" ", filetmp) 
                  else:
                      print("Warning: Attachement "+jop_res+" in note \'"+row[0]+"\' not found in "+pathres)


              except OSError as error:
                print(error)

          date_t= datetime.datetime.fromtimestamp(row[5] // 1000).strftime("%m/%d/%Y, %H:%M:%S")
          meta="\r\n***\r\nNote id: "+row[3]+"\r\nUrl: "+row[4]+"\r\nCreated time (db, local): "+date_t+"\r\nSource app: "+row[6]
        note_file=codecs.open(os.path.join(expath, fol, repl_forb(row[0]) + ".md"), "w", "utf-8")   

        note_file.write(filetmp)
        note_file.write(meta)
        note_file.close()
    con.close()




if __name__ == "__main__":
        main()

