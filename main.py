from flask import Flask, render_template, request, redirect, url_for, flash, Response, stream_with_context
from flaskext.mysql import MySQL
from decouple import config
import random
import json
import time


app = Flask(__name__)


mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = config('USER_DB')
app.config['MYSQL_DATABASE_PASSWORD'] = config('PASSWORD_DB')
app.config['MYSQL_DATABASE_DB'] = config('NAME_DB')
mysql.init_app(app)


def _datos(cur):
    cur.execute(
        'SELECT fecha1, corriente1, potencia1, consumo1 FROM datos_tiempo_real1 WHERE id = (SELECT MAX(id) FROM datos_tiempo_real1)')
    datos_tiempo_real1 = cur.fetchall()
    cur.execute(
        'SELECT fecha2, corriente2, potencia2, consumo2 FROM datos_tiempo_real2 WHERE id = (SELECT MAX(id) FROM datos_tiempo_real2)')
    datos_tiempo_real2 = cur.fetchall()

    json_data = json.dumps({
            'fecha1': datos_tiempo_real1[0][0], 'corriente1': datos_tiempo_real1[0][1], 
            'potencia1': datos_tiempo_real1[0][2], 'consumo1': datos_tiempo_real1[0][3],
            'fecha2': datos_tiempo_real2[0][0], 'corriente2': datos_tiempo_real2[0][1], 
            'potencia2': datos_tiempo_real2[0][2], 'consumo2': datos_tiempo_real2[0][3],
            'fecha_total': time.strftime("%H: %M: %S"),
            'corriente_total': datos_tiempo_real1[0][1] + datos_tiempo_real2[0][1],
            'potencia_total': datos_tiempo_real1[0][2] + datos_tiempo_real2[0][2],
            'consumo_total': datos_tiempo_real1[0][3] + datos_tiempo_real2[0][3],
        })
 
    return f"data:{json_data}\n\n"

@app.route('/datos_monitoreo')
def datos_monitoreo1():
    cur = mysql.get_db().cursor()

    enviar = _datos(cur)

    return Response(stream_with_context(enviar), mimetype='text/event-stream')   

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

if __name__ == '__main__':
    app.run(debug=True)
    
