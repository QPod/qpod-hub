from datetime import tzinfo, timedelta, datetime


class tzUTC(tzinfo):
    """tzinfo object for UTC (zero offset)"""
    ZERO = timedelta(0)  # constant for zero offset

    def utcoffset(self, d):
        return tzUTC.ZERO

    def dst(self, d):
        return tzUTC.ZERO


def utcnow():
    return datetime.utcnow().replace(tzinfo=tzUTC())


def url_path_join(*pieces):
    """Join components of url into a relative url
    Use to prevent double slash when joining subpath. This will leave the
    initial and final / in place
    """
    initial = pieces[0].startswith('/')
    final = pieces[-1].endswith('/')
    stripped = [s.strip('/') for s in pieces]
    result = '/'.join(s for s in stripped if s)
    if initial:
        result = '/' + result
    if final:
        result = result + '/'
    if result == '//':
        result = '/'
    return result


def call_with_asked_args(callback, args):
    """
    Call callback with only the args it wants from args
    Example
    >>> def cb(a):
    ...    return a * 5
    >>> print(call_with_asked_args(cb, {'a': 4, 'b': 8}))
    20
    """
    # FIXME: support default args
    # FIXME: support kwargs
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
