import os
import pkgutil
import sys
from collections import namedtuple

package_name = __name__.split('.')[0]
package_self = sys.modules[package_name]

service = namedtuple('service', ['module_name', 'module_server_handler'])


def get_resource(module_name, folder_name=None, file_name=None):
    path_module = os.path.join(os.path.dirname(__file__), module_name, folder_name or '')
    path_folder = os.path.normpath(path_module)
    if file_name is None:
        return None if not os.path.isdir(path_folder) else path_module
    else:
        path_file = os.path.join(path_folder, file_name)
        path_file = os.path.normpath(path_file)
        return None if not os.path.isfile(path_file) else path_file


def list_modules(package=package_self, exclude=()):
    path = os.path.dirname(package.__file__)
    for importer, module_name, is_pkg in pkgutil.iter_modules([path]):
        if not is_pkg or module_name in exclude:
            continue  # only scan those sub-modules in folders with a `__init__` file

        mod = __import__(package_name + "." + module_name, fromlist=['default_handlers'])
        module_server_handler = getattr(mod, 'default_handlers', [])

        yield service(module_name, module_server_handler)
