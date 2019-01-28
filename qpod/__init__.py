import inspect
import sys

self = sys.modules[__name__]

entry_from_jupyter = False
for stack in inspect.stack()[::-1]:
    if 'jupyter' in stack.filename:
        entry_from_jupyter = True
        break

if entry_from_jupyter:
    print(' @ Entry from Jupyter...')
    from notebook.base.handlers import IPythonHandler as RequestHandler
    from .server_jupyter import _jupyter_nbextension_paths, _jupyter_server_extension_paths, \
        load_jupyter_server_extension
    setattr(self, 'RequestHandler', RequestHandler)  # Stub
else:
    print(' @ Entry from this app...')
    from .base.handlers import MainRequestHandler as RequestHandler
    from .server_main import main
    setattr(self, 'RequestHandler', RequestHandler)  # Stub

