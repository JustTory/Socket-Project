import socket

HOST = '127.0.0.2' # server's IP
PORT = 65432 # server's port: any non-privileged ports

# s = socket.socket(addr_family, type)
# addr_family:
#   socket.AF_INET: Internet protocol (IPv4)
#   socket.AF_INET6: Internet protocol (IPv6)
# type:
#   socket.SOCK_STREAM: Connection based stream (TCP)
#   socket.SOCK_DGRAM: Datagrams (UDP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
print("Server 2 is online, wating for connections...")

while True:
    conn, addr = s.accept()
    print(addr, "has connected")

    while True:
        data = conn.recv(1024)
        str_data = data.decode("utf8")
        if str_data == "exit": break
        if not data: break
        print("Client: " + str_data)
        serverMsg = input("Server: ")
        conn.sendall(bytes(serverMsg, "utf8"))

    conn.close()
    print(addr, "has disconnected")

s.close()