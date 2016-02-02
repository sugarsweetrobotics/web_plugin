import os, sys
import WSB
from plugin import *

class RtcPlugin(PluginObject):
    
    def __init__(self):
        PluginObject.__init__(self, 'mgrRtc')

    def list(self,pkg):
        res = WSB.getRTCList(pkg)
        return [True, res]
    
    def echo(self, msg):
        sys.stdout.write('misc_echo(%s)\n' % msg)
        return [True, msg]

    def repositories(self, pkg):
        res = WSB.getRtcRepositoryList(pkg)
        return [True, res]

    def repository_pull(self, package, rtc):
        res = WSB.pullRTCRepository(package, rtc)
        return [True, res]

    def repository_push(self, package, rtc):
        res = WSB.pushRTCRepository(package, rtc)
        return [True, res]

    def repository_commit(self, package, rtc, comment):
        res = WSB.commitRTCRepository(package, rtc, comment)
        return [True, res]

    def longlist(self,pkg):
        res = WSB.getRTCLongList(pkg)
        return [True, res]


    def profile(self, pkg, rtc):
        res = WSB.getRTCProfile(pkg, rtc)
        return [True, res]
