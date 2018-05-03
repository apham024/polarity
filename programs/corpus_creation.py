import os
import sys

##############################################################################################################
debug_files = dict()
def valid(filename):
    try:
        open(filename);
    except IOError:
        print("Invalid file");
        exit();

##############################################################################################################
def sortHeaders(filename):
    dir_name = filename[:len(filename)-4]
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    valid(filename);
    file = open(filename,"r")
    lines = file.readlines();
    i = 0;
    os.chdir(dir_name)
    file.close()
    file_outn = createName(dir_name,0)
    #file_out = open(file_outn,'w')
    while True:                                                                 #LOOP THROUGH ENTIRE FILE LINE BY LINE
        if len(lines) <= i:
            break;
        if lines[i].find("DOCUMENTS") != -1:                                    #FIND START OF HEADER
            line_formatted = lines[i].strip('\n').strip()
            #for char in lines[i]:
            if len(line_formatted) >=17 and len(line_formatted) <=21 and line_formatted.find(" of ") !=-1:
                while True:
                    #file_out.write(lines[i])
                    lines[i] =  0;
                    i+=1;
                    if lines[i].find("LENGTH: ") !=-1 and lines[i].find("words") != -1:
                        #file_out.write(lines[i])
                        lines[i] = 0;
                        break;
        i+=1;
    os.chdir('..')
    #file_out.close()
    return lines

##############################################################################################################
def subtractStr(stro,strs):
    i = stro.find(strs)
    if(i == -1):
        print("invalid")
        return;
    return stro[0:i]+stro[i+len(strs):]

##############################################################################################################
def insertStr(stro,strs,pos):
    if(pos>=0 and pos<len(stro)):
        return stro[0:pos+1]+strs+stro[pos+1:]
    else:
        print("invalid")
        return
debug_files = dict()

##############################################################################################################
def debug(filename,str):
    if(filename not in debug_files.keys()):
        debug_files[filename] = 0
        if os.path.isfile(filename):
            os.remove(filename)
    open(filename,"a").write(str)
    return

##############################################################################################################
def debug_paren(dic,insert):
    if(insert in dic.keys()):
        dic[insert]+=1
    else:
        dic[insert] = 0

##############################################################################################################
def removeNL(str_handle):
    return str_handle.replace("\n","").replace("\r","")

##############################################################################################################
def removeSpaces(str_handle):
    while(str_handle.find(" ")!=-1):
        str_handle = subtractStr(str_handle," ")
    return str_handle

##############################################################################################################        
def flagSpeakers(filename):
    file_handle  = open(filename,'r')
    text = file_handle.readlines()
    
    file_out = open(filename,"w")
    for line in text:
        if(line.find("(")!=-1 and line.find(")")!=-1 
        and line.find(")") >= len(line)-3 or line.find("ANNOUNCER")!=-1):
            file_out.write(removeNL(line+":")+"\n")
        else:
            count = 0
            for char in line:
                if(ord(char)>=65 and ord(char)<=90):
                    count+=1
            if(count<=12):
                file_out.write(line)
    file_out.close()

##############################################################################################################
def isFirst(str):
    return True if str.find(":")!=-1 and str.find(".")!=-1 and str.find(".")>str.find(":") else False

##############################################################################################################
def clean(filename,lines,mode):
    i = 0
    file_out = open(filename,'w')
    #remove extra unecessary info and separate each document
    while True:
        if len(lines) <= i:
            break;
        if lines[i] !=0 and lines[i-1]== 0:
            while True:
                if len(lines) <= i:
                    break;
                if lines[i].find("LOAD-DATE:")!=-1:
                    while True:
                        if len(lines) <= i:
                            break;
                        if lines[i]!=0:
                            lines[i] = 0;
                            i+=1
                        else:
                            break
                if len(lines) <= i:
                        break;
                if lines[i] !=0:
                    file_out.write(lines[i])
                    i+=1
                else:
                    file_out.write("############################################")
                    break
        i+=1
        #deep clean tuned to each individual file
    i = 0
    file_out.close()
    #special run to get speakers for abc
    if(mode == "ABC"):
        flagSpeakers(filename)
    lines_mod = open(filename,'r').readlines()
    file_final = open(filename,'w')
    #remove (example)
    #stage_instructions = dict()
    error = 0

    while True:
        if len(lines_mod)<=i:
            break;
        str_handle = lines_mod[i]
        while(True):
            if len(lines_mod)<=i:
                break;
            if(str_handle.find("(")!=-1 and str_handle.find(")")!=-1 and error<=10):
                #debug_paren(stage_instructions,str_handle[str_handle.find("("):str_handle.find(")")+1]) ############
                #debug("()",str_handle[str_handle.find("("):str_handle.find(")")+1]+"\n")
                off_b = 1 if str_handle.find(")")<len(str_handle) and str_handle[str_handle.find(")")+1] == " " else 0
                off_f = 1 if str_handle.find("(")>0 and str_handle[str_handle.find("(")-1] == " " else 0
                #print(off_f)
                str_handle = subtractStr(str_handle,str_handle[str_handle.find("(")-off_f:str_handle.find(")")+1+off_b])
                error+=1
            elif(str_handle.find("[")!=-1 and str_handle.find("]")!=-1 and error<=10):
                str_handle = subtractStr(str_handle,str_handle[str_handle.find("["):str_handle.find("]")+1])
                error+=1
            elif(error>10):
                error = 0
                print("ERROR AT #%d. "%i+str_handle+"\n")
                i+=1
                break;
            elif(str_handle != lines_mod[i]):
                error = 0
                file_final.write(str_handle)
                i+=1
                break;
            elif lines_mod[i] !=0:
                error = 0
                file_final.write(lines_mod[i])
                i+=1
                break;
            else:
                error = 0
                i+=1
                break
    
    i = 0
    file_final.close()
    lines_mod = open(filename,'r').readlines()
    
    #Marks Speakers
    while(True):
        temp = 0
        if(i>=len(lines_mod)):
            break
        colonpos = lines_mod[i].find(":")
        speakerVar = isSpeaker(lines_mod[i])
        if(speakerVar == 1):
            lines_mod[i] = "#!#"+lines_mod[i]
        elif(isSpeaker(lines_mod[i])==2):
            j=colonpos-1
            while(True):
                if(j<=0):
                    break
                elif(ord(lines_mod[i][j])>90 or ord(lines_mod[i][j])>=48 and ord(lines_mod[i][j])<=57):
                    temp = j
                    break
                else:
                    j-=1
        if(colonpos-temp>5 and temp>0):
            #split into 2 lines
            templine = "#-1"+lines_mod[i][temp+1:]
            lines_mod[i] = lines_mod[i][0:temp+1]
            lines_mod[i+1] = templine+ lines_mod[i+1]
            i+=1   
        i+=1
    #shorten to 1 line per person
    #os.remove("@12d1233c56")
    oneline(lines_mod,filename)

############################################################################################################## 
def oneline(line_handle,filename):
    file_final = open(filename,'w')
    i = 0
    while(True):
        if(i>=len(line_handle)):
            break
        sentence = line_handle[i]
        if(sentence.find("############################################")!=-1):
            #tp = sentence.find("############################################")
            file_final.write("\n"+sentence)
        elif(sentence.find("#-1")==-1 and sentence.find("#!#")==-1): #is not a speaker
            file_final.write(" "+removeNL(sentence)+" ")
        elif(sentence.find("#-1")!=-1 or sentence.find("#!#")!=-1):
            file_final.write("\n"+removeNL(sentence[3:]))
        i+=1
    #print(line_handle)        
            
    file_final.close()
           
##############################################################################################################
def isSpeaker(line):
    colonpos = line.find(":")
    if(basicSpeaker(line)):
        return 1
    elif(hasCaps(line,colonpos)):
        temp = line
        temp = removeSpaces(temp)
        colontemp = temp.find(":")
        j = colontemp-1
        cnt = 0
        while(True):
            if(colontemp==-1):
                break
            if(j<=0):
                break
            elif(ord(temp[j])>90):
                break;
            else:
                j-=1
                cnt+=1
        if(cnt>=4):
            return 2
        else:
            return 0
    else:
        return 0

##############################################################################################################
def basicSpeaker(line):
    temp = line
    temp = removeSpaces(temp)
    colonpos = temp.find(":")
    i = 0
    if colonpos== -1:
        return False
    while(True):
        if(i>=colonpos):
            return True
        elif(ord(temp[i])>=97):
            return False
        else:
            i+=1

##############################################################################################################
def hasCaps(line,colonpos):
    i = colonpos
    temp = 0
    if(colonpos!=-1):
        while(True):
            if(i<=0):
                break
            if(ord(line[i])>=65 and ord(line[i])<=90):
                temp+=1
            i-=1
    if(temp>=4):
        return True
    else:
        return False

##############################################################################################################
def hasPeriod(line,colonpos):
    if(line.find(".")!=-1 and line.find(".")<colonpos-1):
        return True
    else:
        return False

##############################################################################################################
def createName(name,offset):
    i=0
    num_str = list()
    for char in name:
        num_str.append(char)
        i+=1
    num_str.append('_')
    num_str.append('')
    num_str.append('')
    num_str.append('')
    cnt = 3
    while True:
        cnt-=1;
        if cnt<0:
            break;
        temp = offset%10
        num_str[len(name)+cnt+1] = chr(temp+48)
        offset /=10;
    return ''.join(num_str)

# ##############################################################################################################
def split(name, output_name, name_lines):
    output_name = output_name
    dir_name = name[:len(name)-4]

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    i = 0
    offset = 1;
    file_name = createName(dir_name,1)

    file_in = open(name_lines)                                                     #name_lines is the file name for cleaned lines
    cleaned_lines = file_in.readlines()
    os.chdir(dir_name)
    file_out = open(file_name,'w')
    while True:
        if len(cleaned_lines) <= i:
            os.chdir('..')
            return;
        if cleaned_lines[i].find("############################################") != -1:
            offset+=1;
            file_name = createName(dir_name,offset)
            file_out = open(file_name,'w')
        elif(cleaned_lines[i]!="\n"):
            file_out.write(cleaned_lines[i])
        i+=1
    os.chdir('..')

##############################################################################################################
def main():
    #lists = sortHeaders("test2.txt")
    #clean("cleaned",lists,"CNN")
    #split("test2.txt","cleaned")
    ### Checks for correct number of input argument
    if(len(sys.argv)!=3):
        print("improper number of arguments")
        sys.exit()
    elif(sys.argv[1]=="-h"):
        print("enter directory/file after program name and an output directory name/path")
        sys.exit()

    #### Deals with processing a single file
    if(os.path.isfile(sys.argv[1])):
        try:
            open(sys.argv[1],"r")
        except OSError or IOError:
            print("invalid argument")
            sys.exit(0)
        lists = sortHeaders(sys.argv[1])
        print("News Program: "+sys.argv[1][0:3])
        clean("temp",lists,sys.argv[1][0:3])
        split(sys.argv[1],sys.argv[2],"temp")
        os.remove("temp")
        sys.exit()

    ### Deals with procsssing a directory of files
    else:
        try:
            dir = os.listdir(sys.argv[1])
        except OSError or IOError:
            print("invalid argument")
            sys.exit()
        os.chdir(sys.argv[1])
        counter = 0
        for filename in dir:
            if ((filename != ".DS_Store") and (filename != "Icon^M")):

                flag = 1
                try:
                    open(filename,"r")
                except OSError:
                    print(filename+" is invalid")
                    flag = 0
                if(flag==1):
                    
                    lists = sortHeaders(filename)
                    print("File Number: "+str(counter)+"\tNews Program: "+filename[0:3])
                    clean("temp",lists,filename[0:3])
                    split(filename,sys.argv[2],"temp")
                    os.remove("temp")
                    counter +=1
        os.chdir('..')
            
##############################################################################################################

main()
