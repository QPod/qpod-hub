import os
import re
import logging

from tornado import web
from tornado.log import app_log
from traitlets.config import Application


class MainRequestHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(MainRequestHandler, self).__init__(*args, **kwargs)
        self.base_url = ''

    @property
    def log(self):
        if Application.initialized():
            return Application.instance().log
        else:
            return app_log

    def render_template(self, name, **ns):
        template = self.application.jinja2_env.get_template(name)
        return template.render(static_url=self.static_url, **ns)  # static_url required by jinja2 template render

    @property
    def cookie_name(self):
        non_alphanum = re.compile(r'[^A-Za-z0-9]')
        return non_alphanum.sub('-', 'username-{}'.format(
            self.request.host
        ))

    def get_current_user(self):
        return self.get_secure_cookie(self.cookie_name)


class FileFindHandler(web.StaticFileHandler):
    """subclass of StaticFileHandler for serving files from a search path"""

    # cache search results, don't search for files more than once
    _static_paths = {}

    def set_headers(self):
        super(FileFindHandler, self).set_headers()
        # disable browser caching, rely on 304 replies for savings
        if "v" not in self.request.arguments or \
                any(self.request.path.startswith(path) for path in self.no_cache_paths):
            self.set_header("Cache-Control", "no-cache")

    def initialize(self, path, default_filename=None, no_cache_paths=None):
        self.default_filename = default_filename
        self.no_cache_paths = no_cache_paths or []

        path = [path] if isinstance(path, str) else path

        self.root = tuple(
            os.path.abspath(os.path.expanduser(p)) + os.sep for p in path
        )

    @classmethod
    def get_absolute_path(cls, roots, path):
        """locate a file to serve on our static file search path"""
        with cls._lock:
            if path in cls._static_paths:
                return cls._static_paths[path]

            ret = ''  # return empty string if file not found
            for root in roots:
                name_test = os.path.join(root, path)
                if os.path.isfile(name_test):   # file found
                    ret = os.path.abspath(name_test)
                    cls._static_paths[path] = ret

            return ret

    def validate_absolute_path(self, root, absolute_path):
        """check if the file should be served (raises 404, 403, etc.)"""
        if absolute_path == '':
            raise web.HTTPError(404)

        for root in self.root:
            if (absolute_path + os.sep).startswith(root):
                break

        return super(FileFindHandler, self).validate_absolute_path(root, absolute_path)
