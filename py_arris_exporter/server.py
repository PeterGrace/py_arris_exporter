import logging

from http.server import BaseHTTPRequestHandler
from .handler import process

log = logging.getLogger('main')

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        pass
    def do_GET(self):
        self.respond()

    def handle_http(self, status, body):
        self.send_response(status)
        self.send_header('Content-type', 'text/plain;charset=UTF-8')
        self.end_headers()
        return bytes(body, "UTF-8")


    def respond(self):
        data = process()
        content = self.handle_http(200, data)
        try:
            self.wfile.write(content)
        except Exception as e:
            log.error("Exception when trying to write to socket: %s" % (e))
