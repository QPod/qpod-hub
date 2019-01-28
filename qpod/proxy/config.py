from .handlers import SuperviseAndProxyHandler
from .utils import call_with_asked_args


def make_serverproxy_handler(name, command, environment, timeout=5):
    """Create a SuperviseAndProxyHandler subclass with given parameters"""

    # FIXME: Set 'name' properly
    class _Proxy(SuperviseAndProxyHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.name = name

        @property
        def process_args(self):
            return {
                'port': self.port,
                'base_url': self.base_url,
            }

        def _render_template(self, value):
            args = self.process_args
            if type(value) is str:
                return value.format(**args)
            elif type(value) is list:
                return [self._render_template(v) for v in value]
            elif type(value) is dict:
                return {
                    self._render_template(k): self._render_template(v)
                    for k, v in value.items()
                }
            else:
                raise ValueError('Value of unrecognized type {}'.format(type(value)))

        def get_cmd(self):
            if callable(command):
                return self._render_template(call_with_asked_args(command, self.process_args))
            else:
                return self._render_template(command)

        def get_env(self):
            if callable(environment):
                return self._render_template(call_with_asked_args(environment, self.process_args))
            else:
                return self._render_template(environment)

        def get_timeout(self):
            return timeout

    return _Proxy
