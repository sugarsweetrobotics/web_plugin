import os, sys
import WSB
from plugin import *

class AdminPlugin(PluginObject):

    def __init__(self):
        PluginObject.__init__(self, 'admin')

    def repository_list(self):
        res = WSB.getPackageRepositoryList()
        return [True, res]

    def repository_clone(self, pkg):
        res = WSB.clonePackage(pkg)
        return [True, res]


    def package_list(self):
        res = WSB.getPackages()
        return [True, (res)]

    def package_delete(self, pkg):
        res = WSB.deletePackage(pkg)
        return [True, res]
