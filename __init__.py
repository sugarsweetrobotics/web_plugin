import os, sys
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']

    @manifest
    def start(self, args):
        """ Start Web Server """
        self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        self.parser.add_option('-p', '--port', help='Set TCP Port number for web server', type='int', default=8080, dest='port')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        directory = options.directory
        from nevow import appserver
        from twisted.web import server
        from twisted.internet import reactor
        
        from site import resource
        from rpc import manager
        
        #self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        #force   = options.force_flag
        work_directory = 'workspace'
        port = options.port
        if directory is None:
            directory = os.path.join(__path__[0], 'default')
        elif not os.path.isdir(directory):
            directory = os.path.join(os.getcwd(), directory)
            if not os.path.isdir(directory):
                raise wasanbon.InvalidArgumentException()

        res = resource.ResourceManager(directory)
        res.putChild('RPC', manager.RpcManager(directory=work_directory));
        site = appserver.NevowSite(res)
        reactor.listenTCP(port, site)
        reactor.run()
