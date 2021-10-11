from jupyter_server_proxy.config import _make_serverproxy_handler
from jupyter_server_proxy.handlers import LocalProxyHandler, AddSlashHandler

from .handlers import ServersInfoHandler
from .app import apps


def make_serverproxy_handler(name, command, environment=None, timeout=30, absolute_url=False, \
    port=0, mappath=None, request_headers_override=None, *args, **kwargs):
    return _make_serverproxy_handler(name, command, environment or {}, timeout, absolute_url, \
        port, mappath, request_headers_override or {}, *args, **kwargs)


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
    (r'/proxy/(\d+)(.*)', LocalProxyHandler, {'absolute_url': False}),
    (r'/proxy/absolute/(\d+)(.*)', LocalProxyHandler, {'absolute_url': True})
]
