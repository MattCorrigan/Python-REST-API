import rest

# create server object
s = rest.Server()

def index(client, request):
    global s

    # initiate the request variable
    r = rest.Response(s)

    # set the file path where the content will be loaded from
    r.path = "./index.html"

    # send the file './index.html' back to the client
    client.send(r.form())

# call index() when index.html is requested
s.on("index.html", index)

def error404(client, request):
    global s

    # initiate the request variable
    r = rest.Response(s)

    # set the status code to 404
    r.setCode(404) # the status description is automatically loaded

    # set the file path where the content will be loaded from
    r.path = "./404.html"

    # send the file './404.html' back to the client
    client.send(r.form())

# call error404() when a file is not found
s.on("404", error404)

# start the server
s.start()
