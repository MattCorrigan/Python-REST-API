# Python REST API
A simple rest api module built in python. My goal was to create this in under 4 hours, I did it in under 3. This module allows you to create a server object, add event handlers, and access requests and responses painlessly.

# Example
As an example, this program serves an index.html file, and a 404.html file if the requested file is not available.

```
import rest

s = rest.Server()

def index(client, request):
    global s
    r = rest.Response(s)
    r.path = "./index.html"
    client.send(r.form())

def error404(client, request):
    global s
    r = rest.Response(s)
    r.setCode(404)
    r.path = "./404.html"
    client.send(r.form())

s.on("index.html", index)
s.on("404", error404)

s.start()

```

This code is available with comments in '/example/example.py'.
> Note: If '/' should serve '/index.html' also, then add 's.on("/", index)'.

# Documentation

Python v2.7.10

## Usage Of This Module
> To use this module, you should add the '/rest' folder in the same directory as your python script, or add it to your python 'Lib' folder.

The first step to creating a server is to import the module and create a Server object.
```
import rest

server = rest.Server()
```

Next, you can add event handlers with server.on(name, function). These event handlers are usually files/folders, but can be '404' to handle cases when a file is not found. **Note: the name of the file/folder can start with '/', './', or just nothing at all.**
```
def serveIndexFile(client, request):
  # do stuff, and send data back to client

server.on("/", serveIndexFile)
```

Inside of your function, you should send data back to the client with `client.send(data)`, probably by using the `Request` object.
```
def serveIndexFile(client, request):
  # either do this:
  global server
  r = rest.Response(server)
  r.path = "./index.html"
  client.send(r.form())
  
  # or this, if you want to send raw html:
  client.send("<h1>Your HTML here</h1>")
```

There are also many other configurations you can make to the response object.

Lastly, you need to start your server with:
```
s.start()
```

## `Server` Object

### `.__init__() : constructor`
#### No Arguments

#### What it does:
Initializes the object and a dictionary to hold events. Used by calling `s = Server()`.

### `.on(event, function) : method`
#### Arguments:
- event: name of the file or event, such as '/index.html' or '404'
- function: the function to be called when the event occurs
  - Must accept 'function(client, request)', where 'client' is the client socket and 'request' is a Request object

#### What it does:
This method adds an event handler to the specified event. The second argument, the function, will be called when the first argument, the event name, occurs. This event might be a file name or '404'. When the event occurs, the function will be passed a client and a request object. The function should also use `client.send(data)` with a response object or a string to send a response back to the client.

### `.start() : method`
#### No Arguments

#### What it does:
It starts a server on port 8080 to listen for requests. It will call the event handlers when a client requests one of the specified events.

## `Request` Object

### `.__init__(client, data) : constructor`
#### Arguments:
- client: the client socket that has connected
- data: the http request that was sent by the client

#### What it does:
Creates a request object. This object is usually created by Server object and then sent to the corresponding event handler.

### `.client : object`
The client socket.

### `.data : string`
The http request sent to the server.

### `.lines : array`
A list of the lines that make up the request.

### `.req_line : string`
The first line, or the request line. This line usually contains the http method, the path, and the http version.

### `.method : string`
The http method used in the request.

### `.path : string`
The path to the requested file.

### `.http_version : string`
The version of http that the client is using.

### `.headers : dictionary`
A dictionary of the headers and their values that the request contained.

### `.content : string`
Any content sent after the headers, known as the body of the request.


## `Response` Object

### `.__init__(server, client=None, data=None) : constructor`
#### Arguments:
- server: the Server object
- client: optional, the client socket
- data: optional, the raw http request

#### What it does:
This contructor initializes tons of variables and creates a response object to be used to send data back to the client.

### `.server : object`
This is the Server object that is currently running.

### `.headers : dictionary`
A dictionary of headers and values to be sent back to the client.

### `.statusCode : integer`
The status code, such as 200 or 404. This variable should not be set by your program, rather `setCode` should be called. This insures that the correct description is given to the status code.

### `.status : string`
This variable holds the description of the status code. This should not be set by your program, rather `setCode` will appropriately name this based on the code that you pass to `setCode`.

### `.path : string`
The path to the file that will be sent back to the client. This variable is used when `.form()` is called to load the file.

### `.client : object`
This is the client socket that the response should be sent back to.

### `.data : string`
This is the raw http request that was sent by the client.

### `.header(name, value) : method`
#### Arguments:
- name: the name of the header, such as 'User-Agent' or 'Connection'
- value: the value of the header, such as 'text/html' or 'close'

#### What it does:
This method adds a header to be sent back to the client in the response. 'Content-Type' and 'Content-Length' are not allowed, as they will be set automatically. Returns 1 if the header is accepted, or 0 if the header is one of the two that are not accepted.

### `.setCode(statusCode) : method`
#### Arguments:
- statusCode: The status code that will be sent in the response, such as 200, 404, or 503

#### What it does:
This function sets `.statusCode` to the argument given, and sets `.status` to the corresponding description.

### `.form_headers(content) : method`
#### Arguments:
- content: the body of the request, can be accessed from a Request object by using `request.content`

#### What it does:
This argument is used by `.form()` to add colons inbetween names and values, and to separate each header with a '\r\n'. This method returns a string with that information.

### `.getContent() : method`
#### No Arguments

#### What it does:
This method returns the contents of the file at the location of `.path`. If the file is not found, it will call the '404' event handler. If there is no such event handler, it will send a response with the contents '<h1>404 File Not Found</h1>'.

### `.form() : method`
#### No Arguments

#### What it does:
This method uses the object's methods and variables to create a fully-fledged http/1.1 response. It returns a string of the response, to be sent with `client.send(data)`.
