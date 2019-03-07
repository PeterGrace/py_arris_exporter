"""The primary module for this skeleton application."""
import logging
from http.server import HTTPServer
from .server import Server

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger('main')


def main():
    httpd = HTTPServer(('0.0.0.0', 9393), Server)
    log.info("Starting http server.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    main()
