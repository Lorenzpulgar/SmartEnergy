import paho.mqtt.client as mqtt
import json
import subprocess
from guardar_mqtt_db import cargarDB


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("sensor/corriente")

def on_message(client, userdata, msg):
    valores_json = str(msg.payload, 'utf-8')
    valores = json.loads(valores_json)
    cargarDB(valores)
    print(valores)


def run():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("test.mosquitto.org", 1883, 60)
    client.loop_forever()


if __name__ == '__main__':
    run()
