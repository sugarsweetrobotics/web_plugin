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

    def sigusr1_isr(self, signal, stack):
        from twisted.internet import reactor

    def sigint_isr(self, signal, stack):
        sys.stdout.write(' - SIGINT captured.\n')
        from twisted.internet import reactor
        reactor.stop()
    

    @manifest
    def start(self, args):
        """ Start Web Server """
        self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        self.parser.add_option('-p', '--port', help='Set TCP Port number for web server', type='int', default=8000, dest='port')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        directory = options.directory
        port = options.port

        pid_dir = directory
        if directory is None:
            directory = os.path.join(wasanbon.home_path, 'web', 'applications')
            pid_dir = os.path.join(wasanbon.home_path, 'web')

        sys.stdout.write('# Starting Web Application in %s\n' % directory)

        if not os.path.isdir(pid_dir):
            os.mkdir(pid_dir)
        pid_file = os.path.join(pid_dir, 'pid')
        if os.path.isfile(pid_file):
            os.remove(pid_file)

        open(pid_file, 'w').write(str(os.getpid()))

        from nevow import appserver
        from twisted.web import server
        from twisted.internet import reactor
        
        from site import resource
        from rpc import manager
        
        #self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        #options, argv = self.parse_args(args[:])
        #verbose = options.verbose_flag # This is default option
        #force   = options.force_flag


        import signal
        signal.signal(signal.SIGUSR1, self.sigusr1_isr) # SIGUSR1 = 30
        signal.signal(signal.SIGINT, self.sigint_isr) # SIGUSR1 = 30

        #if directory is None:
        #    directory = os.path.join(__path__[0], 'www')
        if not os.path.isdir(directory):
            directory = os.path.join(os.getcwd(), directory)
            if not os.path.isdir(directory):
                sys.stdout.write('%s not found\n' % directory)
                #raise wasanbon.InvalidArgumentException()
                os.mkdir(directory)

        work_directory = directory
        self.res = resource.ResourceManager(directory)
        self.res.putChild('RPC', manager.RpcManager(directory=work_directory));
        self.site = appserver.NevowSite(self.res)
        reactor.listenTCP(port, self.site)
        reactor.run()
        sys.stdout.write(' - Web reactor stopped.\n')
        os.remove(pid_file)
        return 0

    @manifest
    def stop(self, args):
        """ Stop Web Server """
        self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        self.parser.add_option('-p', '--port', help='Set TCP Port number for web server', type='int', default=8000, dest='port')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        directory = options.directory
        port = options.port

        pid_dir = directory
        if directory is None:
            directory = os.path.join(wasanbon.home_path, 'web', 'applications')
            pid_dir = os.path.join(wasanbon.home_path, 'web')

        sys.stdout.write('# Stopping Web Application in %s\n' % directory)

        pid_file = os.path.join(pid_dir, 'pid')
        if not os.path.isfile(pid_file):
            sys.stdout.write(' - Server not found.\n')
            return -1
        import signal
        pid = int(open(pid_file, 'r').read())
        os.kill(pid, signal.SIGINT)

        return 0
        

    @manifest
    def restart(self, args):
        """ Restarting Web Server """
        self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        self.parser.add_option('-p', '--port', help='Set TCP Port number for web server', type='int', default=8000, dest='port')
        self.parser.add_option('-t', '--timedelay', help='Delay time for stopping server', type='int', default=0, dest='delay')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        directory = options.directory
        delay = options.delay
        port = options.port

        def _restart():
            self.stop(args)
            import time
            time.sleep(0.5)
            self.start(args)

        _restart()

        return 0
        

    def get_packages(self, directory='packages'):
        """ List packages """
        #packdir = os.path.join(__path__[0], directory)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        package_names = []
        for f in os.listdir(directory):
            if f.endswith('.zip'):
                package_names.append(f[0:-4])

        return package_names

    def get_applications(self, appdist):
        """ List applications """

        if not os.path.isdir(appdist):
            os.makedirs(appdist)
        package_names = []
        for f in os.listdir(appdist):

            path = os.path.join(appdist, f)
            if os.path.isdir(path):
                package_names.append(f)
        return package_names

    @manifest
    def package_dir(self, args):
        #self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        sys.stdout.write('%s\n' % os.path.join(__path__[0], 'packages'))
        return 0
    
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

        if app_name == 'all':
            all = True
        else:
            all = False

        force = options.force_flag

        appdist = options.target
        if appdist is None:
            appdist = os.path.join(wasanbon.home_path, 'web', 'applications')

        package_names = self.get_packages(package_dir)
        application_names = self.get_applications(appdist)

        style_file = 'index.css'
        style_file_path = os.path.join(appdist, style_file)
        if not os.path.isfile(style_file_path):
            import shutil
            shutil.copy(os.path.join(__path__[0], 'styles', style_file), style_file_path)


        def install_app(app_name):
            # Check if Web Application is already installed or not
            #if not app_name in package_names
            #    sys.stdout.write('''# Argument '%s' is not ready to install.\n
            # Place .zip package file in the packages package_dir in %s''' % (app_name, package_dir))
            #    return -1

            package_path = options.input
            if package_path is None:
                package_path = os.path.join(package_dir, app_name +'.zip')
            if not os.path.isfile(package_path):
                sys.stdout.write('# Can not find package (%s).\n' % package_path)


            # Check if Web Application is already installed or not
            if app_name in application_names:
                sys.stdout.write('''# '%s' is already installed.\n''' % (app_name))
                
                if not force:
                    sys.stdout.write('# Add -f option to force installing.\n')
                    return -1
            
                sys.stdout.write('# Removing installed %s application\n' % app_name)
                import shutil
                #os.removedirs(os.path.join(appdist, app_name))
                shutil.rmtree(os.path.join(appdist, app_name))

            sys.stdout.write('# Installing %s.\n' % (app_name))

            import zipfile
            z = zipfile.ZipFile(package_path)

            cwd = os.getcwd()
            os.chdir(appdist)

            for n in z.namelist():
                if verbose: sys.stdout.write(' - %s\n' % n)
                z.extract(n)


            os.chdir(cwd)

        if app_name == 'all':
            apps = package_names
        else:
            apps = [app_name]

        for app in apps:
            install_app(app)

        return 0

    @manifest
    def uninstall(self, args):
        """ uninstall application """
        options, argv = self.parse_args(args[:], self._print_alternative_packages)
        verbose = options.verbose_flag # This is default option
        
        package_dir = os.path.join(__path__[0], 'packages')
        appdist = os.path.join(wasanbon.home_path, 'web', 'applications')

        wasanbon.arg_check(argv, 4)

        app_name = argv[3]

        package_names = self.get_packages(package_dir)
        application_names = self.get_applications(appdist)

        style_file = 'index.css'
        style_file_path = os.path.join(appdist, style_file)
        if not os.path.isfile(style_file_path):
            import shutil
            shutil.copy(os.path.join(__path__[0], 'styles', style_file), style_file_path)

        if app_name in application_names:
            sys.stdout.write('''# Removing '%s'.\n''' % (app_name))
            
            import shutil
            #os.removedirs(os.path.join(appdist, app_name))
            shutil.rmtree(os.path.join(appdist, app_name))

        return 0
    
    @manifest
    def generate_dart_app(self, args):
        """ Start Web Server """
        #self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        #self.parser.add_option('-p', '--port', help='Set TCP Port number for web server', type='int', default=8000, dest='port')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        template_dir = os.path.join(__path__[0], 'app_template')
        app_template_name = "App Template"
        app_template_module_name = app_template_name.replace(' ', '-').lower()
        app_template_module_file_name = app_template_module_name.replace('-', '_')
        app_template_strip_name = "AppTemplate"
        app_template_dir_name = app_template_strip_name.lower()

        wasanbon.arg_check(argv, 4)
        app_name = argv[3]
        app_module_name = app_name.replace(' ', '-').lower()
        app_module_file_name = app_module_name.replace('-', '_')
        app_strip_name = ""
        for s in app_name.split(' '):
            app_strip_name = app_strip_name + s
        app_dir_name = app_strip_name.lower()
            
        sys.stdout.write('$APP_NAME       = %s\n' % app_name)
        sys.stdout.write('$APP_MODULE_NAME= %s\n' % app_module_name)
        sys.stdout.write('$APP_STRIP_NAME = %s\n' % app_strip_name)
        sys.stdout.write('$APP_DIR_NAME   = %s\n' % app_dir_name)
        
        cwd = os.getcwd()
        
        if os.path.isdir(app_dir_name):
            sys.stdout.write(' - Error. Directory %s already exists.\n' % app_dir_name)
        os.mkdir(app_dir_name)
        verbose = True

        def _replace_dir_name(src):
            src = src.replace(app_template_dir_name, app_dir_name)
            src = src.replace(app_template_module_file_name, app_module_file_name)
            return src

        def _replace_content(src):
            src = src.replace(app_template_name, app_name)
            src = src.replace(app_template_dir_name, app_dir_name)
            src = src.replace(app_template_strip_name, app_strip_name)
            src = src.replace(app_template_module_file_name, app_module_file_name)
            src = src.replace(app_template_module_name, app_module_name)
            return src
            

        def _dir_copy(src, dst):
            if verbose: sys.stdout.write(' - src is %s.\n - changing to %s\n' % (src, dst))
            os.chdir(dst)
            for s in os.listdir(src):
                src_p = os.path.join(src, s)
                if verbose: sys.stdout.write(' - parsing %s\n' % src_p)

                if os.path.isdir(src_p):
                    sys.stdout.write(' - %s is directory.\n' % src_p)
                    dir_name = _replace_dir_name(s)
                    os.mkdir(dir_name)
                    _dir_copy(src_p, dir_name)
                elif os.path.isfile(src_p):
                    sys.stdout.write(' - %s is file.\n' % src_p)
                    src_f = open(src_p, 'r')
                    dst_f = open(_replace_dir_name(s), 'w')
                    for line in src_f:
                        dst_f.write(_replace_content(line))
                    dst_f.close()

        _dir_copy(template_dir, app_dir_name)


        
        return 0
