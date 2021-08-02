import mysql.connector
import time
from decouple import config


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
    hora = time.strftime("%H: %M: %S")
    fecha = time.strftime("%d/%m/%Y")
    cur.execute('INSERT INTO datos_tiempo_real1 (fecha1, corriente1, potencia1, consumo1) VALUES ("{fecha1}", {corriente1}, {potencia1}, {consumo1})'.format(
        fecha1=hora, corriente1=valores['corriente1'], potencia1=valores['potencia1'], consumo1=valores['consumo1']
    ))

    cur.execute('INSERT INTO datos_tiempo_real2 (fecha2, corriente2, potencia2, consumo2) VALUES ("{fecha2}", {corriente2}, {potencia2}, {consumo2})'.format(
        fecha2=hora, corriente2=valores['corriente2'], potencia2=valores['potencia2'], consumo2=valores['consumo2']
    ))


def cargarDB(valores):
    mydb = conectarDB()
    guardarDB(mydb, valores)
