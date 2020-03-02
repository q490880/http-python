# encoding=utf-8
import socket
import threading

import time

from handler.base_handler import StreamRequestHandler
from handler.base_http_handler import BaseHTTPRequestHandler
from server.http_server import BaseHTTPServer
from server.socket_server import TCPServer

class BaseRequestHandler(StreamRequestHandler):
    def handle(self):
        msg = self.readline()
        print("server recive msg : %s" % msg)
        time.sleep(1)
        self.write_content(msg)
        self.send()

class SocketServerTest:

    def run_server(self):
        tcp_server = TCPServer(('127.0.0.1', 8888), BaseRequestHandler)
        tcp_server.serve_forever()

    def client_connect(self):
        client = socket.socket()
        client.connect(('127.0.0.1',8888))
        client.send(b'Hello TCPServer \r\n')
        msg = client.recv(1024)
        print('client recive msg: %s' % msg)

    def gen_clients(self, num = 10):
        clients = []
        for i in range(num):
            client_thread = threading.Thread(target=self.client_connect)
            clients.append(client_thread)
        return clients

    def run(self):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()


        clients = self.gen_clients()
        for client in clients:
            client.start()

        server_thread.join()
        for client in clients:
            client.join()


class BaseHTTPRequestHandlerTest:
    def run_server(self):
        BaseHTTPServer(('127.0.0.1',9999), BaseHTTPRequestHandler).serve_forever()

    def run(self):
        self.run_server()

if __name__ == '__main__':
    testServer = BaseHTTPRequestHandlerTest()
    testServer.run()