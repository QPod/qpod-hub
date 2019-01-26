import getpass
import os
import tempfile
from textwrap import dedent


def setup_shiny():
    """Manage a Shiny instance."""

    def _get_shiny_cmd(port):
        conf = dedent("""
            run_as {user};
            server {{
                listen {port};
                location / {{
                    site_dir {site_dir}/rshiny;
                    log_dir {site_dir}/rshiny/logs;
                    directory_index on;
                }}
            }}
        """).format(
            user='shiny',  #getpass.getuser(),
            port=str(port),
            site_dir=os.getcwd()
        )

        f = tempfile.NamedTemporaryFile(mode='w', delete=False)
        f.write(conf)
        f.close()
        return ['shiny-server', f.name]

    return {
        'name': 'rshiny',
        'command': _get_shiny_cmd,
        'environment': {},
        'timeout': 5
    }
