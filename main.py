from twisted.internet import reactor, protocol
import random
import time
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
import threading
from kivy.utils import platform
from plyer import accelerometer

#Window.size = (340, 620)
Window.clearcolor = (46/255, 46/255, 46/255)

if platform == 'android':
    perms = ['android.permission.INTERNET']
    from android.permissions import request_permissions
    request_permissions(perms, None)

class DataSender(protocol.Protocol):
    #def send_data(self):
    #    """Envoie des données aléatoires au serveur."""
    #    if self.transport:
    #        x = round(random.uniform(-40, 40))
    #        y = round(random.uniform(-40, 40))
    #        z = round(random.uniform(-40, 40))
    #        message = f"{x},{y},{z}\n"
    #        self.transport.write(message.encode("utf-8"))
    #        reactor.callLater(0.1, self.send_data)  # Appelle la fonction toutes les 100ms
#
    #def connectionMade(self):
    #    print("Connecté au serveur, envoi des données...")
    #    self.send_data()
    def connectionMade(self):
        print("Connecté au serveur, prêt à recevoir les données de l'accéléromètre.")

class DataSenderFactory(protocol.ClientFactory):
    def __init__(self, window):
        self.window = window

    def buildProtocol(self, addr):
        protocol_instance = DataSender()
        self.window.protocol = protocol_instance
        return protocol_instance

    

def thread(function):
    def wrap(*args, **kwargs):
        t = threading.Thread(target=function, args=args, kwargs=kwargs, daemon=True)
        t.start()
        return t
    return wrap

class FirstWindow(Screen):
    def __init__(self, **kwargs):
        super(FirstWindow,self).__init__(**kwargs)
        self.serv_ip = ""
        self.sensor = False
        self.protocol = None

    def set_serv_ip(self):
        self.serv_ip = self.ids.ip.text
        #self.ids.label_ip.text = "Adress IP set to : " + self.serv_ip
        self.connect_to_server(self.serv_ip)

    @thread
    def connect_to_server(self, IP):
        
        reactor.connectTCP(IP, 8000, DataSenderFactory(self))
        if not reactor.running:
            reactor.run(installSignalHandlers=False)

    def toggle_accelerometer(self):
        if not self.sensor:
            try:
                accelerometer.enable()
                self.sensor = True
            except:
                self.ids.label_ip.text = "Erreur lors de l'activation de l'accéléromètre"
            
            if self.sensor:
                Clock.schedule_interval(self.update_accelerometer, 0.1)
                self.ids.label_ip.text = "Accéléromètre activé"
        else:
            accelerometer.disable()
            Clock.unschedule(self.update_accelerometer)
            self.sensor = False

    def update_accelerometer(self, dt):
        try:
            val = accelerometer.acceleration[:3]
            if val and self.protocol and self.protocol.transport:
                x, y, z = val
                message = f"{x:.2f},{y:.2f},{z:.2f}\n"
                self.ids.data.text = f"x: {x:.0f}, y: {y:.0f}, z: {z:.0f}"
                self.protocol.transport.write(message.encode("utf-8"))
        except:
            self.ids.label_ip.text = "Erreur lors de la lecture de l'accéléromètre"


class WindowManager(ScreenManager):
    pass

class ClientApp(App):
    def build(self):
        return Builder.load_file("client.kv")
    
if __name__ == "__main__":
    ClientApp().run()