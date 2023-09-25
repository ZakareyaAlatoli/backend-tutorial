#This script will show an example of how a client might communicate with the backend

import socket

HOST = 'localhost'    
#In this example, our server and client are on the same machine. In production,
#the host to be connected would probably be something like "api.example.com"
PORT = 3000              
#The same port as used by the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.sendall(b'Hello, world')