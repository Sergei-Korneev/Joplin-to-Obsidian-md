import sqlite3, sys, os, shutil, re, codecs

def cmdhelp():
    print("\nUse python3 convert.py [path to exported joplin profile]\n")
    sys.exit(1)
    
def  chkpath(p):
    if not (os.path.exists(p)):
       print("\nThe path " + str(p) + " does not exist.")
       cmdhelp()

def main():

    if (len(sys.argv)==1):            
            cmdhelp()
    chkpath(sys.argv[1]) 

    path=sys.argv[1]
    pathres=os.path.join(path,'resources')
    dbpath=os.path.join(path,'joplin.sqlite')
    expath=os.path.join(path,'Obsidian')
    respath=os.path.join(expath,'resources')
    
    chkpath(pathres)
    chkpath(dbpath)

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

    try: 
        os.mkdir(expath)
        os.mkdir(respath)
    except OSError as error:
        if error.errno != 17:
          print(error)  
          sys.exit(1)

    for row in cur.execute('SELECT title,body FROM notes'):
        
        print("Exporting: "+ row[0])
        filetmp=row[1]
        for line in re.findall("!\[.*\]\(.*\)", filetmp):
          
          t=line.split("(")[1::2][0].split(")")[0].replace(":/","")
          shutil.copyfile(findfiles(t, pathres)[0],os.path.join(respath,os.path.basename(findfiles(t, pathres)[0])))
          t='![['+os.path.basename(findfiles(t, pathres)[0])+']]'
          filetmp=re.sub(line.replace("!","\!").replace("[","\[").replace("]","\]").replace(")","\)").replace("(","\("),t,filetmp)
      
        note_file=codecs.open(os.path.join(expath , row[0] + ".md"),"w","utf-8")           
        note_file.write(filetmp) 
        note_file.close()
    con.close()




if __name__ == "__main__":
        main()

