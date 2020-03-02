# -*- encoding=utf-8 -*-
import socket
import threading


class TCPServer:

    def __init__(self, server_address, handler_class):
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HandlerClass = handler_class
        self.is_shutdown = False

    # 启动服务器
    def serve_forever(self):
        self.socket.bind(self.server_address)
        self.socket.listen(10)
        while not self.is_shutdown:
            request, client_address = self.get_request()
            try:
                self.process_request(request, client_address)
            except Exception as e:
                print(e)

    # 接收请求
    def get_request(self):
        return self.socket.accept()

    # 处理请求
    def process_request(self, request, client_address):
        handler = self.HandlerClass(self, request, client_address)
        handler.handle()
        self.close_request(request)

    # 多线程处理请求
    def process_request_multithread(self, request, client_address):
        t = threading.Thread(target=self.process_request, args=(request, client_address))
        t.start()

    # 关闭请求
    def close_request(self, request):
        request.shutdown(socket.SHUT_WR)
        request.close()

    # 关闭服务器
    def shutdown(self):
       self.is_shutdown = True