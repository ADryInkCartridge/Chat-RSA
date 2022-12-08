import socket
import sys
import threading
from time import sleep

server_address = ('localhost', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(10)

connections = []
public_keys = {}

def disconnect(client_socket):
    global public_keys
    print("Disconnected from " + str(client_socket.getpeername()))
    public_keys = {k: v for k, v in public_keys.items() if v != client_socket}
    connections.remove(client_socket)
    client_socket.close()

def broadcast(message, client_socket):
    global public_keys
    split_message = message.split("\r\n\r\n")
    split_message = split_message[:-1 or None]
    print(split_message)
    for m in split_message:
        recipient, message = m.split(":",1)
        recipient = recipient.replace("[","(")
        recipient = recipient.replace("]",")")
        socket = public_keys[recipient]
        print("Trying to send message to " + str(socket.getpeername()))
        if socket != client_socket:
            print("Sending message to " + str(socket.getpeername()))
            encoded = message.encode()
            encoded = str(len(encoded)).encode() + ":message".encode() + "\r\n\r\n".encode() + encoded
            socket.send(encoded) 
    print("Sent message to all clients")


def broadcast_public_keys(new_key = None, client_socket = None):
    global public_keys
    public_keys[new_key] = client_socket
    keys = []
    for key in public_keys:
        keys.append(key)
    print(keys)
    str_keys = "".join(keys)
    str_keys = str_keys.encode()
    print(str_keys)
    for client in connections:
        print("Sending public keys to " + str(client.getpeername()))
        encoded = str(len(str_keys)).encode() + ":keys".encode() + "\r\n\r\n".encode() + str_keys
        client.send(encoded)
    print("Sent public keys to all clients")

def handle(client_socket):
    # try:
        while True:
            data = client_socket.recv(1024)
            print(data)
            if not data:
                disconnect(client_socket)
            else:
                header = data.decode().split("\r\n\r\n",1)[0]
                print("Header: " + header)
                message_len = int(header.split(":",1)[0])
                message_type = header.split(":",1)[1]

                if message_type == 'keys':
                    print("Received new public keys from " + str(client_socket.getpeername()))
                    keys = data.decode().split("\r\n\r\n",1)[1]
                    keys = keys.encode()
                    if len(keys) < message_len:
                        data = client_socket.recv(message_len - len(keys))
                        keys += data
                    broadcast_public_keys(keys.decode(), client_socket)
                    

                elif message_type == 'message':
                    incoming_message = data.decode().split("\r\n\r\n",1)[1]
                    incoming_message = incoming_message.encode()
                    print(incoming_message, len(incoming_message), message_len,  len(incoming_message) == message_len)
                    if len(incoming_message) < message_len:
                        data = client_socket.recv(message_len - len(incoming_message))
                        incoming_message += data
                    broadcast(incoming_message.decode(), client_socket)
                    
    # except:
    #     print("EXCEPTION")
    #     disconnect(client_socket)

try:
    while True:
        connection, client_address = server_socket.accept()
        connections.append(connection)
        
        # public_key = connection.recv(1024)
        # public_keys[public_key] = connection
        # print(public_keys)
        print("Connected to " + str(connection.getpeername()))

        threading.Thread(target=handle, args=(connection,)).start()
    

except KeyboardInterrupt:
    print("Closed")
    server_socket.close()
    sys.exit(0)




