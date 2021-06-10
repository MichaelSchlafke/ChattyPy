# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 14:03:43 2021

@author: smmlscla
"""



import socket 
import _thread
import time
import os
import sys

#alias
print("input alias:")
alias = input()
if not alias:
    alias = "anon"

connected = False

#settings

localhost = True #is the host local

manual_port = True #aks for port?

# socket anlegen
#port
if manual_port:
    print("enter server port:")
    port = int(input())
else:
    port = 12002#<INTEGER>
#ip
if localhost:
    host = socket.gethostbyname(socket.gethostname())
else:
    host = '129.217.162.205'

def reconnect():
    connected = False
    while not connected:   
        try:  
            print("re-enter port:")
            port_in = input()
            if port_in:
                port = port_in
            print("trying to reconnect at: " + host + ":" + str(port))
            sock.connect( ( host, int(port) ) )  
            connected = True  
            print( "re-connection successful" )
            break
        except socket.error:  
            print("attempt not successfull")
            time.sleep( 2 )  

#attempt establishing connection
#try:
sock = socket.socket()
print("connecting to " + str(host) + ":" + str(port))
sock.connect((host, port))
#finally:
    #fix this!!!
    #print("connection failed! re-enter port:")
    #reconnect()
    #os.execl(sys.executable, sys.executable, *sys.argv)

#info nachricht
msg_sttgs = "/alias=" + alias
msg_sttgs_byt = bytes(msg_sttgs, 'utf-8')
sock.send(msg_sttgs_byt)

def recieve_msg():
    try:
        while True:
            msg = sock.recv(1024).decode()+'\n'
            print(msg)
    finally:
        print("connection lost")
        _thread.start_new_thread(reconnect)


_thread.start_new_thread(recieve_msg)

while True: #Sendeschleife

    #Eingabe der Sendedaten mit input()
    msg_clt = input()
    if not msg_clt:
        break           
    else:
        print("\n")
        #msg_clt = alias + ": \n" + msg_clt
        msg_clt_byt = bytes(msg_clt, 'utf-8')
        #Senden der eingegebenen Daten
        sock.send(msg_clt_byt)