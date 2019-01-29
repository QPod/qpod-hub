from .handlers import SuperviseAndProxyHandler


def call_with_asked_args(callback, args):
    """
    Call callback with only the args it wants from args
    Example
    >>> def cb(a):
    ...    return a * 5
    >>> print(call_with_asked_args(cb, {'a': 4, 'b': 8}))
    20
    """
    # FIXME: support default args and kwargs
    # co_varnames contains both args and local variables, in order.
    # We only pick the local variables
    asked_arg_names = callback.__code__.co_varnames[:callback.__code__.co_argcount]
    asked_arg_values = []
    missing_args = []
    for asked_arg_name in asked_arg_names:
        if asked_arg_name in args:
            asked_arg_values.append(args[asked_arg_name])
        else:
            missing_args.append(asked_arg_name)
    if missing_args:
        raise TypeError(
            '{}() missing required positional argument: {}'.format(
                callback.__code__.co_name,
                ', '.join(missing_args)
            )
        )
    return callback(*asked_arg_values)


def make_serverproxy_handler(name, command, environment, timeout=5, rewrite='/'):
    """Create a SuperviseAndProxyHandler subclass with given parameters"""

    # FIXME: Set 'name' properly
    class _Proxy(SuperviseAndProxyHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.name = name
            self.proxy_base = name
            self.rewrite = rewrite

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
