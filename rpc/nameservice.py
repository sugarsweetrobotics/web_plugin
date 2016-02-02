import os, sys
import WSB
from plugin import *

class NameServicePlugin(PluginObject):
    def __init__(self):
        PluginObject.__init__(self, 'nameservice')

    def activate_rtc(self, fullpath):
        res = WSB.activateRTC(fullpath)
        return [True, res]

    def deactivate_rtc(self, fullpath):
        res = WSB.deactivateRTC(fullpath)
        return [True, res]

    def reset_rtc(self, fullpath):
        res = WSB.resetRTC(fullpath)
        return [True, res]

    def exit_rtc(self, fullpath):
        res = WSB.exitRTC(fullpath)
        return [True, res]

    def configure_rtc(self, rtc, confset, confname, confvalue):
        res = WSB.configureRTC(rtc, confset, confname, confvalue)
        return [True, res]

    def list_connectable_pairs(self, nss):
        res = WSB.listConnectablePairs(nss)
        return [True, res]
        
    def connect_ports(self, port0, port1, param):
        res = WSB.connectPorts(port0, port1, param)
        return [True, res]

    def disconnect_ports(self, port0, port1):
        res = WSB.disconnectPorts(port0, port1)
        return [True, res]

    def start(self, port):
        res = WSB.startNamingService(port)
        return [True, res.strip()]

    def check_runngin(self):
        res = WSB.checkNamingService()
        return [True, res.strip()]

    def stop(self, port):
        res = WSB.stopNamingService(port)
        return [True, res.strip()]

    def tree(self, host, port):
        res = WSB.treeNamingServiceEx(host, port)
        return [True, res.strip()]
        
 
