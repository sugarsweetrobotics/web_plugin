
import os, subprocess, yaml, types, time
import wasanbon


def __check_output(*args, **kwargs):
    cmd = ['wasanbon-admin.py']
    for arg in args:
        cmd.append(arg)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    p.wait()
    return p.stdout

def __check_mgr_output(*args, **kwargs):
    cmd = ['./mgr.py']
    for arg in args:
        cmd.append(arg)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    p.wait()
    return p.stdout

def __mgr_call(*args, **kwargs):
    cmd = ['./mgr.py']
    for arg in args:
        cmd.append(arg)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return p

def getVersion():
    stdout = __check_output('version')
    platform_version = stdout.readline().split()[-1]
    wasanbon_version = stdout.readline().split()[-1]
    return {'platform':platform_version, 
            'wasanbon':wasanbon_version}

def getRepositoryPackage(pkg):
    stdout = __check_output('repository', 'package', pkg)
    return yaml.load(stdout.read())

def getRepositoryRTC(rtc):
    stdout = __check_output('repository', 'rtc', rtc)
    return yaml.load(stdout.read())

def getStatus():
    stdout = __check_output('status')
    dic = {}
    for line in stdout:
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
    return yaml.load(stdout.read())
    
def getPackages():
    stdout = __check_output('package', 'list', '-l')
    return yaml.load(stdout.read())


    
def getRunningPackages():
    stdout = __check_output('package', 'list', '-r')
    y = yaml.load(stdout.read())
    if not y:
        return None
    elif type(y) != types.ListType:
        return [y]
    return y
    
def clonePackage(pkg):
    stdout = __check_output('package', 'clone', pkg, '-v')
    return stdout.read()

def deletePackage(pkg):
    ret = __check_output('package', 'delete', pkg).read().strip()
    return ret

def getPackageAlternative(pkg, sub):
    dir = __check_output('package', 'directory', pkg).read().strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['-a'] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    str = stdout.read()
    return str.split()

def getRTCList(pkg):
    dir = __check_output('package', 'directory', pkg).read().strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtc', 'list', '-d'] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    str = stdout.read()
    return str.strip()
    #d = yaml.load(str)
    #return d

def getRTCLongList(pkg):
    dir = __check_output('package', 'directory', pkg).read().strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtc', 'list', '-l'] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    str = stdout.read()
    d = yaml.load(str)
    return d

def getRTCProfile(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).read().strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtcprofile', 'dump', rtc] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    str = stdout.read()
    return str.strip()
    #d = yaml.load(str)

    
def getSystemList(pkg):
    dir = __check_output('package', 'directory', pkg).read().strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'list', '-l'] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    str = stdout.read()
    return str.strip()
    #d = yaml.load(str)
    #return d

def getRTSProfile(pkg, filename):
    dir = __check_output('package', 'directory', pkg).read().strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'dump', '-f', filename] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    str = stdout.read()
    return str.strip()


def getPackageRTC(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).read().strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtc', 'profile', rtc] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    str = stdout.read()
    d = yaml.load(str)
    return d

def runDefaultSystem(pkg):
    dir = __check_output('package', 'directory', pkg).read().strip()
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
    dir = __check_output('package', 'directory', pkg).read().strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'terminate'] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    str = stdout.read()
    start_time = time.time()
    timeout = 15
    while True:
        running = getRunningPackages()
        print 'running-', running
        if running:
            if pkg in running:
                continue
            else:
                return 0
        diff_time = time.time() - start_time
        if diff_time > timeout:
            return -2
    return -1

def startNamingService(port):
    sub = ['nameserver', 'start', '-p', str(port)] 
    stdout = __check_output(*sub)
    res = stdout.read()
    print res
    return res

def stopNamingService(port):
    sub = ['nameserver', 'stop', '-p', str(port)] 
    stdout = __check_output(*sub)
    res = stdout.read()
    return res

def checkNamingService():
    sub = ['nameserver', 'check_running']
    stdout = __check_output(*sub)
    res = stdout.read()
    return res
    
def buildRTC(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).read().strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtc', 'build', rtc, '-v'] 
    p = __mgr_call(*sub)
    p.wait()
    os.chdir(cwd)
    return p.returncode, p.stdout.read()

def cleanRTC(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).read().strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtc', 'clean', rtc, '-v'] 
    p = __mgr_call(*sub)
    p.wait()
    os.chdir(cwd)
    return p.returncode, p.stdout.read()

def deleteRTC(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).read().strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtc', 'delete', rtc, '-v'] 
    p = __mgr_call(*sub)
    p.wait()
    os.chdir(cwd)
    return p.returncode, p.stdout.read()

def getRTCConfList(pkg):
    dir = __check_output('package', 'directory', pkg).read().strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtcconf', 'show', '-l']
    p = __mgr_call(*sub)
    p.wait()
    os.chdir(cwd)
    return p.stdout.read()
    
def updateSystemFile(pkg, filename, content):
    dir = __check_output('package', 'directory', pkg).read().strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'cat', '-f', filename, '"' + content + '"']
    p = __mgr_call(*sub)
    p.wait()
    os.chdir(cwd)
    return p.stdout.read()
    
