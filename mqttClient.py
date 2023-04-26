import paho.mqtt.client as mqtt
import random

class MQTTClient:
    def __init__(self, broker_address, broker_port=1883,keepalive=60, username=None, password=None):
        # Broker-Adresse, Port, Benutzername und Passwort speichern
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.keepalive = keepalive
        self.username = username
        self.password = password
        # Zufällige Client-ID mit Präfix "client-" und zufälliger Zahl zwischen 1 und 1000 generieren
        self.client_id = f"client-{random.randint(1, 1000)}"
        # MQTT-Client-Objekt erstellen und Callback-Funktionen setzen
        self.client = mqtt.Client(client_id=self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        
    def set_on_message(self, on_message):
        self.client.on_message = on_message

    def on_connect(self, client, userdata, flags, rc):
        # Callback-Funktion für den Verbindungsaufbau
        if rc == 0:
            client.subscribe("ovm_lf7_test_topic")
            print("Verbindung hergestellt.")
        else:
            print("Verbindung fehlgeschlagen. Fehlercode: " + str(rc))

    def on_disconnect(self, client, userdata, rc):
        # Callback-Funktion für die Trennung der Verbindung
        print("Verbindung getrennt. Code: " + str(rc))

    #def on_message(self, client, userdata, msg):
    #    # Callback-Funktion für den Empfang einer Nachricht
    #    print(f"Nachricht empfangen auf Thema {msg.topic}: {msg.payload.decode()}")

    def connect(self):
        # Verbindung zum Broker herstellen
        if self.username is not None and self.password is not None:
            self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker_address, self.broker_port, keepalive=self.keepalive)

    def disconnect(self):
        # Verbindung zum Broker trennen
        self.client.disconnect()

    def publish(self, topic, payload):
        # Nachricht an den Broker senden
        self.client.publish(topic, payload)

    def subscribe(self, topic):
        # Auf ein Thema abonnieren
        self.client.subscribe(topic)

    def loop_start(self):
        # MQTT-Schleife starten und auf eingehende Nachrichten warten
        self.client.loop_start()

    def loop_stop(self):
        # MQTT-Schleife beenden
        self.client.loop_stop()

    def loop(self, timeout=None):
        # MQTT-Schleife für eine bestimmte Zeit laufen lassen
        self.client.loop(timeout=timeout)