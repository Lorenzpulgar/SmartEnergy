import mysql.connector
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
    cur.execute('INSERT INTO datos_tiempo_real (fecha_adquisicion, numero1, numero2) VALUES ("{fecha_adquisicion}", {numero1}, {numero2})'.format(
        fecha_adquisicion=valores['fecha'], numero1=valores['numero1'], numero2=valores['numero2']))


def cargarDB(valores):
    mydb = conectarDB()
    guardarDB(mydb, valores)
