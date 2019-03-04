from .config import make_serverproxy_handler
from .handlers import ServersInfoHandler, LocalProxyHandler, AddSlashHandler
from .app import apps


def make_handlers(server_processes):
    """Get tornado handlers for registered server_processes"""
    _handlers = []
    for sp in server_processes:
        handler = make_serverproxy_handler(**sp)
        name = sp.get('name')
        _handlers.extend([
            (r'/%s(/.*)' % name, handler, dict(state={})),
            (r'/%s' % name, AddSlashHandler)
        ])
    return _handlers

server_handlers = make_handlers(apps)
default_handlers = server_handlers + [
    (r'/server-proxy/servers-info', ServersInfoHandler, {'server_processes': apps}),
    (r'/proxy/(\d+)(.*)', LocalProxyHandler)
]
