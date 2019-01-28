import getpass
import os
import shutil


def setup_rstudio():
    def _get_rserver_cmd(port):        
        if shutil.which('rserver'):
            executable = 'rserver'
        else:
            raise FileNotFoundError('Can not find rserver in PATH')

        return [
            executable,
            '--www-port=' + str(port)
        ]

    return {
        'name': 'rstudio',
        'command': _get_rserver_cmd,
        'environment':  {
            'USER': getpass.getuser()
        },
        'timeout': 5
    }
