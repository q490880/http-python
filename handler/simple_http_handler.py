# encoding = utf-8
from urllib import parse

from handler.base_http_handler import BaseHTTPRequestHandler


class SimpleHTTPRequestsHandler(BaseHTTPRequestHandler):
    def __init__(self, server, request, client_address):
        BaseHTTPRequestHandler.__init__(self, server, request, client_address)

    def do_GET(self):
        pass

    def do_POST(self):
        pass

    def get_resources(self, path):
        url_result = parse.urlparse(path)