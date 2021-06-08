# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 14:03:43 2021

@author: smmlscla
"""



import socket 
import _thread

alias = "client1"

# socket anlegen
host = '129.217.162.178'
port = 12020#<INTEGER>
sock = socket.socket()
sock.connect((host, port))

def recieve_msg():
    while True:
        msg = sock.recv(1024).decode()+'\n'
        print(msg)

_thread.start_new_thread(recieve_msg)

while True: #Sendeschleife

    #Eingabe der Sendedaten mit input()
    #print("enter message: ")
    msg_clt = input()
    if not msg_clt:
        #msg = sock.recv(1024).decode()+'\n'
        #print(msg)
        break           
    else:
        print("\n")
        msg_clt = alias + ": \n" + msg_clt
        msg_clt_byt = bytes(msg_clt, 'utf-8')
        #Senden der eingegebenen Daten
        sock.send(msg_clt_byt)
    ##Warten auf Antwort des Servers
    #msg = sock.recv(1024).decode()+'\n'
    ##Ausgabe der Server Antwort
    #print(msg)