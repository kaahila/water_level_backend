from mqttClient import MQTTClient
from database_handler import Database
from datetime import datetime
from fastapi import FastAPI, Depends
from typing import Annotated
import uvicorn
import asyncio
import json
import os
import threading

app = FastAPI()

class MainClass:
    
    def __init__(self):
        # MQTT-Client-Instanz erstellen
        self.mqtt_client = MQTTClient(
            broker_address="restfulml.de",
            username="server",
            password="lf7istcool"
        )
        self.db = Database()

        #self.router = APIRouter()
        #self.router.add_api_route("/height", self.get_container_height, methods=["GET"])
        #self.router.add_api_route("/latestItem", self.get_latest_recod, methods=["GET"])
        #self.router.add_api_route("/items/{limit}", self.get_allRecords_database, methods=["GET"])
        #self.router.add_api_route("/hello", self.read_root, methods=["GET"])
    
    def run(self):        
        # MQTT-Client-Verbindung herstellen und Schleife starten
        self.mqtt_client.set_on_message(self.on_message)
        self.mqtt_client.connect()
        self.mqtt_client.loop_start()
        
        # Endlosschleife, um das Programm am Laufen zu halten
        while True:
            pass
    
    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload)
        self.add_record_database(value=self.calculate_water_lvl(payload["distance"]), created_on=payload["timestamp"])
        # Callback-Funktion für den Empfang einer Nachricht
        print(f"Nachricht empfangen auf Thema {msg.topic}: {msg.payload.decode()}")

    def add_record_database(self, value, created_on):
        self.db.add_record(value, created_on)
        print(value, created_on)
      
    def calculate_water_lvl(self, distance, container_height = 9):
        return container_height - distance
            
    def close_connection_database(self):
        self.db.close_connection()
        
    
    
def run_server():
    os.system("start /wait cmd /k python -m uvicorn main:app")

if __name__ == '__main__':
    x = threading.Thread(target=run_server)
    x.start()
    main = MainClass()
    main.run()
    
@app.get("/height")
async def get_container_height(main: Annotated[MainClass, Depends(MainClass)]):
    return main.container_height
    
@app.get("/items/{limit}")  
async def get_allRecords_database(limit: int = None):
    all_records = main.db.get_all_records(limit)
    return json.dumps(all_records)
    
@app.get("/latestItem")
async def get_latest_recod():
    latest_record = main.db.get_latest_record()
    return json.dump(latest_record)
        
@app.get("/hello") 
async def read_root(): return {"Hello": "World"}