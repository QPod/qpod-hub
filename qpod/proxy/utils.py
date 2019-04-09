import asyncio
import concurrent.futures
import inspect
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
    Use to prevent double slash when joining subpath. This will leave the initial and final / in place
    """
    stripped = [s.strip('/') for s in pieces]
    result = '/'.join(s for s in stripped if s)
    if pieces[0].startswith('/'):
        result = '/' + result
    if pieces[-1].endswith('/'):
        result = result + '/'
    if result == '//':
        result = '/'
    return result


def maybe_future(obj):
    """Like tornado's deprecated gen.maybe_future but more compatible with asyncio for recent versions of tornado
    """
    if inspect.isawaitable(obj):
        return asyncio.ensure_future(obj)
    elif isinstance(obj, concurrent.futures.Future):
        return asyncio.wrap_future(obj)
    else:
        # not awaitable, wrap scalar in future
        f = asyncio.Future()
        f.set_result(obj)
        return f
