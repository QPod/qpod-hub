import os
import pwd
import shutil


def setup_code_server():
    def _get_code_server_cmd(port):
        if shutil.which('code-server'):
            executable = 'code-server'
        else:
            raise FileNotFoundError('Can not find `code-server` in PATH')

        return [
            executable,
            '--auth=none',
            '--disable-telemetry',
            '--port=' + str(port)
        ]

    return {
        'name': 'code-server',
        'command': _get_code_server_cmd,
        'environment':  {}
    }
