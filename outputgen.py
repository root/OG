import subprocess,os,sys,stat
from globalvar import *
# coding=utf8


def getdata(number):
    datastream = ""
    f = open(problempath+"/file/"+str(number)+".in","r")
    for line in f:
        datastream += line
    f.close()
    return datastream

def get_dir_and_file(path,id):
    exe = list()
    p = str( path )
    if p=="":
        return [ ]
#    p = p.replace( "/","\\")
    if p[-1] != "/":
        p = p+"/"
#    print(p)
    dic = os.listdir( p )  # list file in this path(dir)
    for d in dic:
        if d == str(id) and os.path.isdir( p + d ):
            #print(p + d)
            file = os.listdir( p + d )
            p = p + d + "/"
            for f in file :
                if os.path.isfile( p + f ): # check is file or not
                    # spilt filename and file extenion
                    fname , fext = os.path.splitext(f)
                    if fext == ".exe":
                        exe.append( p + f )
                    if fext == ".class":
                        exe.append( fname )
    return exe

def check_output(ofile,pid):
    Max = 0
    tmplist = list()
#    output = ""
    for k in ofile.keys():
#        print("key:",k,"value:",ofile[k])
        tmplist.append(k)
    tmplist.sort()
    while tmplist:
        if ofile[tmplist[0]] > Max :
            output = tmplist[0]
            Max = ofile[tmplist[0]]
        tmplist.pop(0)  #del the first item
    del tmplist
    print(output)

def main(a):
    ofile = dict()
    data = getdata(a[1])
#    print(data)
    exe = get_dir_and_file(problempath+"/DB/",a[1])
    exe.sort()
    for e in exe:
        ename , eext = os.path.splitext(e)
############################### process on ################################
        if eext == ".exe":
            p = subprocess.Popen(e, stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        else:
            javafile = open(shellpath+"exejava.sh","w")
            javafile.write(cmdproglue)
            javafile.write("cd "+problempath+"/DB/"+a[1]+"\n")
            javafile.write("java "+ e + "\n")
            javafile.close()
            p = subprocess.Popen(["sh",shellpath+"exejava.sh"], stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
####################### process end and get output ########################
#############    p.communicate return (stdout , stderr)   #################
        try:
            std = p.communicate(input = data.encode('utf-8') ,timeout = 10)
            o =std[0].decode('utf-8','ignore')
            if o in ofile:
                ofile[o] += 1
            else :
                ofile[o] = 1
            #p.terminate()
        except:
            p.kill() 
    check_output(ofile,a[1])
#    print(ofile)
    del ofile
    del exe

if __name__ == "__main__":
    main(sys.argv)

