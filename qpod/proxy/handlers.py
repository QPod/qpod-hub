from tornado import web

from .. import RequestHandler

class ServersInfoHandler(RequestHandler):
    def initialize(self, server_processes):
        self.server_processes = server_processes

    @web.authenticated
    async def get(self):
        data = []
        # Pick out and send only metadata
        # Don't send anything that might be a callable, or leak sensitive info
        for sp in self.server_processes:
            # Manually recurse to convert namedtuples into JSONable structures
            data.append({
                'name': sp.get('name', 'Unknown')
            })

        self.write({'server_processes': data})
