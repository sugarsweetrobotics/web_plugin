import os, sys
import WSB
from plugin import *


class ProcessesPlugin(PluginObject):
    
    def __init__(self):
        PluginObject.__init__(self, 'processes')
    
    def run(self, filename, args):
        import subprocess
        if filename.endswith('.py'):
            cmd = ['python', filename]
            try:
                p = subprocess.Popen(cmd)
            except:
                traceback.print_exc()
                return [False, '']
            return [True, '']
        return [False, 'Unknown File Extension.']
