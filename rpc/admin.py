import os, sys, traceback
import WSB
from plugin import *

class AdminPlugin(PluginObject):

    def __init__(self):
        PluginObject.__init__(self, 'admin')

    def repository_list(self):
        self.debug('repository_list()')
        try:
            stdout = check_output('repository', 'list', '-l')
            return self.return_value(True, '', stdout)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])

    def repository_clone(self, pkg):
        self.debug('repository_clone(%s)' % pkg)
        try:
            stdout = check_output('repository', 'clone', pkg, '-v')
            return self.return_value(True, '', stdout)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])

    def package_list(self):
        self.debug('package_list()')
        try:
            stdout = check_output('package', 'list', '-l')
            return self.return_value(True, '', (stdout))
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])

    def package_running_list(self):
        self.debug('package_running_list()')
        try:
            stdout = check_output('package', 'list', '-l', '-r')
            return self.return_value(True, '', stdout)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])


    def package_delete(self, pkg):
        self.debug('package_delete(%s)' % pkg)
        try:
            stdout = check_output('package', 'delete', pkg, '-r').strip()
            return self.return_value(True, '', stdout)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
