#In this example we will only have one server, but in production API servers and web servers
#tend to be separate. 

import socket
from random import randint
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

MAX_CONNECTIONS = 64
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
    timeout = False
    while True:
        client_socket.settimeout(3)
        try:
            client_buffer = client_socket.recv(buffer_size)
        except TimeoutError:
            print("Client timed out")
            client_socket.sendall(f'HTTP/1.1 400 Empty request\r\n\r\n'.encode('utf-8'))
            client_socket.close()
            timeout = True
            break
        #The loop ensures that as long as the server and client are connected, they
        #will continue to send data each other. recv specifies how many bytes to receive
        #at a time. usually a power of 2 
        client_data += client_buffer
        if not client_buffer or client_buffer[-4:] == b'\r\n\r\n' or len(client_buffer) < buffer_size: 
            break
        #When the client has finished sending us stuff we have the complete message
        #WARNING: this code will block if the end of the client request is not caught
        #meaning you must be able to determine when the client is done sending stuff
        #TODO: Fix detecting end of request
        
        #The client can send any data to us. It can be completely unintelligible, but
        #for the API we will be building we will be expecting HTTP requests
        #So let's parse it as if it was HTML. Enter localhost:3000 into the
        #URL bar in a browser and you will actually get an HTTP response
    if timeout:
        continue
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

    top_header = client_data[0]
    path = top_header.split(' ')[1]
    #This should gives us something like "/path/to/resource" Now we determine what
    #message to return based on the requested resource
    #Note that the endpoint can also contain query parameters, which are in this format:
    #/endpoint?queryparam1=value1&queryparam2=value2
    #A question mark marks the beginning of the query parameters
    path = path.split('?')
    endpoint = path[0]
    querystring = None
    if len(path) > 1:
        querystring = path[1]
    #This checks if a query is present
    queries = []
    if querystring:
        queries = querystring.split('&')
    #If there are we split them up
    queryjson = {}
    for q in queries:
        key, val = q.split('=')
        queryjson[key] = val

    #Now we will check the endpoints to see what data we should send back
    if endpoint == '/randomnumber':
        message = f'''HTTP/1.1 200 Here\'s your number!
        Content-Type: application/json
        

        {{"number": "{randint(0,100)}"}}
        '''
        #We just send a random number from 0 to 100 as JSON
    elif endpoint == '/colors':
        color1 = 'red'
        color2 = 'blue'
        if 'color1' in queryjson:
            color1 = queryjson['color1']
        if 'color2' in queryjson:
            color2 = queryjson['color2']

        message = f'''HTTP/1.1 200 Ooh pretty colors!
        Content-Type: text/html

        
        <!DOCTYPE html>
        <html>
            <head>
                <title>Just Two Colors</title>
            </head>
            <body>
                <div style="color:{color1};">Color 1</div>
                <div style="color:{color2};">Color 2</div>
            <body>
        </html>
        '''
        #Try visiting "[ipaddress of backend]:[port]/colors?color1=red&color2=green" 
        #in a web browser to see this response fully rendered
    else:
        message = f'''HTTP/1.1 404 We ain\'t found jack

        
        '''
        
    client_socket.sendall(message.encode('utf-8'))
    #And send the raw bytes
    #Like a request, an HTTP response is also a string with key-value pairs
    #separated by newlines
    #[HTTP VERSION] [status code] [associated message]
    #[key]: [value]
    #[key]: [value]
    #[key]: [value]
    #...
    #An optional body may be appended after two empty lines after the key/value pairs 
    #(also known as the headers)
    #It can be anything, like JSON or a an html page
    client_socket.close()
        





