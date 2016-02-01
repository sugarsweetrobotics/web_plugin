
import os, subprocess, yaml, types, time, sys
import wasanbon

def __call(*args, **kwargs):
    cmd = ['wasanbon-admin.py']
    shell = False
    for arg in args:
        cmd.append(arg)
    if sys.platform == 'win32':
        shell = True
    sys.stdout.write('check_output: %s\n' % str(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell)
    #p.wait()
    #return p.stdout
    #std_out_data, std_err_data = p.communicate()
    return p #std_out_data


def __check_output(*args, **kwargs):
    cmd = ['wasanbon-admin.py']
    shell = False
    for arg in args:
        cmd.append(arg)
    if sys.platform == 'win32':
        shell = True
    sys.stdout.write('check_output: %s\n' % str(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell)
    #p.wait()
    #return p.stdout
    std_out_data, std_err_data = p.communicate()
    return std_out_data

def __check_mgr_output(*args, **kwargs):
    cmd = ['./mgr.py']
    shell = False
    if sys.platform == 'win32':
        cmd = ['mgr.py']
        shell = True
    for arg in args:
        cmd.append(arg)
    sys.stdout.write('check_mgr_output: %s\n' % str(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell)
    #p.wait()
    std_out_data, std_err_data = p.communicate()
    return std_out_data

def __mgr_call(*args, **kwargs):
    cmd = ['./mgr.py']
    shell = False
    if sys.platform == 'win32':
        cmd = ['mgr.py']
        shell = True
    for arg in args:
        cmd.append(arg)
    sys.stdout.write('mgr_call: %s\n' % str(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell)
    return p

def getVersion():
    stdout = __check_output('version')
    platform_version = stdout.split('\n')[0].split()[-1]
    wasanbon_version = stdout.split('\n')[1].split()[-1]
    return {'platform':platform_version, 
            'wasanbon':wasanbon_version}

def getPackageRepositoryList():
    stdout = __check_output('repository', 'list', '-l')
    print stdout
    return stdout

def getRtcRepositoryList(pkg):
    try:
        dir = __check_output('package', 'directory', pkg).strip()
    except:
        return ""

    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['repository', 'list', '-l'] 
    strval = ""
    try:
        stdout = __check_mgr_output(*sub)
        strval = stdout
    except:
        pass
    os.chdir(cwd)
    return strval
   

def getRepositoryRTC(rtc):
    stdout = __check_output('repository', 'rtc', rtc)
    return yaml.load(stdout)


def getStatus():
    stdout = __check_output('status')
    dic = {}
    for line in stdout.split('\n'):
        if len(line.strip()) == 0:
            continue
        if line.strip().startswith('- Checking'):
            continue
        name = line.split()[1]
        status = line.split()[-1]
        dic[name] = status
    return dic
    
def getRepositories():
    stdout = __check_output('repository', 'status', '-l')
    return yaml.load(stdout)
    
def getPackages():
    stdout = __check_output('package', 'list', '-l')
    return stdout #yaml.load(stdout.read())

def getRunningPackages():
    stdout = __check_output('package', 'list', '-l', '-r')
    return stdout #yaml.load(stdout.read())
    
"""
def getRunningPackages():
    stdout = __check_output('package', 'list', '-r')
    y = yaml.load(stdout)
    if not y:
        return None
    elif type(y) != types.ListType:
        return [y]
    return y
"""
    
def clonePackage(pkg):
    stdout = __check_output('repository', 'clone', pkg, '-v')
    return stdout

def deletePackage(pkg):
    ret = __check_output('package', 'delete', pkg, '-r').strip()
    return ret

def getPackageAlternative(pkg, sub):

    dir = __check_output('package', 'directory', pkg).strip()

    cwd = os.getcwd()
    os.chdir(dir)
    try:
        sub = ['-a'] 
        stdout = __check_mgr_output(*sub)
        #str = stdout.read().split()
        str = stdout.split()
    except:
        str = ""

    os.chdir(cwd)
    return str

def getRTCList(pkg):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    try:
        sub = ['rtc', 'list', '-d'] 
        stdout = __check_mgr_output(*sub)
        #str = stdout.read().strip()
        str = stdout
    except:
        str = ""
    os.chdir(cwd)    
    return str


def getRTCLongList(pkg):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtc', 'list', '-l'] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    #str = stdout.read()
    d = yaml.load(stdout.strip())
    return d

def getRTCProfile(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtcprofile', 'dump', rtc] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    #str = stdout.read()
    return stdout.strip()
    #d = yaml.load(str)

    
def getSystemList(pkg):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'list', '-l'] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    #str = stdout.read()
    return stdout.strip()
    #d = yaml.load(str)
    #return d

def getRTSProfile(pkg, filename):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'dump', '-f', filename] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    #str = stdout.read()
    return stdout.strip()


def getPackageRTC(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtc', 'profile', rtc] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    #str = stdout.read()
    d = yaml.load(stdout.strip())
    return d

def runDefaultSystem(pkg):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'run', '-v'] 
    stdout = __mgr_call(*sub)
    os.chdir(cwd)
    start_time = time.time()
    timeout = 15
    while True:
        running = getRunningPackages()
        print 'running-', running
        if running:
            if pkg in running:
                return 0
        diff_time = time.time() - start_time
        if diff_time > timeout:
            return -2

    return -1

def terminateSystem(pkg):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'terminate'] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    #str = stdout.read()
    str = stdout.strip()
    start_time = time.time()
    timeout = 15
    while True:
        running = getRunningPackages()
        print 'Running Packages are ', running
        if running:
            if pkg in running:
                sys.stdout.write(' pkg(%s) is still running\n' % pkg)
                continue
            else:
                sys.stdout.write(' pkg(%s) stopped\n' % pkg)
                return 0
        else:
            sys.stdout.write(' No pkgs are running.\n')
            return 0
        diff_time = time.time() - start_time
        if diff_time > timeout:
            return -2
    return -1

def startNamingService(port):
    sub = ['nameserver', 'start', '-p', str(port)] 
    #stdout = __check_output(*sub)
    __call(*sub)
    #res = stdout.read()
    #print res
    return "Success"

def stopNamingService(port):
    sub = ['nameserver', 'stop', '-p', str(port)] 
    stdout = __check_output(*sub)
    #res = stdout.read()
    return stdout

def checkNamingService():
    sub = ['nameserver', 'check_running']
    stdout = __check_output(*sub)
    #res = stdout.read()
    return stdout

def treeNamingService(port):
    sub = ['nameserver', 'tree', '-d']
    stdout = __check_output(*sub)
    #res = stdout.read()
    return stdout

def treeNamingServiceEx(host, port):
    sub = ['nameserver', 'tree', '-d', '-p', str(port), '-u', host]
    stdout = __check_output(*sub)
    #res = stdout.read()
    return stdout

    
def buildRTC(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtc', 'build', rtc, '-v'] 
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return p.returncode, std_out_data


def cleanRTC(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtc', 'clean', rtc, '-v'] 
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return p.returncode, std_out_data

def deleteRTC(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtc', 'delete', rtc, '-v'] 
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return p.returncode, std_out_data


def getRTCConfList(pkg):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtcconf', 'show', '-l']
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return std_out_data
    
def updateSystemFile(pkg, filename, content):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'cat', '-f', filename, content]
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return std_out_data

def updateRTCProfile(pkg, rtc, content):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    filename = os.path.join(dir, 'temp_' + rtc + '_RTC.xml')
    if os.path.isfile(filename):
        os.remove(filename)
    f = open(filename, 'w')
    f.write(content)
    f.close()
    #sub = ['rtcprofile', 'cat', rtc, content]
    sub = ['rtcprofile', 'cat', rtc, '-i', filename]
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    print std_out_data
    return std_out_data

def syncRTCProfile(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtc', 'update_profile', rtc]
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return 'Success'
    
def copySystem(pkg, src, dst):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'copy', src, dst, '-f']
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return std_out_data

def deleteSystem(pkg, filename):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'delete', filename, '-f']
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return std_out_data

def pullRTCRepository(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['repository', 'pull', rtc, '-v']
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return std_out_data.strip()

def pushRTCRepository(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['repository', 'push', rtc, '-v']
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return std_out_data.strip()

def commitRTCRepository(pkg, rtc, comment):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['repository', 'commit', rtc, comment]
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return std_out_data.strip()

def activateRTC(fullpath):
    stdout = __check_output('nameserver', 'activate_rtc', fullpath)
    return stdout
    
def deactivateRTC(fullpath):
    stdout = __check_output('nameserver', 'deactivate_rtc', fullpath)
    return stdout
    
def resetRTC(fullpath):
    stdout = __check_output('nameserver', 'reset_rtc', fullpath)
    return stdout

def exitRTC(fullpath):
    stdout = __check_output('nameserver', 'exit_rtc', fullpath)
    return stdout
    
def configureRTC(rtc, confset, confname, confvalue):
    stdout = __check_output('nameserver', 'configure', rtc, '-s', confset, confname, confvalue)
    return stdout

def listConnectablePairs(nss):
    stdout = __check_output('nameserver', 'list_connectable_pair', '-n', nss) 
    return stdout
    
def connectPorts(port0, port1, param):
    params = param.split(',')
    cmd = ['nameserver', 'connect', port0, port1]
    for p in params:
        if len(p) > 0:
            cmd = cmd + ['-p', p]
    stdout = __check_output(*cmd)
    return stdout

def disconnectPorts(port0, port1):
    cmd = ['nameserver', 'disconnect', port0, port1]
    stdout = __check_output(*cmd)
    return stdout

def sendCode(code):
    code_dir = 'codes'
    if not os.path.isdir(code_dir):
        os.mkdir(code_dir)
    codeName = 'code' + wasanbon.timestampstr() + '.py'
    fileName = os.path.join(code_dir, codeName)
    f = open(fileName, 'w')
    f.write(code)
    f.close()
    return fileName

def startCode(filename):
    args = {}
    args['env'] = os.environ.copy()
    #args['preexec_fn'] = None if sys.platform == 'win32' else disable_sig
    args['stdout'] = subprocess.PIPE
    args['stdin'] = subprocess.PIPE
    if sys.platform == 'win32':
        args['creationflags'] = 512
    if sys.platform == 'win32':
        for path in sys.path:
            if os.path.isfile(os.path.join(path, 'python.exe')):
                exe = os.path.join(path, 'python.exe')
                cmd = [exe, filename]
                break
    else:
        cmd = ['python', filename]
    p = subprocess.Popen(cmd, **args)
    return p.pid
    
