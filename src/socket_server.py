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
    while True:
        client_data = client_socket.recv(1024)
        #The loop ensures that as long as the server and client are connected, they
        #will continue to send data each other. recv specifies how many bytes to receive
        #at one time. usually a power of 2
        if not client_data: 
            client_socket.close()
            break
        #When the client has finished sending us stuff we close the connection
        print(client_data)



