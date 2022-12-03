import sqlite3, sys, os, shutil, re, codecs

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
  forbidden_char={'<': '(less than)',
                 '>': '(greater than)',
                 ':': '(colon)',
                 '"': '(double quote)',
                 '/': '(forward slash)',
                 '\\': '(backslash)',
                 '|': '(vertical bar or pipe)',
                 '?': '(question mark)',
                 '*': '(asterisk)'
                 }


  for   rep in forbidden_char:
                 string=string.replace(rep,forbidden_char[rep])
  return string



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

    def findfiles(filename, search_path):
       result = []

       for root, dir, files in os.walk(search_path):
           for f in files:
               if  filename in f:
                 result.append(os.path.join(root, f))
       return result


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
    for row in cur.execute('SELECT title,body,parent_id FROM notes'):
        print(folders[row[2]] + "\t" +  row[0])
        filetmp=row[1]
        for line in re.findall("!\[.*\]\(.*\)", filetmp):
          
          t=line.split("(")[1::2][0].split(")")[0].replace(":/","")
          shutil.copyfile(findfiles(t, pathres)[0],os.path.join(respath,os.path.basename(findfiles(t, pathres)[0])))
          t='![['+os.path.basename(findfiles(t, pathres)[0])+']]'
          filetmp=re.sub(line.replace("!","\!").replace("[","\[").replace("]","\]").replace(")","\)").replace("(","\("),t,filetmp)
      
        note_file=codecs.open(os.path.join(expath, folders[row[2]], repl_forb(row[0]) + ".md"), "w", "utf-8")           
        note_file.write(filetmp) 
        note_file.close()
    con.close()




if __name__ == "__main__":
        main()

