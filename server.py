# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 14:03:16 2021

@author: smmlscla
"""



import socket 
from datetime import datetime
#from _thread import start_new_thread 
import _thread
#from threading import Thread
# Neuen Thread starten, recherchieren wie die Funktion runktioniert.

#settings
manual_set_ip = False

#socket anlegen
sock = socket.socket()

#IP setting
if manual_set_ip:
    #user input defined
    print("Input host IP adress:")
    host_manual = input()
    host = host_manual
    print("Input port:")
    port_manual = input()
    sock.bind((host_manual, port_manual))
else:
    #auto selected
    host_auto = socket.gethostbyname(socket.gethostname())
    sock.bind((host_auto, 0))
    port_auto = sock.getsockname()[1]
    print("hosting at: " + str(host_auto) + ":" + str(port_auto))






sock.listen(100)

clients = set()

print("socked created")

def handle_client(client_socket, adress):
    #load history
    with open('history.txt','r') as text_file:
        history = text_file.read()
        history_b = bytes(history, 'utf-8')
        client_socket.sendall(history_b)

        # Warten auf Nachricht der Clientseite
        while True:
            msg = client_socket.recv(1024).decode()+'\n'
            if not msg:
                            break
            else:
                if "@" in msg:
                    print("command detected!")
                    #add alliases
                else:
                    # Ausgabe der Clientnachricht
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    msg = (current_time + ", " + msg)
                    print(msg) 
                    with open('history.txt','a') as text_file:
                        text_file.write(msg + '\n')
                    # Weiterleitung der Nachricht an alle anderen clients
                    msg = bytes(msg, 'utf-8')
                    for c in clients:
                        c.sendall(msg)
                        #print("send to " + str(c)) #debugging
                    
                



#Serverschleife
num_conn = 0
addr = []

while True: 
    
    conn, addr_new = sock.accept()
    clients.add(conn)
    addr.append(addr_new)
    print(addr[num_conn], ' just joind the chat')
    num_conn += 1

    conn.send(b"Welcome to the Server.\n")

    #thread erschaffen
    _thread.start_new_thread(handle_client, (conn, addr_new))

