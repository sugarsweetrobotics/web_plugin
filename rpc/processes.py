import os, sys
import WSB
from plugin import *


class ProcessesPlugin(PluginObject):
    
    def __init__(self):
        PluginObject.__init__(self, 'processes')
    
    def run(self, filename, args):
        self.debug('run(%s, %s)' % (filename, str(args)))
        import subprocess
        if filename.endswith('.py'):
            cmd = ['python', filename]
            try:
                p = subprocess.Popen(cmd)
                return self.return_value(True, '', ('python', p.pid))
            except Exception, ex:
                traceback.print_exc()
                return self.return_value(False, 'Exception: %s' % str(ex), [])

        return self.return_value(False, 'Unknown File Extension.', [])
