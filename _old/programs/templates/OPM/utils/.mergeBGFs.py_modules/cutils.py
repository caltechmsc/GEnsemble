#!/exec/python/python-2.4.2/bin/python
"""
cutils.py
Aug 12 2004 -(c)- caglar tanrikulu

Module with general utilities for python scripting

 040812 # cutils module created.
 041012 # no log availble until this date.
 041013 # created the deltree() and printout() functions.
 041014 # printError() flushes stdout before writing to stderr.
          renamed lineIsInLines and lineIsInFile to reIsInLines
           and reIsInFile, respectively.
 041025 # added delAll()
 041116 # added readInList()
 050118 # added derefSymLink()
 050126 # added waitForFile()
 050817 # added getSysInfo()
 050824 # added assertPath()22
 050826 # added addLinesToFile()
 050829 # added addLineToFile()
 050830 # added writeLineToFile()
 071104 # reIsInLines option returnLineNos added
 071119 # added runViaPBS()
 071218 # added initDict()
"""

import sys, os, string, types, time, re, shutil

version = '071218'


#
# - output:
#

def printHeader(programName, creationDate, version):
    """
printHeader(programName, creationDate, version):
    prints header & version
    """
    version      = "ver: " + version    
    print string.join( ["\n caglar tanrikulu", \
                        programName,           \
                        creationDate,          \
                        version] , ' # ')
    sys.stdout.flush()
    # return


def doI(text,var):
    """
doI(text,var):
    prints (text+' Yes/No') depending on whether var is true
    """
    if var:
        print text,'Yes'
    else:
        print text,'No'
    # done
    

def printError(message, die=0):
    """
printError(message, die=0):
    prints error message, exits run if (die != 0)
    """
    if die:
        type = 'ERROR'
    else:
        type = 'WARNING'
        
    error = os.path.basename(sys.argv[0]) + ': ' + type + ': ' + message + '\n'
    # flush stdout:
    sys.stdout.flush()
    # print error
    sys.stderr.write(error)

    if die:  sys.exit(2)
    # done


def die(message):
    """
die(message):
    same as  printError(message, 1)
    """
    printError(message, 1)

    
def warn(message):
    """
warn(message):
    same as  printError(message, 0)
    """
    printError(message, 0)


def printout(*items):
    """
printout(*items):
    writes `items` to STDOUT and flushes it
    """
    sys.stdout.write( list2str(items) )
    sys.stdout.flush()




#
# - type conversion
#

def list2str(List, sep=' '):
    """
list2str(List, sep=' '):
    takes in a list and returns it as a string with separators inserted
    """
    outList = []
    # convert elements to string:
    for i in range(len(List)):
        outList.append( str(List[i]) )

    # return:
    return string.join(outList, sep)


def list2intList(List):
    """
list2intList(List):
    takes in a list and converts its elements to integers
    """
    for i in range(len(List)):  
        List[i] = int(List[i])   # convert elements to integers

    # return:
    return List


def list2floatList(List):
    """
list2floatList(List):
    takes in a list and converts its elements to floats
    """
    for i in range(len(List)):
        List[i] = float(List[i])  # convert elements to floats

    # return:
    return List



#
# - system commands
#

def execCmd(command, outputTo=''):    # longer 'execute' function
    """
execCmd(command, outputTo=''):
    executes a system call submitted as a list,
    * directs the output:
      - into a file (if outputTo=='file'),
      - to stdout (if outputTo==''), or
      - into the list ''output'' (if outputTo=='return')
    * also, calculates elapsed time if specified (etime!=0)

    returns: (elapsed-time, output/success, commandLine)
    where output/success is a list containing output lines if (outputTo == 'return'),
    or an integer:
      -1  if output was sent to stdout,
      0   if output file was not written,
      size of output file if output file was written.
    """
    commandLine = flatWrite(command)      # prepare command line

    outputTo.strip()                      # clean-up output specifier

    etime = time.time()                   # if e.time is requested, get a timestamp
        
    if outputTo == 'return':              # if we want the output lines:
        output = []                       # ... get them!
        output = os.popen( commandLine ).readlines()

    elif outputTo:                        # if we have an output file:
        if outputTo[0] == '>':            # ... check if we are really redirecting output,

            commandLine += ' '+outputTo
            outputTo = re.sub(r'^[^\w/]+','',outputTo)
            if not outputTo:              # ... check to see an OK file-name,
                die("execCmd: output specifier '%s' does not contain an alpha-numeric file name!" % outputTo)
        else:
            die("execCmd: output specifier '%s' does not contain a '>' for redirection!" % outputTo)

        os.system( commandLine )          # ... execute program,

        if os.path.exists(outputTo):      # ... and check for a successfully written program
            output = os.path.getsize(outputTo)
        else:
            output = 0
    else:                                 # if we just want to run the damn thing:
        os.system( commandLine )          # ... do it right here!
        output = -1

    etime = time.time() - etime           # calculate the elapsed time
    
    # return
    return etime, output, commandLine



def execute(*vars):    # simple 'execute' function
    """
execute(*vars):
    executes a system call submitted as a list
    """
    os.system( flatWrite(vars) )
    # done


def runViaPBS(listOfCommands, project='', type='', dir='', printOnly=0):
    """
runViaPBS(listOfCommands, project='', type='', dir='', printOnly=0):
    Writes a PBS file using the commands specified in the 'listOfCommands',
    which simply is an array of command-strings.  The following options are
    defined:
     * 'project' is used to specify the job name.  If not defined, current
       time is used as 'job#TIME#'
     * If 'type' is set to one of the predetermined job types, 'listOfCommands'
       is modified to accomodate that job type.
       Currently defined jobs are:  'jaguar'
     * 'dir' sets the directory the commands will be run in. If different than
       the current working directory is used
     * If 'printOnly' is set, the PBS file is written, but the job is not
       submitted to the queue.
    """
    if not project:
        project = 'job' + str(int(time.time()))[-5:]

    curdir = os.getcwd()
    if not dir:
        dir = curdir
        
    PBSlines = ["#PBS -l nodes=1,walltime=800:00:00",\
                "#PBS -e oscar_server:%s/%s.ERR" % (curdir,project),\
                "#PBS -o oscar_server:%s/%s.OUT" % (curdir,project),\
                "#PBS -q workq",\
                "#PBS -N %s" % (project),\
                "#!/bin/csh",\
                "",\
                "cd %s" % dir,\
                "",\
                "echo %s $HOST $cwd" % project,\
                ""]
    if not type:
        pass
    elif type == 'jaguar':
        PBSlines.append('setenv LM_LICENSE_FILE @10.0.0.1')

    PBSlines += listOfCommands

    PBSlines += ['','echo \" done with %s\"' % project,\
                 'date','']
    
    PBStext = list2str(PBSlines, "\n") + "\n"
    PBSfile = project+'.PBS'
    writeLineToFile(PBStext, PBSfile)
    if not printOnly:
        os.system('qsub %s' % PBSfile)

    


#
# - I/O
#

def readLinesFromFile(file):
    """
readLinesFromFile(file):
    reads lines from a file and returns them in a list
    """
    try:
        FH = open(file)
        lines = FH.readlines()
    except IOError, (errno, strerror):
        die( "I/O error(%s): %s" % (errno, strerror) )
    else:
        FH.close()

    # return
    return lines


def readInList(file):
    """
readInList(file):
    reads non-empty lines from a file, strips any leading/trailing
    white-space ignoring lines starting with a '#', and returns
    the result in a list
    """
    list = []
    lines = readLinesFromFile(file)
    for line in lines:
        if line.strip() and not re.match(r'^#', line):
            list.append( line.strip() )
    # return
    return list


def writeLinesToFile(lines, file, openMode='w'):
    """
writeLinesToFile(lines, file, openMode='w'):
    writes lines of strings into a file 
    """
    try:
        FH = open(file,openMode)
        FH.writelines(lines)
    except IOError, (errno, strerror):
        die( "I/O error(%s): %s" % (errno, strerror) )
    else:
        FH.close()
    # done


def writeLineToFile(line, file):
    """
writeLineToFile(line, file):
    adds a line (string) to a file
    """
    writeLinesToFile([line], file, 'w')


def addLinesToFile(lines, file):
    """
addLinesToFile(lines, file):
    adds lines of strings to a file
    """
    writeLinesToFile(lines, file, 'a')


def addLineToFile(line, file):
    """
addLineToFile(line, file):
    adds a line (string) to a file
    """
    writeLinesToFile([line], file, 'a')

    
def reIsInLines(reToMatch, lines, returnLineNos=0):
    """
reIsInLines(reToMatch, lines, returnLineNos =0):
    grabs all matching lines from a list of lines and returns them,
    if no match is found, returns empty list.
    if returnLineNos is set to 1, returns the indices of the matching
    lines, instead.
    """
    match = []
    reObject = re.compile(reToMatch)

    if returnLineNos:
        for i in range(len(lines)):
            if reObject.search(lines[i]):
                match.append(i)
    else:
        for line in lines:
            if reObject.search(line):
                match.append(line)
    # return
    return match


def reIsInFile(reToMatch,filename):
    """
reIsInFile(reToMatch,filename):
    grabs all matching lines from a file and returns them,
    if no match is found, returns empty list.
    """
    return reIsInLines( reToMatch, readLinesFromFile(filename) )


def waitForFile(file, toExist =1, checkPeriod =6, maxWaitTime = 86400):
    """
waitForFile(file, toExist =1, checkPeriod =5, maxWaitTime = 86400):
    sleeps 'checkPeriod' seconds and checks for the existance (if
    toExist is  1) or the absence (if toExist is  0) of the path
    'file'.  When the condition is satisfied, it returns  1.  If
    the 'maxWaitTime' is reached, returns  0.
    """
    startTime = time.time()
    checkPeriod = float(checkPeriod)
    maxWaitTime = float(maxWaitTime)

    while os.path.exists(file) ^ toExist:
        time.sleep( checkPeriod )

        if (time.time() - startTime) > maxWaitTime:
            return 0
    # done
    return 1


def getSysInfo(n=5):
    """
getSysInfo(n=5):
    obtains common environmental varibles from the os/time modules,
    and returns the first <n> of the below items in the following order:
    (curuser, curhost, homedir, initdir, curtime)
    """
    curuser = os.environ['USER']
    initdir = os.getcwd()
    curhost = os.environ['HOST']
    homedir = os.environ['HOME']
    curtime = time.ctime()

    myTuple = (curuser, curhost, homedir, initdir, curtime)
    if n > len(myTuple):  n = len(myTuple)
    
    # done
    return myTuple[:n]


#
# - array utilities
#

def flatten(array):
    """
flatten(array):
    flattens list/tuple objects
    """
    flatList = []

    # join all vars into a single list:
    for element in array:
        if type(element) is types.ListType or type(element) is types.TupleType:
            flatList += flatten(element)
        elif type(element) is types.DictType:
            die("flatten: Cannot flatten dictionary types!")
        else:
            flatList.append(element)

    # return
    return flatList


def flatWrite(*vars):
    """
flatWrite(*vars):
    turns tuple/list to a flat-list, and returns it as a string
    """
    # return the flattenned list as a string:
    return list2str( flatten(vars) )


def initArray(noOfElements,initializeTo):
    """
initArray(noOfElements,initializeTo):
    creates an array of size 'noOfElements' and initializes each
    element to 'initializeTo'
    """
    return noOfElements * [initializeTo]


def initDict(arrayOfKeys,initializeTo):
    """
initDict(arrayOfKeys,initializeTo):
    creates a dictionary using the contents of 'arrayOfKeys' as keys
    and initializes each element to 'initializeTo'
    """
    newDict = {}
    for element in arrayOfKeys:
        newDict[element] = initializeTo    
    return newDict


def addUp(array):
    """
addUp(array):
    returns the sum of the elements of the array
    """
    total = 0
    for element in array:
        total += element
    return total


def nonZeroElements(array,returnNonZeroElements=0):
    """
nonZeroElements(array,returnNonZeroElements=0):
    counts and returns the number of non-zero elements in the array,
    and also returns these elements if specified
    """
    count = 0
    nonZeroList = []
    for element in array:
        if element:
            count += 1
            nonZeroList.append(element)

    if returnNonZeroElements:
        return nonZeroList
    else:
        return count


#
# - file manipulation:
#

def assertPath(path, fileDescription=None):
    """
assertPath(path, fileDescription=None):
    checks to see if path exists, and if it does, returns 1.  If it 
    doesn't, dies with an ERROR message that includes fileDescription
    """
    if os.path.exists(path):
        return 1
    else:
        if fileDescription:
            die("Cannot find %s:  %s" % (fileDescription, path))
        else:
            die("Cannot find path:  %s" % path)
    # done
    

def deltree(root):
    """
deltree(root):
    deletes the given directory 'root' with its contents
    """
    for curdir, dirs, files in os.walk(root, topdown=False):
        for name in files:
            os.remove( os.path.join(curdir,name) ) # remove each file in dir
        for name in dirs:
            os.rmdir(  os.path.join(curdir,name) ) # remove each dir  in dir
    os.rmdir(root)
    # done


def delAll(fileList):
    """
delAll(fileList):
    deletes all files/directories provided in the fileList
    """
    for item in fileList:
        if os.path.isdir(item):
            deltree(item)
        else:
            os.remove(item)
    # done


def derefSymLink(file, rmOriginal =0):
    """
derefSymLink(file, rmOriginal =0):
    if the file is a sym.link, dereferences it,
    and if 'rmOriginal' is set, deletes the original
    """
    if os.path.islink(file):
        originalFile = os.readlink(file)
        os.remove(file)
        
        if rmOriginal:
            os.rename(originalFile, file)
            #os.system( 'mv %s %s' % (originalFile, file) )
        else:
            if os.path.isdir(originalFile):    
                shutil.copytree(originalFile, file)
            else:
                shutil.copy2(originalFile, file)
    # done



#
# - utilities:
#

def commonTime(etime, returnTuple=0):
    """
commonTime(etime, returnTuple=0):
    converts time in seconds to common time
    """
    etuple = time.gmtime(etime)
    ztuple = time.gmtime(0)

    ctuple = ( etuple[0] - ztuple[0], \
               etuple[7] - ztuple[7], \
               etuple[3] - ztuple[3], \
               etuple[4] - ztuple[4], \
               etuple[5] - ztuple[5]  )

    # return
    if returnTuple:
        return ctuple    # return tuple (if selected)
    else:
        cstring = ''
        if ctuple[0]:  cstring += '%d years, ' % ctuple[0]
        if ctuple[1]:  cstring += '%d days, ' % ctuple[1]
        if ctuple[2]:  cstring += '%d hours, ' % ctuple[2]
        if ctuple[3]:  cstring += '%d mins, ' % ctuple[3]
        cstring += '%d secs' % ctuple[4]
        return cstring   # return string (default)




#-------------------------------------
#
# - Print information
#
if __name__ == '__main__':

    # get directory:
    directory = dir()

    # set imported stuff we don't want to see:
    imported = ['sys', 'os', 'string', 'types', 'time', 're', 'shutil']


    # print __doc__ for the module:
    print
    print ( '-'*60 )
    if 'version' not in directory:  version = '??????'
    print "%-45s%15s" % (os.path.basename(sys.argv[0]), 'ver: '+version)

    print ( '-'*60 )
    print __doc__


    # import types:
    import types

    # create hash-table:
    hashtable = {}
    for item in directory:
        actual_item = eval(item)
        if item in imported:
            # don't show imported stuff:
            pass
        elif type(actual_item) is types.ModuleType:
            # don't discuss other modules:
            pass
        elif type(actual_item) is types.FunctionType or type(actual_item) is types.ClassType:
            # show __doc__s for functions/classes:
            hashtable[item] = actual_item.__doc__             
        elif item[0] != '_':
            # for other stuff show the value:
            hashtable[item] = '\n'+item+' = '+str(actual_item)+'\n'

    # print info out
    keys = hashtable.keys()
    keys.sort()
    
    print 'Contents:'
    print ( '-'*60 )
    for item in keys:
        #print ( '--- '*6 ),
        print ' ', 
        print hashtable[item],

    print
    print ( '-'*60 )
    print 'contact:  caglar@wag.caltech.edu'
    print ( '-'*60 )
    print
    
    # done!

    
