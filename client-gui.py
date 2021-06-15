from chat_client_ui import Ui_MainWindow # Hier wird das eigene Design geladen
import sys
from PyQt5 import QtWidgets,QtCore # Erforderliche QT Bibliotheken werden importiert!
import socket

# Dies ist ein Template und soll als Denkanstoß dienen. Trotzdem sollten alle Funktionen verstanden werden und die Aufgabe nicht durch ausprobieren gelöst werden.

sock = socket.socket()

# Hauptfenster erbt von dem Designer Ergebnis und von einer QT Klasse
class Hauptfenster(QtWidgets.QMainWindow, Ui_MainWindow): 

    def __init__(self, parent = None):
        super(Hauptfenster, self).__init__(parent)                      # Ausführen der __init__ der Elternklasse
        self.setupUi(self)                                              # Initialisierung des User Interface


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
            host = "localhost"
        else:
            host = self.ServerIPLine.text()
        port = str(self.PortLine.text())
        alias = self.AliasLine.text()
        #connect
        sock = socket.socket()
        print("connecting to " + str(host) + ":" + str(port))
        sock.connect((host, port))
        #send alias
        msg_sttgs = "/alias=" + alias
        msg_sttgs_byt = bytes(msg_sttgs, 'utf-8')
        sock.send(msg_sttgs_byt)

        # Verbidnung mit dem Server aufbauen

        # Starten eines neuen Threads für den kontinuierlichen Empfang von Signalen. (QTCore.QThread sollte verwendet werden) -> dazu muss das receiver Signal aus der listener Klasse mit der Funktion print_message verbunden werden


    def on_sendButtonClicked(self):
        """
        Diese Funktion wird aufgerufen, sobald der Sendeknopf gedrückt wird.

        """

        #Implementierung.

    def print_message(self,msg):
        """
        Diese Funktion wird aufgerufen, sobald eine Nachricht empfangen wurde. Die Nachricht wird im Ausgabefenster angezeigt.  
        """
        # Implementierung.


    def on_disconnectButtonClicked(self):
        """
        Diese Funktion wird aufgerufen, sobald der Disconnectknopf gedrückt wird.

        """

        #Implementierung.

    def on_helpButtonClicked(self):
        """
        Diese Funktion wird aufgerufen, sobald der Helpknopf gedrückt wird.

        """

        #Implementierung.        

# #Erstellen eines neuen Threads, indem von der QThread Klasse geerbt wird.  
# class listener(QtCore.QThread):
#     receiver = QtCore.pyqtSignal(str) #Ein Signal erzeugen, welches einen 'str' übergeben kann. Namensgebung änderbar.
#     def __init__(self):
#         QtCore.QThread.__init__(self) # Konstruktor der Elternklasse
#         self.exiting = False

#     def run(self):                     
#     # Implementieren der Empfangsschleife!

# main Funktion
def main():
    app = QtWidgets.QApplication(sys.argv)

    form = Hauptfenster()
    form.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()