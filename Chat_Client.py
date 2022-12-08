import socket
import sys
import threading
import time
import RSA as RSA
import Key_Provider as key_provider
from time import sleep
import re
import multiprocessing
import concurrent.futures
from datetime import datetime



username  = input("Enter username: ")
public_key, private_key = key_provider.generate_keys()
print("Public key: " + str(public_key))
print("Private key: " + str(private_key))

public_keys = [public_key]

server_address = ('localhost', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

def update_public_keys(keys):
    global public_keys
    keys = keys.replace("(","")
    keys = keys.replace(")",";")
    keys = keys.replace(" ","")
    keys = keys.split(";")
    for key in keys:
        if key != "":
            key = key.split(",")
            key = (int(key[0]), int(key[1]))
            if key not in public_keys:
                public_keys.append(key)
    print("Updated public keys: " + str(public_keys))


def handle(client_socket):
    # try:
        while True:
            data = client_socket.recv(1024)
            print("Received data from server ", data)
            if not data:
                print("No data received from server")
                print("Disconnected from server")
                client_socket.close()
                sys.exit(0)
            else:
                header = data.decode().split("\r\n\r\n",1)[0]
                print("Header: " + header)
                message_len = int(header.split(":",1)[0])
                message_type = header.split(":",1)[1]

                print("Received " + str(message_len) + " bytes of " + message_type + " from server")

                if message_type == 'keys':
                    print("Received public keys from server")
                    keys = data.decode().split("\r\n\r\n",1)[1]
                    keys = keys.encode()
                    if len(keys) < message_len:
                        data = client_socket.recv(message_len - len(keys))
                        keys += data
                    print("Received public keys: " + keys.decode())
                    update_public_keys(keys.decode())

                elif message_type == 'message':
                    incoming_message = data.decode().split("\r\n\r\n",1)[1]
                    incoming_message = incoming_message.encode()
                    print(incoming_message, len(incoming_message), message_len, message_len == len(incoming_message))
                    if (len(incoming_message) < message_len):
                        data = client_socket.recv(message_len - len(incoming_message))
                        incoming_message += data
                    print(RSA.RSA_Decrypt(private_key,incoming_message.decode()))
                    
    # except:
        print("Disconnected from server")
        client_socket.close()
        sys.exit(0)

try:

    client_socket.send(str(len(str(public_key))).encode() + ":keys".encode() + "\r\n\r\n".encode() + str(public_key).encode())
    thread = threading.Thread(target=handle, args=(client_socket,)).start()
    
    try:
        while True:
            message = input(username +"(You): ")
            now = "(" + datetime.now().strftime('%Y-%m-%d-%H_%M-%S') + ")"
            sent = ""
            message = username + now + ": " + message
            if len(public_keys) == 0:
                print("No public keys available")
            else:
                # for key in public_keys:
                #     key, encrypted = RSA.RSA_Encrypt(key, message)
                with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                    futures = [executor.submit(RSA.RSA_Encrypt, [list(keys),message]) for keys in public_keys]
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            target_key, message = future.result()
                            sent += str(target_key) + ":" + str(message) + "\r\n\r\n"
                        except Exception as exc:
                            print(exc)
                            pass
                sent = sent.encode()
                print("Sent: " + sent.decode())
                client_socket.send(str(len(sent)).encode() + ":message".encode() + "\r\n\r\n".encode() + sent)
            
            
    except KeyboardInterrupt:
        print("Closed")
        client_socket.close()
        sys.exit(0)
        
       

except KeyboardInterrupt:
    print("Disconnnected from " + str(client_socket.getpeername()))
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()
    sys.exit(0)