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
            '--bind-addr=0.0.0.0:{port}'.format(port=port),
            '/root/'
        ]

    return {
        'name': 'code-server',
        'command': _get_code_server_cmd,
        'environment':  {}
    }
