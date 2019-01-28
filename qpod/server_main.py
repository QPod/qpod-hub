import uuid

import jinja2
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application, RedirectHandler

from .base.handlers import MainRequestHandler, FileFindHandler
from .util import get_resource, list_modules, package_name

services = list(list_modules())


class AuthHandler(MainRequestHandler):
    def get(self):
        url = self.request.uri
        if url.startswith('/login'):
            self.log_in()
        elif url.startswith('logout'):
            self.log_out()

    def log_out(self):
        self.clear_cookie(self.cookie_name)
        message = {'info': 'Successfully logged out.'}
        self.write(self.render_template('logout.html', message=message))

    def log_in(self):
        self.set_secure_cookie(self.cookie_name, uuid.uuid4().hex)
        next_url = self.get_argument('next', default='')
        self.redirect(next_url)


define("port", default=8888, help="Run Service on the given port", type=int)


def main():
    handlers = [
        (r"/", RedirectHandler, {"url": "/home"}),
        (r"/logout", AuthHandler),
        (r"/login", AuthHandler)
    ]

    path_templates = []
    path_static = []

    for mod_name, mod_handlers in services:
        p_template, p_static = get_resource(mod_name, 'templates'), get_resource(mod_name, 'static')

        if p_template is not None:
            path_templates.append(p_template)
        if p_static is not None:
            path_static.append(p_static)

        handlers.extend(mod_handlers)

    app = Application(
        handlers,
        login_url='/login',
        default_url='/home',
        cookie_secret=package_name,
        static_path=path_static,
        # static_url_prefix='',
        static_handler_class=FileFindHandler,
        static_handler_args={},
        debug=True
    )
    app.jinja2_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path_templates),
        autoescape=True
    )

    app.listen(options.port)
    print("Service Standalone service running at port:", options.port)
    IOLoop.instance().start()
