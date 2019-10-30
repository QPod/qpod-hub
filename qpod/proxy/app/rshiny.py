import os
import pwd
import tempfile
from textwrap import dedent


def setup_shiny():
    """Manage a Shiny instance."""

    def _get_shiny_cmd(port):
        site_dir = os.getcwd() + '/rshiny'
        os.makedirs(site_dir, exist_ok=True)

        conf = dedent("""
            run_as :HOME_USER: {user};
            server {{
                listen {port};
                location / {{
                    site_dir {site_dir};
                    log_dir {site_dir}/logs;
                    directory_index on;
                }}
            }}
        """).format(
            user=pwd.getpwuid(os.getuid())[0],  # 'shiny'
            port=str(port),
            site_dir=site_dir
        )

        f = tempfile.NamedTemporaryFile(mode='w', delete=False)
        f.write(conf)
        f.close()
        return ['shiny-server', f.name]

    return {
        'name': 'rshiny',
        'command': _get_shiny_cmd,
        'environment': {}
    }
