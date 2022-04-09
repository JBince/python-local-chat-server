#!/usr/bin/python3

import threading
import socket
import sys
from time import sleep
from datetime import datetime


#Check for sufficient args
if len(sys.argv) != 3:
    print(f'[*] Usage: {sys.argv[0]} <Bind Address> <Bind Port>')
    exit()

#Get bind address and port
bind_addr = str(sys.argv[1])
bind_port = int(sys.argv[2])

#Create and bind server to desired interface and port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_addr,bind_port))
server.listen()

#Get clients and their nicknames
clients = []
nicknames = []

#Send message to all OTHER clients, not the user who sent it
def broadcast(message,cli='',name=''):
    for c in clients:
        if str(c) != str(cli):
            if name:
                usr_msg = message.replace(b"\n",b"").decode("utf-8")
                usr_msg = f'{name}: {usr_msg}'.encode("utf-8")
                log(usr_msg.decode("utf-8"))
                c.send(usr_msg)
            else:
                c.send(message)

#Handle message from clients
def handle(client):
    while True:
        try:
            #Broadcast message
            message = client.recv(1024)
            cli = str(client)
            name = nicknames[clients.index(client)]
            broadcast(message,cli,name)
        except:
            #Remove and close client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the server')
            nicknames.remove(nickname)
            break

#Create users, log their entry
def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        #Request and store nickname
        client.send('Name: '.encode("utf-8"))
        nickname = client.recv(1024).replace(b"\n",b"").decode("utf-8")

        #Create user obj for referencing
        print(f'{nickname} has connected')
        log(f'{nickname} has connected')
        clients.append(client)
        nicknames.append(nickname)

        #Print nickname and join message
        client.send(f'Hello {nickname}. For a list of commands, please type /help\n'.encode("utf-8"))
        broadcast(f'{nickname} has joined the server\n'.encode("utf-8"))

        #Start handling thread for clients
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

#Logs user connections and messages
def log(message,nickname=''):
    f = open("log.txt", "a")
    now=datetime.now()
    dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
    if message:
        if nickname:
            nickname = nickname[0]
            log = f"{nickname} logged in at {dt_string}\n"
            print(log)
            f.write(log)
        else:
            log = f"{dt_string} {message}\n"
            print(log)
            f.write(log)

#Start server
print ('<--SERVER RUNNING-->')
receive()