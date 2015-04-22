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

        return self.parser.parse()

class ResourceManager(rend.Page):
    isLeaf = True

    def __init__(self, static_dir='static'):
        rend.Page.__init__(self)
        self.static_dir = static_dir
        for f in os.listdir(static_dir):
            path = os.path.join(static_dir, f)
            self.putChild(f, static.File(path))

    def parse(self):
        for file in os.listdir(self.static_dir):
            if file.endswith('~'): continue

            if os.path.isfile(os.path.join(self.static_dir, file)):
                self.putChild(file, Page(os.path.join(self.static_dir, file)))

    def renderHTTP(self, ctx):
        filename = os.path.join(self.static_dir, 'index.html')
        return open(filename, 'r').read()
