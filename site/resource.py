import os
import twisted
from nevow import static, rend, loaders
from nevow import tags as T
from parser import Parser

CSS_DIR='static/css'
HTML_DIR='static/html'
JS_DIR='static/js'
MEDIA_DIR='static/media'

def document_factory(file):
    parser = Parser(file)
    return loaders.htmlstr(
        parser.parse()
    );
    

class Page(rend.Page):
    def __init__(self, file):
        self.file = file
        self.parser = Parser(file)

    def renderHTTP(self, context):
        print 'Context:', context
        return self.parser.parse()

class ResourceManager(rend.Page):
    isLeaf = True
    __except_dir = ['js', 'index.css']
    def __init__(self, static_dir='static'):
        rend.Page.__init__(self)
        self.static_dir = static_dir
        #self.putChild('index.css', static.File(os.path.join(static_dir, 'index.css')))
        for f in os.listdir(static_dir):
            if f.endswith('~'):
                continue
            path = os.path.join(static_dir, f)
            self.putChild(f, static.File(path))
            if not f in self.__except_dir:                
                self._index += """
<a href="%s" target="new">
<li class="plugin_item">
<h1>%s</h1>
</li>
</a>
""" % (f, f)

        self._index += """
  </ul>
  </div>
</body></html>"""

    _index = """
<html>
<head>
  <title>Wasanbon Web System</title>
  <script type="text/javascript" src="js/jquery-1.11.0.min.js"></script>
  <script type="text/javascript" src="js/jquery-ui-1.10.4.min.js"></script>
  <link rel="stylesheet" href="index.css" type="text/css"></link>
</head>
<body id="content">
  <div id="topbar">
  </div>
  <div id="top">
    <h1>wasanbon web server</h1>
    <p>Framework for Robotic Technology System</p>
  </div>
  <div id="container">
  <ul class="plugin_items">
"""

    def parse(self):
        for file in os.listdir(self.static_dir):
            if file.endswith('~'): continue

            if os.path.isfile(os.path.join(self.static_dir, file)):
                self.putChild(file, Page(os.path.join(self.static_dir, file)))

    def renderHTTP(self, ctx):
        return self._index
        #filename = os.path.join(self.static_dir, 'index.html')
        #return open(filename, 'r').read()
        
