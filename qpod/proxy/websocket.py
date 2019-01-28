"""
Authenticated HTTP proxy, Some original inspiration from https://github.com/senko/tornado-proxy
"""

import inspect
from tornado import httpclient, httputil, websocket, ioloop, version_info


class PingableWSClientConnection(websocket.WebSocketClientConnection):
    """A WebSocketClientConnection with an on_ping callback."""
    def __init__(self, **kwargs):
        if 'on_ping_callback' in kwargs:
            self._on_ping_callback = kwargs['on_ping_callback']
            del (kwargs['on_ping_callback'])
        super().__init__(**kwargs)

    def on_ping(self, data):
        if self._on_ping_callback:
            self._on_ping_callback(data)


def pingable_ws_connect(request=None, on_message_callback=None, on_ping_callback=None):
    """
    A variation on websocket_connect that returns a PingableWSClientConnection
    with on_ping_callback.
    """
    # Copy and convert the headers dict/object (see comments in AsyncHTTPClient.fetch)
    request.headers = httputil.HTTPHeaders(request.headers)
    request = httpclient._RequestProxy(request, httpclient.HTTPRequest._DEFAULTS)

    if version_info[0] == 4:  # for tornado 4.5.x compatibility
        conn = PingableWSClientConnection(
            request=request,
            on_message_callback=on_message_callback,
            on_ping_callback=on_ping_callback,
            io_loop=ioloop.IOLoop.current(),
        )
    else:
        conn = PingableWSClientConnection(
            request=request,
            on_message_callback=on_message_callback,
            on_ping_callback=on_ping_callback,
            max_message_size=getattr(websocket, '_default_max_message_size', 10 * 1024 * 1024)
        )

    return conn.connect_future


# https://stackoverflow.com/questions/38663666/how-can-i-serve-a-http-page-and-a-websocket-on-the-same-url-in-tornado
class WebSocketHandlerMixin(websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # calling the super() constructor since the parent doesn't keep
        bases = inspect.getmro(type(self))
        assert WebSocketHandlerMixin in bases
        meindex = bases.index(WebSocketHandlerMixin)
        try:
            nextparent = bases[meindex + 1]
        except IndexError:
            raise Exception("WebSocketHandlerMixin should be followed by another parent to make sense")

        # un-disallow methods --- t.ws.WebSocketHandler disallows methods, re-enable these methods
        def wrapper(method):
            def un_disallow(*args2, **kwargs2):
                getattr(nextparent, method)(self, *args2, **kwargs2)

            return un_disallow

        for method in ["write", "redirect", "set_header", "set_cookie",
                       "set_status", "flush", "finish"]:
            setattr(self, method, wrapper(method))
        nextparent.__init__(self, *args, **kwargs)

    async def get(self, *args, **kwargs):
        if self.request.headers.get("Upgrade", "").lower() != 'websocket':
            return await self.http_get(*args, **kwargs)
        # super get is not async
        super().get(*args, **kwargs)
