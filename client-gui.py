from chat_client_ui import Ui_MainWindow # Hier wird das eigene Design geladen
import sys
from PyQt5 import QtWidgets,QtCore,QtGui # Erforderliche QT Bibliotheken werden importiert!
import socket
import _thread
import time
import os

# Dies ist ein Template und soll als Denkanstoß dienen. Trotzdem sollten alle Funktionen verstanden werden und die Aufgabe nicht durch ausprobieren gelöst werden.

sock = socket.socket()

# Hauptfenster erbt von dem Designer Ergebnis und von einer QT Klasse
class Hauptfenster(QtWidgets.QMainWindow, Ui_MainWindow): 

    # def recieve_msg(self):
    #     try:
    #         while True:
    #             msg = sock.recv(1024).decode()+'\n'
    #             print(msg)
    #     finally:
    #         print("connection lost")
    #         #ADD DISCONNECT
    #         #_thread.start_new_thread(reconnect)

    def __init__(self, app, parent = None):
        super(Hauptfenster, self).__init__(parent)                      # Ausführen der __init__ der Elternklasse
        self.setupUi(self)                                              # Initialisierung des User Interface
        self.app = app

        # History anlegen oder laden
        # Signals and Slots der einzelnen Elemente verbinden (Ein guter Anfang sind eine Sendebox und eine Anzeige für das Chatprotokoll)
        #button = QPushButton("connect")
        self.ConnectButton.clicked.connect(self.on_connectButtonClicked) 
        self.SendButton.clicked.connect(self.on_sendButtonClicked)
        self.DisconnectButton.clicked.connect(self.on_disconnectButtonClicked)
        self.HelpButton.clicked.connect(self.on_helpButtonClicked)

    def on_connectButtonClicked(self):
        """
        Diese Funktion wird aufgerufen, sobald der Verbindenknopf gedrückt wird.

        """
        #read inputs
        toggle_local_host = self.toggleLocalHost.checkState()
        if toggle_local_host:
            print("using local host")
            #host = 'localhost' #broken!
            host = socket.gethostbyname(socket.gethostname())
        else:
            host = self.ServerIPLine.text()
        port = int(self.PortLine.text())
        alias = self.AliasLine.text()
        #connect
        self.sock = socket.socket()
        print("connecting to " + str(host) + ":" + str(port))
        self.sock.connect((host, port))
        #send alias
        msg_sttgs = "/alias=" + alias
        msg_sttgs_byt = bytes(msg_sttgs, 'utf-8')
        self.sock.send(msg_sttgs_byt)

        #Verbidnung mit dem Server aufbauen

        #Starten eines neuen Threads für den kontinuierlichen Empfang von Signalen. (QTCore.QThread sollte verwendet werden) -> dazu muss das receiver Signal aus der listener Klasse mit der Funktion print_message verbunden werden
        listener_recieve = listener(self.sock,self,self.app)
        #listener_recieve.__init__(sock,self)
        #listener_recieve.run(sock,self)
        listener_recieve.start()

        updater_send = updater(self)
        updater_send.start()

        # bckgrd_thrd = BackgroundThread(listener_recieve,self.app)
        # #bckgrd_thrd.__init__(listener_recieve)
        # #bckgrd_thrd.run()
        # bckgrd_thrd.start()

        while True:
            #time.sleep(1)
            #print("still running")
            self.app.processEvents()

        # # try:
        # #     while True:
        # #         msg = sock.recv(1024).decode()+'\n'
        # #         if msg:
        # #             #text_field.append(msg)
        # #             #time.sleep(0.1)
        # #             #hauptfenster.print_message(msg)  #freezes GUI
        # #             self.print_message(msg)
        # #             print(msg)
                
                
                
        # # finally:
        # #     print("connection lost")
        # #     #ADD DISCONNECT
        # #     #_thread.start_new_thread(reconnect)
    def send_msg(self,msg_clt):
        """
        Diese Funktion sendet die Nachricht.

        """
        msg_clt_byt = bytes(msg_clt, 'utf-8')
        #Senden der eingegebenen Daten
        self.sock.send(msg_clt_byt)


    def on_sendButtonClicked(self):
        """
        Diese Funktion wird aufgerufen, sobald der Sendeknopf gedrückt wird.

        """
        msg_clt = self.TextEingabe.toPlainText()
        self.send_msg(msg_clt)
        self.TextEingabe.clear()


    def print_message(self,msg):
        """
        Diese Funktion wird aufgerufen, sobald eine Nachricht empfangen wurde. Die Nachricht wird im Ausgabefenster angezeigt.  
        """
        # Implementierung.
        self.ChatText.append(msg)
        ##app = QtWidgets.QApplication(sys.argv) #update UI
        #self.app.processEvents()


    def on_disconnectButtonClicked(self):
        """
        Diese Funktion wird aufgerufen, sobald der Disconnectknopf gedrückt wird.

        """
        try:
            self.sock.detach()
            self.print_message("[successfully disconnected from server]")
            self.sock = socket.socket()
        except:
            print("[critical error in disconnect!]")
            self.print_message("[successfully disconnected from server]")
        #Implementierung.

    def on_helpButtonClicked(self):
        """
        Diese Funktion wird aufgerufen, sobald der Helpknopf gedrückt wird.
        
        """
        self.send_msg("/help")
        #Implementierung.

    def on_user_change(self,user_list):
        #self.UserList.clear()
        self.UserList.append(user_list)
        #self.UserList.setText(user_list)

#Erstellen eines neuen Threads, indem von der QThread Klasse geerbt wird.  
class listener(QtCore.QThread):

    receiver = QtCore.pyqtSignal(str) #Ein Signal erzeugen, welches einen 'str' übergeben kann. Namensgebung änderbar.
    def __init__(self,sock_client,hauptfenster_,app):
        QtCore.QThread.__init__(self) # Konstruktor der Elternklasse
        self.exiting = False
        self.sock = sock_client
        self.hauptfenster = hauptfenster_
        self.app = app
    def run(self):                
    # Implementieren der Empfangsschleife!
        try:
            while True:
                #app = QtWidgets.QApplication(sys.argv) #update UI
                self.app.processEvents()
                time.sleep(0.1)
                msg = self.sock.recv(1024).decode()+'\n'
                if msg:
                    time.sleep(0.1)
                    #self.UserList
                    #if "[" in msg and "]" in msg:
                        #print("detected server message")
                    if "[currently online:]" in msg:
                        user_list = msg[20:].replace("\t","")
                        self.hauptfenster.on_user_change(user_list)
                    else:
                        self.hauptfenster.print_message(msg)  #freezes GUI???
                        print(msg)
                #QtGui.QApplication.processEvents()  #existiert nicht
                
        finally:
            print("connection lost")
            #ADD DISCONNECT
            #_thread.start_new_thread(reconnect)

class updater(QtCore.QThread):
    def __init__(self,hauptfenster_):
        QtCore.QThread.__init__(self) # Konstruktor der Elternklasse
        self.exiting = False
        self.hauptfenster = hauptfenster_
    def run(self):
        try:
            while True:
                self.hauptfenster.send_msg("/users")
                time.sleep(.5)
        except:
            print("critical error in update message")

class BackgroundThread(QtCore.QThread):
    '''Keeps the main loop responsive'''

    def __init__(self, worker, app):
        super(BackgroundThread, self).__init__()
        self.exiting = False
        self.worker = worker
        self.app = app

    def run(self):
        '''This starts the thread on the start() call'''

        #while self.worker.running:
        while True:
            #app = QtWidgets.QApplication(sys.argv)
            self.app.processEvents()
            print("Updating the main loop")
            time.sleep(0.1)

# main Funktion
def main():
    app = QtWidgets.QApplication(sys.argv)

    form = Hauptfenster(app)

    form.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()