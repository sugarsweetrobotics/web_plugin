import os, sys
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):
    """ Plugin for Web interface """
    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def _print_alternative_packages(self, argv):
        packages = self.get_packages()
        for p in packages:
            sys.stdout.write('%s\n' % p)
        return 0
        
    def depends(self):
        return ['admin.environment']

    @manifest
    def start(self, args):
        """ Start Web Server """
        self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default='applications', dest='directory')
        self.parser.add_option('-p', '--port', help='Set TCP Port number for web server', type='int', default=8000, dest='port')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        directory = options.directory


        from nevow import appserver
        from twisted.web import server
        from twisted.internet import reactor
        
        from site import resource
        from rpc import manager
        
        #self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        #options, argv = self.parse_args(args[:])
        #verbose = options.verbose_flag # This is default option
        #force   = options.force_flag

        port = options.port
        if directory is None:
            directory = os.path.join(__path__[0], 'www')
        elif not os.path.isdir(directory):
            directory = os.path.join(__path__[0], directory)
            print directory
            if not os.path.isdir(directory):
                raise wasanbon.InvalidArgumentException()
        work_directory = directory

        res = resource.ResourceManager(directory)
        res.putChild('RPC', manager.RpcManager(directory=work_directory));
        site = appserver.NevowSite(res)
        reactor.listenTCP(port, site)
        reactor.run()
        return 0


    def get_packages(self, directory='packages'):
        """ List packages """
        packdir = os.path.join(__path__[0], directory)
        if not os.path.isdir(packdir):
            os.mkdir(packdir)
        package_names = []
        for f in os.listdir(packdir):
            if f.endswith('.zip'):
                package_names.append(f[0:-4])

        return package_names

    def get_applications(self, directory='applications'):
        """ List applications """
        appdist = os.path.join(__path__[0], directory)
        if not os.path.isdir(appdist):
            os.mkdir(appdist)
        package_names = []
        for f in os.listdir(appdist):
            path = os.path.join(packdir, f)
            if 'index.html' in os.listdir(path):
                package_names.append(f)
        return package_names


    @manifest
    def packages(self, args):
        self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default='packages', dest='directory')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        directory = options.directory

        package_names = self.get_packages(directory)
        sys.stdout.write('# Install ready packages:\n')
        for p in package_names:
            sys.stdout.write(' - %s\n' % p)
        return 0

    @manifest
    def applications(self, args):
        self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default='packages', dest='directory')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        directory = options.directory

        package_names = self.get_applications(directory)
        sys.stdout.write('# Installed Applications:\n')
        for p in package_names:
            sys.stdout.write(' - %s\n' % p)
        return 0
        
    @manifest
    def install(self, args):
        """ install application """
        self.parser.add_option('-d', '--directory', help='Set Package Archive Directory Root', default='packages', dest='directory')
        self.parser.add_option('-t', '--target', help='Set Application File Directory Root', default='applications', dest='target')
        self.parser.add_option('-f', '--force', help='Force install', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(args[:], self._print_alternative_packages)
        verbose = options.verbose_flag # This is default option
        directory = options.directory
        target = options.target
        force = options.force_flag

        package_names = self.get_packages(directory)
        application_names = self.get_applications(target)

        wasanbon.arg_check(argv, 4)
        if not argv[3] in package_names:
            sys.stdout.write('''# Argument '%s' is not ready to install.\n
# Place .zip package file in the packages directory in %s
''' % (argv[3], __path__[0]))
            return -1
        
        if argv[3] in application_names:
            sys.stdout.write('''# '%s' is already installed.\n''' % (argv[3]))

            if not force:
                sys.stdout.write('# Add -f option to force installing.\n')
                return -1

        sys.stdout.write('# Installing %s.\n' % (argv[3]))
        cwd = os.getcwd()
        os.chdir(os.path.join(__path__[0], target))

        package_path = os.path.join(__path__[0], directory, argv[3] +'.zip')
        import zipfile
        z = zipfile.ZipFile(package_path)
        for n in z.namelist():
            z.extract(n)
        
        return 0
