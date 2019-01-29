from .config import make_serverproxy_handler
from .handlers import ServersInfoHandler, LocalProxyHandler, AddSlashHandler
from .app import apps

from collections import namedtuple


ServerProcess = namedtuple('ServerProcess', ('name', 'command', 'environment', 'timeout'))
server_proccesses = [ServerProcess(**a) for a in apps]


def make_handlers(server_processes):
    """Get tornado handlers for registered server_processes"""
    _handlers = []
    for sp in server_processes:
        handler = make_serverproxy_handler(
            sp.name, sp.command, sp.environment, sp.timeout,
        )
        _handlers.extend([
            (r'/%s/(.*)' % sp.name, handler, dict(state={})),
            (r'/%s' % sp.name, AddSlashHandler)
        ])

    return _handlers


server_handlers = make_handlers(server_proccesses)
default_handlers = server_handlers + [
    (r'/server-proxy/servers-info', ServersInfoHandler, {'server_processes': server_proccesses}),
    (r'/proxy/(\d+)(.*)', LocalProxyHandler)
]
