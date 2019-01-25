import jinja2
from notebook.utils import url_path_join

from .util import package_name, list_modules, get_resource

services = list(list_modules())


def _jupyter_server_extension_paths():
    # used when enabling server-extension
    return [{"module": package_name}]


def _jupyter_nbextension_paths():
    # used when enabling notebook-extension
    ret = []
    for s in services:
        for section in ['notebook', 'tree']:
            path_static = get_resource(s.module_name, folder_name='static/' + s.module_name, file_name=section + '.js')

            if path_static is None:
                continue

            ext = dict(section=section, require='%s/%s' % (s.module_name, section),
                       src='%s/static' % (s.module_name,), dest='%s/%s' % (package_name, s.module_name,))
            ret.append(ext)

    return ret


def load_jupyter_server_extension(nbapp):
    webapp = nbapp.web_app
    base_url = nbapp.base_url

    static_url_prefix = nbapp.tornado_settings.get("static_url_prefix", "static")
    static_url_prefix = url_path_join(base_url, static_url_prefix) + '/'

    template_loader = webapp.settings['jinja2_env'].loader

    def add_static_path(path_static):
        for rule in webapp.default_router.rules:
            for r in rule.target.rules:
                if r.matcher.regex.match(static_url_prefix):
                    current_static_path = r.target_kwargs.get('path', [])

                    if path_static not in current_static_path:
                        r.target_kwargs.get('path').insert(0, path_static)
                        return True
        return False

    def add_template_path(path_template):
        if isinstance(template_loader, jinja2.ChoiceLoader):
            for loader in template_loader.loaders:
                if isinstance(loader, jinja2.FileSystemLoader):
                    loader.searchpath.append(path_template)
        elif isinstance(template_loader, jinja2.FileSystemLoader):
            template_loader.searchpath.append(path_template)
        else:
            raise RuntimeError("Unknown Template Handler [%s]!" % template_loader)

    for s in services:
        # Handler Static files, make sure our static files are available
        p_static = get_resource(s.module_name, 'static')
        if p_static:
            add_static_path(p_static)
            p_static in webapp.settings['nbextensions_path'] or webapp.settings['nbextensions_path'].append(p_static)

        # Handler Template files, make sure application find templates in right folders
        p_template = get_resource(s.module_name, 'templates')
        if p_template and p_template not in nbapp.extra_template_paths:
            add_template_path(p_template)

        # Add Service Handlers
        if s.module_server_handler:
            webapp.add_handlers(".*$", [(url_path_join(base_url, h[0]), *h[1:]) for h in s.module_server_handler])
            nbapp.log.info('Service Loaded: %s' % s.module_name)
        else:
            nbapp.log.info('Service Skipped (no service found): %s' % s.module_name)

    # Change the `default_url` of the WebAPP
    default_url = '/home'
    webapp.settings['default_url'] = '/'
    from tornado.web import RedirectHandler
    from notebook.base.handlers import RedirectWithParams
    for rule in webapp.default_router.rules:
        for r in rule.target.rules:
            if r.target == RedirectWithParams and 'url' in r.target_kwargs:
                if not default_url.startswith(base_url):
                    default_url = url_path_join(base_url, default_url)
                r.target_kwargs['url'] = default_url
            elif r.target == RedirectHandler and 'url' in r.target_kwargs:
                r.target_kwargs['url'] = url_path_join(base_url, r.target_kwargs['url'])
