import sys

class PluginObject:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def debug(self, msg):
        sys.stdout.write('Plugin(%s) %s\n' % (self._name, str(msg)))
        pass

    def return_value(self, success_flag, msg, return_value):
        self.debug('return_value is (%s, %s, %s)' % (success_flag, msg, return_value))
        return (success_flag, msg, return_value)
