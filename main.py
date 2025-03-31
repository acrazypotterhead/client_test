#from twisted.internet import reactor, protocol
import random
import time
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
import threading
Window.size = (340, 620)
Window.clearcolor = (46/255, 46/255, 46/255)


#class DataSender(protocol.Protocol):
#    def send_data(self):
#        """Envoie des données aléatoires au serveur."""
#        if self.transport:
#            x = round(random.uniform(-40, 40))
#            y = round(random.uniform(-40, 40))
#            z = round(random.uniform(-40, 40))
#            message = f"{x},{y},{z}\n"
#            self.transport.write(message.encode("utf-8"))
#            reactor.callLater(0.1, self.send_data)  # Appelle la fonction toutes les 100ms
#
#    def connectionMade(self):
#        print("Connecté au serveur, envoi des données...")
#        self.send_data()
#
#class DataSenderFactory(protocol.ClientFactory):
#    protocol = DataSender

    #def clientConnectionFailed(self, connector, reason):
    #    print("Connexion échouée, tentative de reconnexion...")
    #    reactor.callLater(2, connector.connect)  # Réessaie après 2 secondes
#
    #def clientConnectionLost(self, connector, reason):
    #    print("Connexion perdue, tentative de reconnexion...")
    #    reactor.callLater(2, connector.connect)  # Réessaie après 2 secondes

# Démarre le client et connecte-le au serveur sur le port 8000
#reactor.connectTCP("localhost", 8000, DataSenderFactory())
#reactor.run()

#def thread(function):
#    def wrap(*args, **kwargs):
#        t = threading.Thread(target=function, args=args, kwargs=kwargs, daemon=True)
#        t.start()
#        return t
#    return wrap
#
class FirstWindow(Screen):
    def __init__(self, **kwargs):
        super(FirstWindow,self).__init__(**kwargs)
        self.serv_ip = ""

    #def set_serv_ip(self):
    #    self.serv_ip = self.ids.ip.text
    #    #self.ids.label_ip.text = "Adress IP set to : " + self.serv_ip
    #    self.connect_to_server(self.serv_ip)
#
    #@thread
    #def connect_to_server(self, IP):
#
    #    reactor.connectTCP(IP, 8000, DataSenderFactory())
    #    if not reactor.running:
    #        reactor.run(installSignalHandlers=False)
#


class WindowManager(ScreenManager):
    pass

class ClientApp(App):
    def build(self):
        return Builder.load_file("client.kv")
    
if __name__ == "__main__":
    ClientApp().run()