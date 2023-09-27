#This script will show an example of how a client might communicate with the backend

import socket, json

HOST = 'localhost'    
#In this example, our server and client are on the same machine. In production,
#the host to be connected would probably be something like "api.example.com"
PORT = 3000              
#The same port as used by the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))
server.sendall(b'GET /randomnumber HTTP/1.1\r\n'
                      b'Accept: application/json'
                      b'\r\n\r\n'
                      )
response = server.recv(1024)
#We receive the raw response in bytes

body = response.split(b'\r\n\r\n')[-1]
#We separate the body from the header
print(body)

json_response = json.loads(body.decode('utf-8'))
for key in json_response:
  print(f"{key}: {json_response[key]}")