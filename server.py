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
manual_port_overwite = False
port = 64303

manual_set_ip = False

#socket anlegen
sock = socket.socket()

#IP setting
if manual_port_overwite:
    host_auto = socket.gethostbyname(socket.gethostname())
    sock.bind((host_auto, port))
    print("hosting at: " + str(host_auto) + ":" + str(port))
elif manual_set_ip:
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
identities = {}


print("socket created")

def handle_client(client_socket, adress):
    #load history
    alias = "anon"
    try:
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
                    if "/" in msg:
                        if "/alias=" in msg:
                            alias_new = msg[7:]
                            alias_new = alias_new.replace('\n', '').replace('\r', '')
                            if alias == "anon":
                                msg_conn = "A wild " + alias_new + " appears!\t"
                            else:
                                msg_conn = alias + " turned into " + alias_new + "!\t"
                            alias = alias_new
                            alias = alias.replace('\n', '').replace('\r', '')
                            #connect alias to ip
                            identities[alias] = (client_socket)
                            #print("current identities:\n" + str(identities))
                            msg_comm_resp = "[Name set to " + alias + "]"
                            
                            for c in clients:
                                c.sendall(bytes(msg_conn, 'utf-8'))
                            print("current users: \n" + str(identities))
                        elif "/users" in msg:
                            msg_comm_resp = "[currently online:]\n"
                            for user in identities:
                                msg_comm_resp += "\t" + user + "\n"
                        elif "/help" in msg:
                            msg_comm_resp = "[list of commands:]\n/alias=[name here]\tfor changing names\n/users\tfor list of current users\n"
                        client_socket.sendall(bytes(msg_comm_resp, 'utf-8'))
                    elif "@" in msg:
                        print("@ command detected!")
                        #add alliases
                        for alias_other in identities:
                            print("searching for @" + str(alias_other))
                            if "@" + str(alias_other) in str(msg):
                                #formulieren der Nachricht
                                msg = msg.replace("@" + str(alias_other),"")
                                now = datetime.now()
                                current_time = now.strftime("%H:%M:%S")
                                msg = (alias + " to "+ alias_other + ", " + current_time + ":\n" + msg)
                                print(msg) 
                                #send message
                                msg = bytes(msg, 'utf-8')
                                identities[alias_other].sendall(msg)


                    else:
                        # Ausgabe der Clientnachricht
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        msg = (alias + ", " + current_time + ":\n" + msg)
                        print(msg) 
                        with open('history.txt','a') as text_file:
                            text_file.write(msg + '\n')
                        # Weiterleitung der Nachricht an alle anderen clients
                        msg = bytes(msg, 'utf-8')
                        for c in clients:
                            c.sendall(msg)
                            #print("send to " + str(c)) #debugging
    #except socket.error:
        #print("logging error")
        #with open('error_log.txt','a') as text_file:
            #text_file.write("???" + '\n')
    except socket.error:
        print("closing socket: " + str(client_socket))
        msg = (alias + " disconnected!")
        clients.remove(client_socket)
        client_socket.close()
        if alias != "anon":
            identities.pop(alias)
        print(msg)
        for c in clients:
            try:
                c.sendall(bytes(msg, 'utf-8'))
            except:
                print("critical error when sending disconnect msg to user:" + str(c))
                    
                



#Serverschleife
num_conn = 0
addr = []

while True: 
    
    conn, addr_new = sock.accept()
    clients.add(conn)
    addr.append(addr_new)
    msg_conn = str(addr[num_conn]) + ' just joind the chat'
    print(msg_conn)
    #for c in clients:
        #c.sendall(bytes(msg_conn, 'utf-8'))
    num_conn += 1

    conn.send(b"Welcome to the Server.\nuse /help to see all commands\n")

    #thread erschaffen
    _thread.start_new_thread(handle_client, (conn, addr_new))

