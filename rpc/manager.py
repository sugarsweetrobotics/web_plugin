import os, types, traceback, sys
from twisted.web import server, xmlrpc, resource
from twisted.web.xmlrpc import withRequest

import WSB
from plugin import *
from misc import *
from processes import *
from files import *
from rtc import *
from admin import *

class RpcManager(xmlrpc.XMLRPC):
    """
    An example object to be published.
    """
    isLeaf = True

    def __init__(self, directory=None):
        xmlrpc.XMLRPC.__init__(self, allowNone=True)

        self.add_plugin(MiscPlugin())
        self.add_plugin(FilesPlugin())
        self.add_plugin(ProcessesPlugin())
        self.add_plugin(RtcPlugin())
        self.add_plugin(AdminPlugin())
        if not directory:
            directory = os.getcwd()
        self.directory = directory
        if not os.path.isdir(directory):
            os.mkdir(directory)

        self.old_directory = os.getcwd()


    def add_plugin(self, plugin_obj):
        for atr_name in dir(plugin_obj):
            attribute = getattr(plugin_obj, atr_name)
            if atr_name.startswith('_'):
                continue

            if type(attribute) == types.MethodType:
                func_name = 'xmlrpc_' + plugin_obj.name + '_' + atr_name
                print func_name
                setattr(self, func_name, attribute)

    def pre_rpc(self):
        os.chdir(self.directory)

    def post_rpc(self):
        os.chdir(self.old_directory)
        
    #def xmlrpc_echo(self, x):
    #
    #    return [True, x]

    def xmlrpc_get_package_alter(self, pkg, sub):
        res = WSB.getPackageAlternative(pkg, sub)
        return [True, res]
        


    # Repository Management


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

    def xmlrpc_running_packages(self, request):
        res = WSB.getRunningPackages()
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
        res = WSB.treeNamingService(port)
        return [True, res.strip()]

    def xmlrpc_tree_name_service_ex(self, host, port):
        res = WSB.treeNamingServiceEx(host, port)
        return [True, res.strip()]
        

    def xmlrpc_running_packages(self):
        res = WSB.getRunningPackages()
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

    def xmlrpc_rtcprofile_update(self, pkg, rtc, content):
        res = WSB.updateRTCProfile(pkg, rtc, content)
        return [True, res]

    def xmlrpc_rtcprofile_sync(self, pkg, rtc):
        res = WSB.syncRTCProfile(pkg, rtc)
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

    def xmlrpc_activate_rtc(self, fullpath):
        res = WSB.activateRTC(fullpath)
        return [True, res]

    def xmlrpc_deactivate_rtc(self, fullpath):
        res = WSB.deactivateRTC(fullpath)
        return [True, res]

    def xmlrpc_reset_rtc(self, fullpath):
        res = WSB.resetRTC(fullpath)
        return [True, res]

    def xmlrpc_exit_rtc(self, fullpath):
        res = WSB.exitRTC(fullpath)
        return [True, res]


    def xmlrpc_configure_rtc(self, rtc, confset, confname, confvalue):
        res = WSB.configureRTC(rtc, confset, confname, confvalue)
        return [True, res]

    def xmlrpc_list_connectable_pairs(self, nss):
        res = WSB.listConnectablePairs(nss)
        return [True, res]
        
    def xmlrpc_connect_ports(self, port0, port1, param):
        res = WSB.connectPorts(port0, port1, param)
        return [True, res]

    def xmlrpc_disconnect_ports(self, port0, port1):
        res = WSB.disconnectPorts(port0, port1)
        return [True, res]


    def xmlrpc_misc_send_code(self, code):
        res = WSB.sendCode(code)
        return [True, res]

    def xmlrpc_misc_start_code(self, filename):
        res = WSB.startCode(filename)
        return [True, res]

    def xmlrpc_misc_kill_code(self, filename):
        res = WSB.killCode(self, filename)
        return [True, res]

    def xmlrpc_misc_read_stdout(self, filename):
        res = WSB.readStdout(filename)
        return [True, res]

    def xmlrpc_misc_communicate(self, filename):
        res = WSB.communicate(filename)
        return [True, res]
