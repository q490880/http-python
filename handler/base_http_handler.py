# encoding=utf-8
from handler.base_handler import StreamRequestHandler
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filenae)s[line:$(lineni)d] - %(levelname)s: %(nessage)s')

class BaseHTTPRequestHandler(StreamRequestHandler):
    def __init__(self, server, request, client_address):
        self.method = None
        self.path = None
        self.headers = None
        self.body = None
        StreamRequestHandler.__init__(self, server, request, client_address)

    # 请求处理
    def handle(self):
        try:
            # 解析请求
            if not self.parse_request():
                return
            # 方法执行(GET、POST)
            method_name = 'do_' + self.method
            # 判断方法是否存在
            if not hasattr(self, method_name):
                self.write_error(404, None)
                return
            method = getattr(self, method_name)
            method() # 应答报文的封装
            # 发送结果
            self.send()
        except Exception as e:
            print(e)
            #logging.exception(e)

    # 解析请求头
    def parse_headers(self):
        headers = {}
        while True:
            line = self.readline()
            if line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                headers[key] = value
            else:
                break
        return headers

    # 解析请求
    def parse_request(self):
        # 解析请求行
        first_line = self.readline()
        words = first_line.split()
        self.method, self.path, self.version = words
        # 解析请求头
        self.headers = self.parse_headers()
        # 解析请求体
        key = 'Content-Length'
        if key in self.headers.keys():
            # 请求内容的长度
            body_length = int(self.headers[key])
            self.body = self.read(body_length)
        return True

    # 写入应答头
    def write_header(self, key, value):
        msg = '%s: %s' % (key, value)
        self.write_content(msg)

    default_http_version = 'HTTP/1.1'

    # 写入正常HTTP应答的头部
    def write_response(self, code, msg):
        # 状态行
        response_line = '%s %d %s' % (self.default_http_version, code, msg)
        self.write_content(response_line)
        self.write_content('Server', '')
        self.write_content('Date', '')

    DEFAULT_ERROR_MESSAGE_TEMPLATE = r'''
    <head>
    <title>Error response</title>
    </head>
    <body>
    <h1>Error response</h1>
    <p>Error code %(code)d.
    <p>Message: %(message)s.
    <p>Error code explanation: %(code)s = %(explain)s.
    </body>
    '''

    responses = {
        100: ('Continue', 'Request received, please continue'),
        101: ('Switching Protocols',
              'Switching to new protocol; obey Upgrade header'),

        200: ('OK', 'Request fulfilled, document follows'),
        201: ('Created', 'Document created, URL follows'),
        202: ('Accepted',
              'Request accepted, processing continues off-line'),
        203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
        204: ('No Content', 'Request fulfilled, nothing follows'),
        205: ('Reset Content', 'Clear input form for further input.'),
        206: ('Partial Content', 'Partial content follows.'),

        300: ('Multiple Choices',
              'Object has several resources -- see URI list'),
        301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
        302: ('Found', 'Object moved temporarily -- see URI list'),
        303: ('See Other', 'Object moved -- see Method and URL list'),
        304: ('Not Modified',
              'Document has not changed since given time'),
        305: ('Use Proxy',
              'You must use proxy specified in Location to access this '
              'resource.'),
        307: ('Temporary Redirect',
              'Object moved temporarily -- see URI list'),

        400: ('Bad Request',
              'Bad request syntax or unsupported method'),
        401: ('Unauthorized',
              'No permission -- see authorization schemes'),
        402: ('Payment Required',
              'No payment -- see charging schemes'),
        403: ('Forbidden',
              'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
              'Specified method is invalid for this resource.'),
        406: ('Not Acceptable', 'URI not available in preferred format.'),
        407: ('Proxy Authentication Required', 'You must authenticate with '
                                               'this proxy before proceeding.'),
        408: ('Request Timeout', 'Request timed out; try again later.'),
        409: ('Conflict', 'Request conflict.'),
        410: ('Gone',
              'URI no longer exists and has been permanently removed.'),
        411: ('Length Required', 'Client must specify Content-Length.'),
        412: ('Precondition Failed', 'Precondition in headers is false.'),
        413: ('Request Entity Too Large', 'Entity is too large.'),
        414: ('Request-URI Too Long', 'URI is too long.'),
        415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
        416: ('Requested Range Not Satisfiable',
              'Cannot satisfy request range.'),
        417: ('Expectation Failed',
              'Expect condition could not be satisfied.'),

        500: ('Internal Server Error', 'Server got itself in trouble'),
        501: ('Not Implemented',
              'Server does not support this operation'),
        502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
        503: ('Service Unavailable',
              'The server cannot process the request due to a high load'),
        504: ('Gateway Timeout',
              'The gateway server did not receive a timely response'),
        505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
    }

    # 写入错误HTTP请求结果
    def write_error(self, code, msg):
        s_msg, l_msg = self.responses[code]
        if msg:
            s_msg = msg
        response_content = self.DEFAULT_ERROR_MESSAGE_TEMPLATE % {
            'code': code,
            'message': s_msg,
            'explain': l_msg
        }

        self.write_response(code, s_msg)
        self.write_content(response_content)

    def end_header(self):
        self.write_content('\r\n')