#This script will show an example of how a client might communicate with the backend

import socket, json

HOST = 'localhost'    
#In this example, our server and client are on the same machine. In production,
#the host to be connected would probably be something like "api.example.com"
PORT = 3000              
#The same port as used by the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))
server.sendall(
f'''GET /account?fname=Zakareya&lname=Alatoli HTTP/1.1
Content-Type: application/json
Accept: application/json 

{{"fname: "Zakareya", "lname": "Alatoli"}}
'''.encode('utf-8'))
response = server.recv(1024)
#We receive the raw response in bytes
#TODO: Make sure the entire response is received in case it's bigger than 1024 bytes

response = response.decode('utf-8')

header = response.split('\r\n')[0]

print(response)