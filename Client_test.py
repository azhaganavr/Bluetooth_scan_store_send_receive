#!/usr/bin/python           # This is client.py file
import socket               # Import socket module
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
port = 21               #Reserveaportfor your service.
print('Tryning to connect.....')
#while 1==1:
s.connect(("192.168.0.9", port))
print (s.recv(2048).decode())

