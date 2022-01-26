import sqlite3, re, sys, os, shutil



if (len(sys.argv)==1) or  not os.path.exists(sys.argv[1]):    
        __help()
        print("\nThe path  does not exist.")
        sys.exit(1)


path=sys.argv[1]
expath=path+'/Obsidian/'
respath=expath+'/resources/'



def __find(filename, search_path):
   result = []

   for root, dir, files in os.walk(search_path):
       for f in files:
           if  filename in f:
             result.append(os.path.join(root, f))
   return result


try:
    con = sqlite3.connect(path+'/joplin.sqlite')
    cur = con.cursor()
except OSError as error:
    print(error)


try: 
    os.mkdir(expath)
    os.mkdir(respath)
except OSError as error: 
    print(error)  


for row in cur.execute('SELECT title,body FROM notes'):
    
    print("Exporting: "+ row[0])
    filetmp=row[1]
    for line in re.findall("!\[.*\]\(.*\)", filetmp):
      
      t=line.split('(')[1::2][0].split(')')[0].replace(":/","")
      shutil.copyfile(__find(t, path+'/resources')[0],respath+__find(t, path+'/resources')[0].split("/")[-1])
      t='![['+__find(t, path+'/resources')[0].split("/")[-1]+']]'
      #print(t)
      filetmp=re.sub(line.replace("!","\!").replace("[","\[").replace("]","\]").replace(")","\)").replace("(","\("),t,filetmp)
  
    note_file=open(expath + row[0] + ".md",'w')           
    note_file.write(filetmp) 
    note_file.close()
con.close()
