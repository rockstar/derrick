import glob
import json
import mimetypes
import os

from twisted.web.resource import Resource


FAVICON = 'GIF89a\x01\x00\x01\x00\xf0\x00\x00\xff\xff\xff\x00\x00\x00!' \
          '\xff\x0bXMP DataXMP\x02?x\x00!\xf9\x04\x05\x00\x00\x00\x00,' \
          '\x00\x00\x00\x00\x01\x00\x01\x00@\x02\x02D\x01\x00;'


class DerrickRootResource(Resource):

    isLeaf = True

    blacklist = ['tools']

    def __init__(self, root='.'):
        self.root = os.path.abspath(root)

    def _save(self):
        pass

    def _browse(self):
        pass

    def _glob(self):
        pass

    def render_GET(self, request):
        path = request.path

        if path == '/':
            path = 'index.html'
        elif path == '/editor':
            path = 'weltmeister.html'
        elif path == '/lib/weltmeister/api/glob.php':
            globs = request.args.get('glob[]', None)
            if not globs:
                request.setResponseCode(503)
                return 'globs[] not set'

            files = []
            for _glob in globs:
                # TODO: Don't let you do '..' for security
                _files = glob.glob(_glob)
                files.extend(_files)
            return json.dumps(files)
        elif request.path == '/lib/weltmeister/api/browse.php':
            top_dir = request.args.get('dir')
            if not top_dir:
                request.setResponseCode(404)
                return ''
            # TODO: Don't let you do '..' for security
            top_dir = top_dir[0]
            dirs = [os.path.join(top_dir, d)
                    for d in os.listdir(os.path.join(self.root, top_dir))
                    if os.path.isdir(os.path.join(top_dir, d))]
            files = glob.glob(os.path.join(top_dir, '*.*'))

            if 'type' in request.args:
                types = request.args.get('type')[0]
                if 'scripts' in types:
                    files = [f for f in files if os.path.splitext(f)[1] == '.js']

            request.setResponseCode(200)
            return json.dumps({
                'files': files,
                'dirs': dirs,
                'parent': False if top_dir == './' else os.path.dirname(top_dir)
            })

        # Trim the leading forward slash
        if path[0] == '/':
            path = path[1:]
        for bad in self.blacklist:
            if path.startswith(bad):
                request.setResponseCode(404)
                return ''

        # TODO: Don't let you do '..' for security

        path = os.path.join(self.root, path)

        try:
            with open(path, 'rb') as f:
                data = f.read()

            content_type = mimetypes.guess_type(path)[0]

            request.setHeader('Content-Type', content_type)
            request.setResponseCode(200)
            return data
        except IOError:
            if 'favicon.ico' in path:
                request.setHeader('Content-Type', 'image/gif')
                request.setResponseCode(200)
                return FAVICON
            else:
                request.setResponseCode(404)
                return None

    def render_POST(self, request):
        if request.path == '/lib/weltmeister/api/save.php':
            path = request.args.get('path', None)
            data = request.args.get('data', None)
            if not path or not data:
                request.setResponseCode(503)
                return json.dumps({'error': 1, 'msg': 'No data or path'})

            # TODO: Don't let you do '..' for security
            path = path[0]
            data = data[0]

            open(path, 'w').write(data)
            request.setResponseCode(200)
            return json.dumps({'error': 0})
        else:
            request.setResponseCode(405)
            return 'Method not allowed'
