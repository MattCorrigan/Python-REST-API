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

### `.on(event, function) : function`
#### Arguments:
- event: name of the file or event, such as '/index.html' or '404'
- function: the function to be called when the event occurs
  - Must accept 'function(client, request)', where 'client' is the client socket and 'request' is a Request object

#### What it does:
This method adds an event handler to the specified event. The second argument, the function, will be called when the first argument, the event name, occurs. This event might be a file name or '404'. When the event occurs, the function will be passed a client and a request object. The function should also use `client.send(data)` with a response object or a string to send a response back to the client.

### `.start() : function`
#### No Arguments

#### What it does:
It starts a server on port 8080 to listen for requests. It will call the event handlers when a client requests one of the specified events.
