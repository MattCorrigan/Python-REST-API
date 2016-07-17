#!/usr/bin/env python

import socket
import os.path
from thread import start_new_thread
import mimetypes
mimetypes.init()

host = ''
port = 8080
backlog = 5
size = 1024

codes = {"200": "OK", "400": "Bad Request", "404": "Not Found", "500": "Server Error"}
newline = "\r\n"
stop = False

class Request:
    def __init__(self, client, data):
        self.client = client
        self.data = data

class Response:
    def __init__(self, server, client=None, data=None):
        self.server = server
        self.headers = {}
        self.statusCode = 200
        self.status = "OK"
        self.path = "./index.html"
        self.client = client
        self.data = data

    def header(self, name, value):
        if not (name == "Content-Length" or name == "Content-Type"):
            self.headers[name] = value
            return 1
        else:
            return 0

    def setCode(self, statusCode):
        global codes
        self.statusCode = statusCode
        codeMeaning = codes[str(self.statusCode)]
        if codeMeaning:
            self.status = codeMeaning
        else:
            return 0
        return 1

    def form_headers(self, content):
        self.headers["Content-Type"] = mimetypes.types_map["." + self.path.split("/")[-1].split(".")[-1]]
        self.headers["Content-Length"] = len(content)

        return "".join([str(i)+": "+str(j)+"\r\n" for i,j in self.headers.iteritems()])

    def getContent(self):
        if not os.path.isfile(self.path):
            if not "./404" in self.server.events:
                self.path = ".html" # do this so mimetypes interprets data as .html file
                return "<h1>404 File Not Found</h1>"
            self.server.events["./404"](self.client, self.data)

        f = open(self.path, "rb")
        f_contents = f.read()
        f.close()

        return f_contents

    def form(self):
        global newline
        content = self.getContent()
        response = "HTTP/1.1 " + str(self.statusCode) + " " + self.status + newline +\
                   self.form_headers(content) + newline +\
                   content
        return response



def handle(server, client, data):
    path = ""
    try:
        path = data.strip("\r").split("\n")[0].split(" ")[1]
    except:
        return 0

    #remove after release
    if "kill_server" in path:
        global stop
        stop = True
        print("stopping server...")
        return 0

    if path.startswith("/"):
        path = "." + path
    else:
        path = "./" + path

    if path in server.events:
        server.events[path](client, data)
    else:
        # no handler
        r = Response(server, client, data)
        r.path = path
        client.send(r.form())

    try:
        client.close()
    except:
        pass

class Server:
    def __init__(self):
        self.events = {}

    def on(self, event, function):
        if event.startswith("/"):
            event = "." + event
        elif not event.startswith("./"):
            event = "./" + event
        self.events[str(event)] = function

    def start(self):
        global host, port, backlog, size
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host,port))
        s.listen(backlog)

        while 1:
            if stop:
                assert 0
            client, address = s.accept()
            data = client.recv(size)
            start_new_thread(handle, (self, client, data))

s = Server()

def index(client, data):
    global s
    r = Response(s)
    r.path = "./index.html"
    client.send(r.form())

s.on("index.html", index)

s.start()
