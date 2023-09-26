#In this example we will only have one server, but in production API servers and web servers
#tend to be separate. 

import socket
#The most basic type of server we can make is with sockets. Sockets are like a mailbox for 
#your computer. You specify a port number, and any outside computers that want to get data 
#from our server will specify this computer's address along with the desired port. We can
#have many ports open on a single computer in order to have data we receive sent to different
#applications. In particular, we might use port 80 for our web server (where we send back a
#webpage to a client) and port 8000 for API requests. Keep in mind, only one application may
#use a given port at a time.

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Here we create a socket and specify the "address family" (AF). AF_INET means an IPV4
#address or a domain name. There are others you can use, see here: 
#https://docs.python.org/3/library/socket.html#socket-families

#The second argument is the "protocol family". SOCK_STREAM means that data will be sent
#to and from the client continuously until the connection is terminated. Another common
#protocol type is SOCK_DGRAM, in which something is sent, a reply is sent back, and
#then the connection is terminated. Transport Layer Protocol (TCP) usually uses SOCK_STREAM
#and it ensures the data arrived in order and intact so this is what we will use

HOST = ''
PORT = 3000
server_socket.bind((HOST, PORT))
#AF_INET sockets are bound to a host and a port. IP addresses don't actually belong to a 
#particular computer, rather they belong to a computer's network interface (of which there
#can be many, such as Wifi or Ethernet). When we specify the host as '' it means "bind to
#any available interface". The port number used here is arbitrary, but note there are 
#ports that are often used for specific functions. Learn more here: 
#https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers

MAX_CONNECTIONS = 1
server_socket.listen(MAX_CONNECTIONS)
#Now the server will listen for incoming requests with a maximum of 1 client at a time.
#Obviously in a production app this number will be as high as is feasible

while True:
    client_socket, client_address = server_socket.accept()
    #This loop will wait for a client to connect. When one does, a socket for use in 
    #sending back data to it will be returned, as well as information about its address

    print(client_address, " connected")
    client_data = []
    buffer_size = 1024
    while True:
        client_buffer = client_socket.recv(buffer_size)
        #The loop ensures that as long as the server and client are connected, they
        #will continue to send data each other. recv specifies how many bytes to receive
        #at a time. usually a power of 2 
        client_data += client_buffer
        if not client_buffer or client_buffer[-4:] == b'\r\n\r\n': 
            break
        #When the client has finished sending us stuff we have the complete message
        #WARNING: this code will block if the end of the client request is not caught
        #meaning you must be able to determine when the client is done sending stuff
        #TODO: Fix detecting end of request
        
        #The client can send any data to us. It can be completely unintelligible, but
        #for the API we will be building we will be expecting HTTP requests
        #So let's parse it as if it was HTML. Enter localhost:3000 into the
        #URL bar in a browser and you will actually get an HTTP response
    client_data = bytearray(client_data)
    client_data = client_data.decode("utf-8")
    #HTTP messages are meant to be interpreted as plain strings, so we
    #interpet the raw bytes the client sent into UTF-8 encoded characters
    
    client_data = client_data.split('\r\n')
    #An HTTP request is a string formatted like this:
    #[VERB] /[endpoint] [HTTP VERSION]
    #[key]: [value]
    #[key]: [value]
    #[key]: [value]
    #...
    #The verb corresponds to the HTTP verb (GET, POST, PUT, DELETE, etc.)
    #The endpoint denotes what resource on our server the client is looking for
    for line in client_data:
        print(line)

    #Now we will implement our API. We will use the endpoint to determine what
    #the client is asking for

    client_socket.sendall(b'HTTP/1.1 200 Nice!\r\n'
                          b'Content-Type: application/json'
                          b'Content-Length: 23'
                          b'\r\n\r\n'#this separates the body from the headers
                          b'{"testkey":"testvalue"}'
                          )
    #Like a request, an HTTP response is also a string with key-value pairs
    #separated by newlines
    #[HTTP VERSION] [status code] [associated message]
    #[key]: [value]
    #[key]: [value]
    #[key]: [value]
    #...
    #An optional body may be appended after two empty lines after the key/value pairs 
    #(also known as the headers)
    #In our example we specified an html page 
    client_socket.close()
        





