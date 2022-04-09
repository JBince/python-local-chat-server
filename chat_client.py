#!/usr/bin/python3
import sys
import socket
import threading


if len(sys.argv) !=3:
    print(f"[*] Usage: {sys.argv[0]} <Remote Address> <Remote Port>")
    exit()

connect_addr=sys.argv[1]
connect_port=int(sys.argv[2])

nickname=input("Please select a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((connect_addr,connect_port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "Name: ":
                client.send(nickname.encode("utf-8"))
            else:
                print(message)
        except:
            print("An error occured")
            client.close()
            break
def write():
    while True:
        message = '{}'.format(input(''))
        client.send(message.encode("utf-8"))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()