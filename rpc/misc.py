import os, sys
import WSB
from plugin import *


class MiscPlugin(PluginObject):
    
    def __init__(self):
        PluginObject.__init__(self, 'misc')
    
    def echo(self, msg):
        sys.stdout.write('misc_echo(%s)\n' % msg)
        return [True, msg]

    def version(self):
        res = WSB.getVersion()
        return [True, res]

    def status(self):
        res = WSB.getStatus()
        return [True, res]
