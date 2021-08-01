from flask import Flask, render_template, request, redirect, url_for, flash, Response, stream_with_context
from flaskext.mysql import MySQL
import mysql.connector
import paho.mqtt.client as mqtt
import json
import subprocess
from decouple import config
import json


app = Flask(__name__)


mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = config('USER_DB')
app.config['MYSQL_DATABASE_PASSWORD'] = config('PASSWORD_DB')
app.config['MYSQL_DATABASE_DB'] = config('NAME_DB')
mysql.init_app(app)


def _datos(cur):
    cur.execute(
        'SELECT fecha_adquisicion, numero1, numero2 FROM datos_tiempo_real WHERE id = (SELECT MAX(id) FROM datos_tiempo_real)')
    datos_tiempo_real = cur.fetchall()

    json_data = json.dumps(
        {'fecha': datos_tiempo_real[0][0], 'numero1': datos_tiempo_real[0][1], 'numero2': datos_tiempo_real[0][2]})

    yield f"data:{json_data}\n\n"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/dashboard')
def monitoreo():
    return render_template('dashboard.html')

@app.route('/carga1')
def carga1():
    return render_template('carga1.html')

@app.route('/carga2')
def carga2():
    return render_template('carga2.html')

@app.route('/datos_monitoreo')
def datos_monitoreo():
    cur = mysql.get_db().cursor()

    enviar = _datos(cur)

    return Response(stream_with_context(enviar), mimetype='text/event-stream')

## Guardar MQTT
def conectarDB():
    mydb = mysql.connector.connect(
        host='localhost',
        user=config('USER_DB'),
        password=config('PASSWORD_DB'),
        database=config('NAME_DB')
    )

    return mydb


def guardarDB(mydb, valores):
    cur = mydb.cursor()
    cur.execute('INSERT INTO datos_tiempo_real (fecha_adquisicion, numero1, numero2) VALUES ("{fecha_adquisicion}", {numero1}, {numero2})'.format(
        fecha_adquisicion=valores['fecha'], numero1=valores['numero1'], numero2=valores['numero2']))


def cargarDB(valores):
    mydb = conectarDB()
    guardarDB(mydb, valores)

## Recibir MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("sensor_corriente")
    #mqtt.subscribe("sensor_corriente")

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
    app.run(debug=True)
    
