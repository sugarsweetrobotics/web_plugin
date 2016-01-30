import os, sys
import WSB
from plugin import *

class FilesPlugin(PluginObject):
    
    def __init__(self):
        PluginObject.__init__(self, 'files')

    def list_directory(self, path):
        sys.stdout.write('files_list_directory(%s)\n' % path)
        try:
            return [True, os.listdir(path)]
        except:
            traceback.print_exc()
        return [False, []]

    def change_directory(self, path):
        try:
            os.chdir(path)
            return [True, os.getcwd()]
        except:
            traceback.print_exc()
        return [False, '']
      
    def print_working_directory(self):
        try:
            return [True, os.getcwd()]
        except:
            traceback.print_exc()
        return [False, '']

    def upload_file(self, filename, file_content):
        try:
            open(filename, 'w').write(file_content)
            return [True, filename]
        except:
            traceback.print_exc()
        return [False, '']

    def download_file(self, filename):
        try:
            return [True, open(filename, 'r').read()]
        except:
            traceback.print_exc()
        return [False, '']

    def delete_file(self, filename):
        try:
            sys.stdout.write('delete_file %s\n' % filename)
            os.remove(filename)
            return [True, '']
        except:
            traceback.print_exc()
        return [False, '']
