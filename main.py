from mqttClient import MQTTClient
from database_handler import Database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import threading

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'])

container_height = 9

# MQTT-Client-Instanz erstellen
mqtt_client = MQTTClient(
    broker_address="restfulml.de",
    username="server",
    password="lf7istcool"
)
db = Database(url= "postgresql://lf7:lf7istcool@restfulml.de/lf7")

    #"postgresql://lf7:lf7istcool@restfulml.de/lf7"
    #"postgresql://postgres:postgres@192.168.43.148/postgres"

def run():        
    # MQTT-Client-Verbindung herstellen und Schleife starten
    mqtt_client.set_on_message(on_message)
    mqtt_client.connect()
    mqtt_client.loop_start()
    
    # Endlosschleife, um das Programm am Laufen zu halten
    while True:
        pass

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    add_record_database(value=calculate_water_lvl(payload["distance"]), created_on=payload["timestamp"])
    # Callback-Funktion für den Empfang einer Nachricht
    print(f"Nachricht empfangen auf Thema {msg.topic}: {msg.payload.decode()}")

def add_record_database(value, created_on):
    db.add_record(value, created_on)
    
def calculate_water_lvl(distance):
    return container_height - distance
        
def close_connection_database():
    db.close_connection()
    
@app.get("/height")
async def get_container_height():
    return container_height
    
@app.get("/items")  
async def get_allRecords_database(limit: int|None = 20):
    all_records = db.get_all_records(limit)
    return all_records
    
@app.get("/latestItem")
async def get_latest_recod():
    latest_record = db.get_latest_record()
    return latest_record
        
@app.get("/hello") 
async def read_root(): return {"Hello": "World"}
        
    
    
def run_server():
    os.system("start /wait cmd /k python -m uvicorn main:app --host 0.0.0.0")

if __name__ == '__main__':
    x = threading.Thread(target=run_server)
    x.start()
    run()
    
