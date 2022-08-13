import sqlite3, re, sys, os, shutil

def cmdhelp():
    print("\nUse python3 convert.py [path to exported joplin profile]\n")
    sys.exit(1)

def main():

    if (len(sys.argv)==1) or  not os.path.exists(sys.argv[1]):    
            print("\nThe path  does not exist.")
            cmdhelp()

    path=sys.argv[1]
    pathres=os.path.join(path,'resources')
    expath=os.path.join(path,'Obsidian')
    respath=os.path.join(expath,'resources')



    def __find(filename, search_path):
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
        print(error)  
        sys.exit(1)

    for row in cur.execute('SELECT title,body FROM notes'):
        
        print("Exporting: "+ row[0])
        filetmp=row[1]
        for line in re.findall("!\[.*\]\(.*\)", filetmp):
          
          t=line.split('(')[1::2][0].split(')')[0].replace(":/","")
          shutil.copyfile(__find(t, pathres)[0],os.path.join(respath,os.path.basename(__find(t, pathres)[0])))
          t='![['+__find(t, pathres)[0].split("/")[-1]+']]'
          filetmp=re.sub(line.replace("!","\!").replace("[","\[").replace("]","\]").replace(")","\)").replace("(","\("),t,filetmp)
      
        note_file=open(os.path.join(expath , row[0] + ".md"),'w')           
        note_file.write(filetmp) 
        note_file.close()
    con.close()




if __name__ == "__main__":
        main()

