
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
from widgets import Jauge 

# Définition de la couleur de fond de la fenêtre
Window.clearcolor = (46/255, 46/255, 46/255)

Builder.load_file('jauge.kv')

# Demande de permissions si l'application tourne sur Android
if platform == 'android':
    perms = ['android.permission.INTERNET']  # Permission pour accéder à Internet
    from android.permissions import request_permissions
    request_permissions(perms, None)

# Classe définissant le protocole pour la connexion avec le serveur
class DataSender(protocol.Protocol):
    def __init__(self, window):
        self.window = window 

    def connectionMade(self):  
        self.window.ids.status.text = "Connected"

    
    def connectionLost(self, reason):
        self.window.ids.status.text = "Disconnected"  

# Classe définissant la fabrique pour la gestion de la connexion client
class DataSenderFactory(protocol.ClientFactory):
    def __init__(self, window):
        self.window = window  # Référence à la fenêtre pour mise à jour

    def buildProtocol(self, addr):
        protocol_instance = DataSender(self.window)
        self.window.protocol = protocol_instance  # Stockage de l'instance du protocole
        return protocol_instance

# Décorateur pour exécuter une fonction dans un thread séparé
def thread(function):
    def wrap(*args, **kwargs):
        t = threading.Thread(target=function, args=args, kwargs=kwargs, daemon=True)
        t.start()
        return t
    return wrap

# Définition de la première fenêtre de l'application
class FirstWindow(Screen):
    def __init__(self, **kwargs):
        super(FirstWindow,self).__init__(**kwargs)
        self.serv_ip = ""  # Stocke l'adresse IP du serveur
        self.sensor = False  # Indique si l'accéléromètre est activé ou non
        self.protocol = None  # Stocke l'instance du protocole réseau
        self.text_status = "disconnect"

    def set_serv_ip(self):
        self.serv_ip = self.ids.ip.text  # Récupère l'adresse IP entrée par l'utilisateur
        self.connect_to_server(self.serv_ip)  # Lance la connexion au serveur

    @thread  # Exécute la connexion au serveur dans un thread séparé
    def connect_to_server(self, IP):
          # Mise à jour de l'état de connexion
        reactor.connectTCP("localhost", 8000, DataSenderFactory(self))  # Connexion au serveur via Twisted
        
        #self.ids.status.text = f"Connexion au serveur..."  # Mise à jour de l'interface
        if not reactor.running:
            reactor.run(installSignalHandlers=False)  # Démarrage du réacteur Twisted

    def update_status_text(self, new_text):
        def _update(dt):
            self.ids.status.text = new_text
            self.ids.status.texture_update()  # <== Forcer le recalcul du rendu
        Clock.schedule_once(_update)

    def toggle_accelerometer(self):
        if not self.sensor:
            try:
                accelerometer.enable()  # Activation de l'accéléromètre
                self.sensor = True
            except:
                self.ids.label_ip.text = "Erreur lors de l'activation de l'accéléromètre"
            
            if self.sensor:
                
                Clock.schedule_interval(self.update_accelerometer, 0.1)  # Mise à jour toutes les 0.1 secondes
                self.ids.label_ip.text = "Accéléromètre activé"
        else:
            accelerometer.disable()  # Désactivation de l'accéléromètre
            Clock.unschedule(self.update_accelerometer)  # Arrêt de la mise à jour
            self.sensor = False

    def update_accelerometer(self, dt):
        try:
            val = accelerometer.acceleration[:3]  # Récupération des valeurs (x, y, z)
            if val and self.protocol and self.protocol.transport:
                x, y, z = val
                x = int(x)
                y = int(y)
                z = int(z)
                message = f"{x},{y},{z}\n"  # Formatage des données
                self.ids.data.text = f"x: {x:.0f}, y: {y:.0f}, z: {z:.0f}"  # Mise à jour de l'affichage
                self.protocol.transport.write(message.encode("utf-8"))  # Envoi des données au serveur
        except:
            self.ids.label_ip.text = "Erreur lors de la lecture de l'accéléromètre"

# Définition de la deuxième fenêtre de l'application (vide pour l'instant)
class SecondWindow(Screen):
    pass

# Gestionnaire d'écrans de l'application
class WindowManager(ScreenManager):
    pass

# Définition de l'application Kivy
class ClientApp(App):
    def build(self):
        return Builder.load_file("client.kv")  # Chargement du fichier de description de l'interface

# Lancement de l'application
if __name__ == "__main__":
    ClientApp().run()
