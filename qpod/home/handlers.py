import os
import shutil
from datetime import datetime

from tornado import web
from .. import RequestHandler



try:
    t_build = os.path.getmtime(__file__)
    t_build = datetime.fromtimestamp(t_build).strftime('%Y-%m-%d %H:%M:%S')
except:
    t_build = 'Unknown'  # a string to represent last build of this package


def if_exist(cmd):
    cmd = shutil.which(cmd)
    return cmd is not None


class HomepageHandler(RequestHandler):
    @web.authenticated
    def get(self):
        tpl = self.render_template(
            'home/index.html',
            last_update=t_build,
            exist_jupyterlab=if_exist('jupyter-lab'),
            exist_jupyter_notebook=if_exist('jupyter-notebook'),
            exist_code_server=if_exist('code-server'),
            exist_tensorboard=if_exist('tensorboard'),
            exist_rserver=if_exist('rserver'),
            exist_rshiny=if_exist('shiny-server'),
        )
        self.write(tpl)
