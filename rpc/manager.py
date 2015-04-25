import os
from twisted.web import server, xmlrpc, resource
from twisted.web.xmlrpc import withRequest

import WSB

class RpcManager(xmlrpc.XMLRPC):
    """
    An example object to be published.
    """
    isLeaf = True

    def __init__(self, directory=None):
        xmlrpc.XMLRPC.__init__(self, allowNone=True)
        if not directory:
            directory = os.getcwd()
        self.directory = directory
        if not os.path.isdir(directory):
            os.mkdir(directory)

        self.old_directory = os.getcwd()

    def pre_rpc(self):
        os.chdir(self.directory)

    def post_rpc(self):
        os.chdir(self.old_directory)
        
    def xmlrpc_echo(self, x):

        return [True, x]

    def xmlrpc_version(self):
        res = WSB.getVersion()
        return [True, res]

    def xmlrpc_get_package_alter(self, pkg, sub):
        res = WSB.getPackageAlternative(pkg, sub)
        return [True, res]
        
    def xmlrpc_status(self):
        res = WSB.getStatus()
        return [True, res]

    def xmlrpc_clone_package(self, pkg):
        self.pre_rpc()
        res = WSB.clonePackage(pkg)
        self.post_rpc()
        return [True, res]

    # Repository Management
    def xmlrpc_package_repositories(self):
        res = WSB.getPackageRepositoryList()
        return [True, res]

    def xmlrpc_repository_package(self, pkg):
        res = WSB.getRepositoryPackage(pkg)
        return [True, res]

    def xmlrpc_repository_rtc(self, rtc):
        res = WSB.getRepositoryRTC(rtc)
        return [True, res]
    
    def render_OPTIONS(self, request):    
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')        
        request.setHeader('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
        return ""

    # Package Management
    @withRequest
    def xmlrpc_packages(self, request):
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'POST, GET')
        request.setHeader('Access-Control-Allow-Headers', 'x-prototype-version,x-requested-with')
        request.setHeader('Access-Control-Max-Age', 2520) # 42 hours
        
        res = WSB.getPackages()
        #res = '<package></package>'
        
        return [True, (res)]

    def xmlrpc_start_name_service(self, port):
        res = WSB.startNamingService(port)
        return [True, res.strip()]

    def xmlrpc_check_name_service(self):
        res = WSB.checkNamingService()
        return [True, res.strip()]

    def xmlrpc_stop_name_service(self, port):
        res = WSB.stopNamingService(port)
        return [True, res.strip()]

    def xmlrpc_tree_name_service(self, port):
        res = WSB.treeNamingservice(port)
        return [True, res.strip()]
        

    def xmlrpc_running_packages(self):
        res = WSB.getRunningPackages()
        return [True, res]

    def xmlrpc_rtc_longlist(self,pkg):
        res = WSB.getRTCLongList(pkg)
        return [True, res]

    def xmlrpc_rtc_list(self,pkg):
        res = WSB.getRTCList(pkg)
        return [True, res]

    def xmlrpc_rtc_profile(self, pkg, rtc):
        res = WSB.getRTCProfile(pkg, rtc)
        return [True, res]

    def xmlrpc_build_rtc(self, pkg, rtc):
        result, stdout = WSB.buildRTC(pkg, rtc)
        return [True, result, stdout]

    def xmlrpc_clean_rtc(self, pkg, rtc):
        result, stdout = WSB.cleanRTC(pkg, rtc)
        return [True, result, stdout]

    def xmlrpc_delete_rtc(self, pkg, rtc):
        result, stdout = WSB.deleteRTC(pkg, rtc)
        return [True, result, stdout]

    def xmlrpc_delete_package(self, pkg):
        res = WSB.deletePackage(pkg)
        return [True, res]



    def xmlrpc_package_rtc(self, pkg, rtc):
        res = WSB.getPackageRTC(pkg, rtc)
        return [True, res]

    def xmlrpc_rtcconf_list(self, pkg):
        res = WSB.getRTCConfList(pkg)
        return [True, res]



    def xmlrpc_rts_profile(self, pkg, filename):
        res = WSB.getRTSProfile(pkg, filename)
        return [True, res]

    def xmlrpc_system_update(self, pkg, filename, content):
        res = WSB.updateSystemFile(pkg, filename, content)
        return [True, res]
    
    def xmlrpc_system_copy(self, pkg, srcfilename, dstfilename):
        res = WSB.copySystem(pkg, srcfilename, dstfilename)
        return [True, res]
    
    def xmlrpc_system_delete(self, pkg, filename):
        res = WSB.deleteSystem(pkg, filename)
        return [True, res]

    def xmlrpc_system_list(self, pkg):
        res = WSB.getSystemList(pkg)
        return [True, res]

    def xmlrpc_run_default_system(self, pkg):
        res = WSB.runDefaultSystem(pkg)
        return [True, res]

    def xmlrpc_terminate_system(self, pkg):
        res = WSB.terminateSystem(pkg)
        return [True, res]

    def xmlrpc_system_run(self, pkg):
        res = WSB.runSystem(pkg)
        return [True, res]
