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

host = '129.217.162.178'
port = 12020#<INTEGER>
#socket anlegen
sock = socket.socket()
sock.bind((host, port))
sock.listen(100)

clients = set()

print("socked created")

def handle_client(client_socket, adress):
    #load history
    #with open('history.txt','a') as text_file:
        #history = text_file.read()
        #history_b = bytes(history, 'utf-8')
        #client_socket.sendmsg(history_b)
    
        while True:
            # Warten auf Nachricht der Clientseite
            while True:
                #print(client_socket)
                #print(adress)
                #client_socket.
                msg = client_socket.recv(1024).decode()+'\n'
                if not msg:
                                break
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
                    #will nicht.
                    #for i in range(len(adress)):
                        #sock.sendto(msg,adress[i])
                    for c in clients:
                        c.sendall(msg)
                        #print("send to " + str(c))
                        
                



#Serverschleife
num_conn = 0
addr = []

while True: 
    
    conn, addr_new = sock.accept()
    clients.add(conn)
    addr.append(addr_new)
    #with conn:
        #welcome_msg = bytes((str(addr[0]) + ' just joind the chat'), 'utf-8')
    print(addr[num_conn], ' just joind the chat')
    #print(addr)
    num_conn += 1
        #sock.sendall(welcome_msg)
    conn.send(b"Welcome to the Server.\n")

        #thread erschaffen
    _thread.start_new_thread(handle_client, (conn, addr_new))

        #thread = Thread(target = handle_client, args = (conn, ))
        #thread.start()

        #handle_client(conn)
