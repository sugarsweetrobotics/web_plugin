import os, sys
import WSB
from plugin import *

class FilesPlugin(PluginObject):
    
    def __init__(self):
        PluginObject.__init__(self, 'files')

        
    def list_directory(self, path):
        """ List directory 
        :param string path: Path for listing
        :rtype: tupple
        :return: tupple(Successflag, Message, List of directory)
        """
        self.debug('files_list_directory(%s)' % path)
        try:
            return self.return_value(True, '', os.listdir(path))
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass

    def change_directory(self, path):
        """ Change directory
        :param string path: Destination path.
        :rtype: tupple
        :return: tupple(Success flag, Message, current directory after changed.)
        """
        self.debug('change_directory(%s)' % path)
        try:
            os.chdir(path)
            return self.return_value(True, '', os.getcwd())
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass
      
    def print_working_directory(self):
        """ Print Current Directory
        """
        self.debug('print_working_directory')
        try:
            return self.return_value(True, '', os.getcwd())
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass

    def upload_file(self, filename, file_content):
        self.debug('upload_file(%s, %s)' % (filename, file_content))
        try:
            open(filename, 'w').write(file_content)
            return self.return_value(True, '', filename)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass

    def download_file(self, filename):
        self.debug('download_file(%s)' % filename)
        try:
            return (True, '', open(filename, 'r').read())
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass

    def delete_file(self, filename):
        self.debug('delete_file(%s)' % filename)
        try:
            os.remove(filename)
            return (True, '', filename)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass
