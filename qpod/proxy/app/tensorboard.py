import shutil


def setup_tensorboard():
    def _get_tensorboard_cmd(port):
        if shutil.which('tensorboard'):
            executable = 'tensorboard'
        else:
            raise FileNotFoundError('Can not find `tensorboard` in PATH')

        return [
            executable,
            '--port=' + str(port),
            '--logdir=/tmp/tensorboard',
            #'--path_prefix=/tensorboard/',
            '--purge_orphaned_data=true',
            '--window_title=QPod - Tensorboard'
        ]

    return {
        'name': 'tensorboard',
        'command': _get_tensorboard_cmd,
        'environment': {},
        'timeout': 5,
        'rewrite': '/'
    }
