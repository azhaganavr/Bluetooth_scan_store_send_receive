import socket               # Import socket module


port = 21
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.0.9", port))
# s.bind(("10.136.36.101", port))

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
print('Server Listening.......')


#host = socket.gethostname() # Get local machine name
#host = '14.139.160.42'


c, addr = s.accept()     # Establish connection with client.
print ('Got connection from', addr)
c.send('Thank you for connecting'.encode())
c.close()                # Close the connection