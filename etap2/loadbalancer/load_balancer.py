import socket
import threading
from threading import Lock
import sys
from time import sleep
import ssl
import requests
from http.server import BaseHTTPRequestHandler
from io import BytesIO
import logging
logging.basicConfig(level=logging.DEBUG)


max_request_size = 1*1024*1024
buffer_size = 2*max_request_size
http_server_port = 80
https_server_port = 443
bad_request = b'HTTP/1.1 400 Bad Request\r\nVary: Accept-Encoding\r\nContent-Encoding: gzip\r\nContent-Length: 0\r\nConnection: close\r\nContent-Type: text/html;\r\n\r\n'
REDIRECT_HEADER = b'HTTP/1.1 307 Encryption Required\r\nLocation: https://loadbalancer%b\r\nConnection: close\r\nCache-control: private\r\n\r\n<html><body>Encryption Required.  Please go to for this service.</body></html>'
REDIRECT_TEMP = b'HTTP/1.1 307 Temporary Redirect\r\nLocation: https://loadbalancer%b\r\nConnection: close\r\nCache-control: private\r\n\r\n<html><body>Encryption Required.  Please go to for this service.</body></html>'
MAX_CONNECTIONS_TO_LB = 1

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message


class Connection(threading.Thread):
    def __init__(self, connection, address, connection_close_signal, redirect=False, group=None,target=None, name=None, args=(), kwargs=None):
        threading.Thread.__init__(self, group=group, target=target, name=name)
        self.conn = connection
        self.addr = address
        self.connection_close_signal = connection_close_signal
        self.redirect = redirect

    def run(self):
        logging.debug('New conection to '+repr(self.addr))

        def response_error(error):
            self.conn.send(bad_request)
            self.conn.close()

        def response(request, data=None):
            # r = requests.get('http://studia.elka.pw.edu.pl/', stream=True)
            s = requests.Session()
            req = requests.Request(request.command, 'http://api_server:5000'+request.path, data=data, headers=request.headers)
            prepped = req.prepare()
            print(request.headers)
            print(data)
            print(prepped.headers)
            print(prepped.body)
            r = s.send(prepped, stream=True)

            response = b'HTTP/1.1 '+str.encode(str(r.status_code))+b' '+str.encode(r.reason)+b'\r\n'+b'\r\n'.join((str.encode(k)+b': '+str.encode(v) for k, v in r.headers.items()))+b'\r\n\r\n'
            response+=r.raw.read()
            logging.debug('Server response %s...',response[:10])
            self.conn.send(response)
            logging.debug('Sended to client %s...',self.addr)
            sleep(15)

        if self.redirect:
            request = self.conn.recv(buffer_size) 
            request = HTTPRequest(request)
            if request.error_code is None:
                logging.debug('Redirecting %s by sending %s', self.addr, REDIRECT_TEMP%(str.encode(request.path)))
                self.conn.send(REDIRECT_TEMP%(str.encode(request.path)))
            else:
                logging.debug('Bad request %s',request.error_code)
            self.conn.close()
            return

        count = 0
        while True:
            request = self.conn.recv(buffer_size) 
            if len(request) < 1:
                self.conn.close()
                break
            request = HTTPRequest(request)
            if request.error_code is None:
                if request.command in ['POST', 'PUT', 'DELETE']:
                    if 'Content-Length' in request.headers.keys() and int(request.headers['Content-Length']) <= max_request_size:
                        request_data = b''
                        logging.debug('Request response from '+repr(self.addr)+' '+repr(request.command)+' '+'content-length:'+str(request.headers['Content-Length']))
                        request_data = request.rfile.read(max_request_size+1)
                        if len(request_data) == 0 and int(request.headers['Content-Length']) > 0:
                            logging.debug('Request response from '+repr(self.addr)+' data in next packet')
                            request_data = self.conn.recv(int(request.headers['Content-Length']))
                        if len(request_data) > max_request_size:
                            logging.debug('Request response from '+repr(self.addr)+' send data is to big')
                            response_error('')
                            break
                        else:
                            logging.debug('Request response from '+repr(self.addr)+' recived data '+repr(request_data[:10])+'...')
                            response(request, request_data)
                    else:
                        response_error('')
                        break
                else:
                    logging.debug('Request response from '+repr(self.addr)+' '+repr(request.command)+' '+repr(request.path))
                    response(request)
            else:
                logging.debug('Bad request %s',request.error_code)
                response_error('')
                break
        logging.debug('Connection to %s closed',self.addr)
        self.connection_close_signal()

class LoadBalancer(threading.Thread):

    def __init__(self, address, secure=True, group=None, target=None, name=None, args=(), kwargs=None):
        threading.Thread.__init__(self, group=group, target=target, name=name)
        self.address = address
        self.secure = secure
        self.connections_count = 0
        self.connections_count_lock = Lock()

    def connection_close_signal(self):
        with self.connections_count_lock:
            self.connections_count-=1
            logging.debug('Connection close. There is %s active connections', self.connections_count)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(self.address)
            s.listen(0)
            while True:
                conn, addr = s.accept()
                if self.secure:
                    try:
                        conn = ssl.wrap_socket(conn, server_side=True, certfile="server.crt", keyfile="server.key")
                    except:
                        conn.close()
                        continue

                redirect_to_diffrend_lb = False
                with self.connections_count_lock:
                    if self.connections_count >= MAX_CONNECTIONS_TO_LB:
                        redirect_to_diffrend_lb = True
                    else:
                        self.connections_count+=1
                        logging.debug('New connection. There is %s active connections', self.connections_count)

                t = Connection(conn, addr, connection_close_signal=self.connection_close_signal, redirect=redirect_to_diffrend_lb)                  
                # t = threading.Thread(name='connection_worker', target=connection_worker, args=(conn, addr))
                t.start()

class RedirectToSecureConnection(threading.Thread):

    def __init__(self, address, secure=True, group=None, target=None, name=None, args=(), kwargs=None):
        threading.Thread.__init__(self, group=group, target=target, name=name)
        self.address = address
        self.secure = secure

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(self.address)
            s.listen(5)
            while True:
                conn, addr = s.accept()
                request = conn.recv(buffer_size) 
                if len(request) < 1:
                    conn.close()
                    break
                request = HTTPRequest(request)
                if request.error_code is None:
                    logging.debug('Redirecting %s by sending %s', addr, REDIRECT_HEADER%(str.encode(request.path)))
                    conn.send(REDIRECT_HEADER%(str.encode(request.path)))
                else:
                    logging.debug('Bad request %s',request.error_code)
                conn.close()

try:
    lb = LoadBalancer(('', https_server_port))
    lb.start()
    redirect = RedirectToSecureConnection(('', http_server_port))
    redirect.start()

except KeyboardInterrupt:
    print('Load balancer stoped...')