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
        self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        self.parser.add_option('-p', '--port', help='Set TCP Port number for web server', type='int', default=8000, dest='port')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        directory = options.directory
        port = options.port

        if directory is None:
            directory = os.path.join(wasanbon.home_path, 'web', 'applications')
        
        sys.stdout.write('# Starting Web Application in %s\n' % directory)

        from nevow import appserver
        from twisted.web import server
        from twisted.internet import reactor
        
        from site import resource
        from rpc import manager
        
        #self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        #options, argv = self.parse_args(args[:])
        #verbose = options.verbose_flag # This is default option
        #force   = options.force_flag


        #if directory is None:
        #    directory = os.path.join(__path__[0], 'www')
        if not os.path.isdir(directory):
            directory = os.path.join(os.getcwd(), directory)
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
        #packdir = os.path.join(__path__[0], directory)
        if not os.path.isdir(directory):
            os.mkdir(directory)
        package_names = []
        for f in os.listdir(directory):
            if f.endswith('.zip'):
                package_names.append(f[0:-4])

        return package_names

    def get_applications(self, appdist):
        """ List applications """

        if not os.path.isdir(appdist):
            os.mkdir(appdist)
        package_names = []
        for f in os.listdir(appdist):

            path = os.path.join(appdist, f)
            if os.path.isdir(path):
                package_names.append(f)
        return package_names


    @manifest
    def packages(self, args):
        self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        directory = options.directory
        if directory is None:
            directory = os.path.join(__path__[0], 'packages')

        package_names = self.get_packages(directory)
        sys.stdout.write('# Install ready packages:\n')
        for p in package_names:
            sys.stdout.write(' - %s\n' % p)
        return 0

    @manifest
    def applications(self, args):
        self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        appdist = options.directory
        if appdist is None:
            appdist = os.path.join(wasanbon.home_path, 'web', 'applications')

        package_names = self.get_applications(appdist)
        sys.stdout.write('# Installed Applications:\n')
        for p in package_names:
            sys.stdout.write(' - %s\n' % p)
        return 0
        
    @manifest
    def install(self, args):
        """ install application """
        self.parser.add_option('-d', '--directory', help='Set Package Archive Directory Root', default=None, dest='directory')
        self.parser.add_option('-t', '--target', help='Set Application File Directory Root', default=None, dest='target')
        self.parser.add_option('-i', '--input', help='Set Input Package name', default=None, dest='input')
        self.parser.add_option('-f', '--force', help='Force install', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(args[:], self._print_alternative_packages)
        verbose = options.verbose_flag # This is default option
        package_dir = options.directory
        if package_dir == None:
            package_dir = os.path.join(__path__[0], 'packages')

        wasanbon.arg_check(argv, 4)
        app_name = argv[3]
        if app_name.endswith('.zip'):
            app_name = app_name[:-4]


        appdist = options.target
        if appdist is None:
            appdist = os.path.join(wasanbon.home_path, 'web', 'applications')

        package_path = options.input
        if package_path is None:
            package_path = os.path.join(package_dir, app_name +'.zip')

        force = options.force_flag

        package_names = self.get_packages(package_dir)
        application_names = self.get_applications(appdist)


        if not os.path.isfile(package_path):
            sys.stdout.write('# Can not find package.\n')

        # Check if Web Application is already installed or not
        #if not app_name in package_names:
        #    sys.stdout.write('''# Argument '%s' is not ready to install.\n
        # Place .zip package file in the packages package_dir in %s''' % (app_name, package_dir))
        #    return -1

        # Check if Web Application is already installed or not
        if app_name in application_names:
            sys.stdout.write('''# '%s' is already installed.\n''' % (app_name))

            if not force:
                sys.stdout.write('# Add -f option to force installing.\n')
                return -1
            
            

        sys.stdout.write('# Installing %s.\n' % (app_name))

        import zipfile
        z = zipfile.ZipFile(package_path)

        cwd = os.getcwd()
        os.chdir(appdist)

        for n in z.namelist():
            if verbose:
                sys.stdout.write(' - %s\n' % n)
            z.extract(n)


        os.chdir(cwd)
        return 0
