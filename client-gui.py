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

    def __init__(self, app, parent = None):
        super(Hauptfenster, self).__init__(parent)                      # Ausführen der __init__ der Elternklasse
        self.setupUi(self)                                              # Initialisierung des User Interface
        self.app = app

        # Signals and Slots der einzelnen Elemente verbinden (Ein guter Anfang sind eine Sendebox und eine Anzeige für das Chatprotokoll)
        #button = QPushButton("connect")
        self.ConnectButton.clicked.connect(self.on_connectButtonClicked) 
        self.SendButton.clicked.connect(self.on_sendButtonClicked)
        self.DisconnectButton.clicked.connect(self.on_disconnectButtonClicked)
        self.HelpButton.clicked.connect(self.on_helpButtonClicked)
        self.ChatText.ensureCursorVisible()

    def on_connectButtonClicked(self):
        """
        Diese Funktion wird aufgerufen, sobald der Verbindenknopf gedrückt wird.

        """
        #read inputs
        try:
            self.ChatText.clear()
            toggle_local_host = self.toggleLocalHost.checkState()
            if toggle_local_host:
                print("using local host")
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
        except:
            print("Connect failed")
            self.print_message("[connection failed]")
            self.on_disconnectButtonClicked()
        #Verbidnung mit dem Server aufbauen

        #Starten eines neuen Threads für den kontinuierlichen Empfang von Signalen. (QTCore.QThread sollte verwendet werden) -> dazu muss das receiver Signal aus der listener Klasse mit der Funktion print_message verbunden werden
        listener_recieve = listener(self.sock,self,self.app)
        listener_recieve.start()

        while True:
            self.app.processEvents()


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
        self.ChatText.append(msg)
        self.ChatText.moveCursor(QtGui.QTextCursor.End)


    def on_disconnectButtonClicked(self):
        """
        Diese Funktion wird aufgerufen, sobald der Disconnectknopf gedrückt wird.

        """
        try:
            self.sock.detach()
            self.sock = socket.socket()
            time.sleep(.2)
            self.ChatText.clear()
            self.print_message("[successfully disconnected from server]")
        except:
            print("[critical error in disconnect!]")
            self.print_message("[successfully disconnected from server]")

    def on_helpButtonClicked(self):
        """
        Diese Funktion wird aufgerufen, sobald der Helpknopf gedrückt wird.
        
        """
        self.send_msg("/help")


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
                self.app.processEvents()
                time.sleep(0.1)
                msg = self.sock.recv(1024).decode()+'\n'
                if msg:
                    self.hauptfenster.print_message(msg)  
                    print(msg)
                
        except:
            print("connection lost")


# main Funktion
def main():
    app = QtWidgets.QApplication(sys.argv)

    form = Hauptfenster(app)

    form.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()