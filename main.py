from flask import Flask, render_template, request, redirect, url_for, flash, Response, stream_with_context
from flaskext.mysql import MySQL
from decouple import config
import random
import json
import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,login_user,logout_user,login_required,current_user,UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
db = SQLAlchemy(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = config('USER_DB')
app.config['MYSQL_DATABASE_PASSWORD'] = config('PASSWORD_DB')
app.config['MYSQL_DATABASE_DB'] = config('NAME_DB')
mysql.init_app(app)


app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///prueba.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'bx99xa4xa6x1axc9x10irxfexdeex12x0esx98dfsfsdfsdfsd'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/test'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'iniciarsesion' 


class usuarios(UserMixin,db.Model):
    __tablename__='usuarios'
    id = db.Column(db.Integer,  primary_key = True)
    nombre = db.Column(db.String(50), unique= True,nullable=False)
    contraseña = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(50), unique=True,nullable=False)
    telefono = db.Column(db.String(50),nullable=False)
    fecha = db.Column(db.DateTime, default = datetime.now)


@login_manager.user_loader
def load_user(user_id):
    return usuarios.query.get(int(user_id))

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

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    
    if not current_user.is_authenticated:
        if request.method == 'POST':

            lon_nom =len(request.form.get('nombre'))
            lon_pass =len(request.form.get('clave')) 
            lon_email =len(request.form.get('email')) 
            if lon_nom != 0 and lon_email != 0 and lon_pass != 0:

                nombre_existente = usuarios.query.filter_by(nombre=request.form.get('nombre')).first()
                email_existente = usuarios.query.filter_by(email=request.form.get('email')).first()

                if nombre_existente:
                    flash('El nombre de usuario ya existe, intenta con otro', 'error')
                elif email_existente:
                    flash('El correo proporcionado ya existe, intenta con otro', 'error')
                elif request.form.get('clave') != request.form.get('confirClave'):
                    flash('La contraseña proporcionada no coincide','error')

                else:

                    codificar_clave = generate_password_hash(request.form.get('clave'), method = 'sha256')
                    nuevo_usuario = usuarios(nombre = request.form.get('nombre'), contraseña = codificar_clave, email= request.form.get('email'), telefono = request.form.get('telefono') ) 
                    db.session.add(nuevo_usuario)
                    db.session.commit()

                    flash(' Te has registrado exitosamente.','exito')

                    return redirect(url_for('iniciarsesion'))
            else:
                flash('No dejes espacios en blanco, todos los campos son abligatorios','error')
        
        return render_template('registro.html')
    return redirect(url_for('perfil'))

@app.route('/iniciarsesion',methods=['GET','POST'])
def iniciarsesion():
    if not current_user.is_authenticated:
        if request.method == 'POST':

            usuario = usuarios.query.filter_by(nombre = request.form.get('nombre')).first()

            if usuario and check_password_hash(usuario.contraseña, request.form.get('clave')):

                login_user(usuario, remember=request.form.get('recordar'))
            
                return redirect('/perfil')
            
            flash('La contraseña o el usuario no coinciden','error')

        return render_template('login.html')
    return redirect('/perfil')

@app.route('/perfil', methods=['GET','POST'])
@login_required
def perfil():
    user = current_user
    return render_template('perfil.html', user=user)

@app.route('/salir')
@login_required
def salir():
    logout_user()
    return redirect('/')

@app.route('/dashboard')
@login_required
def monitoreo():
    return render_template('dashboard.html')

@app.route('/carga1')
def carga1():
    return render_template('carga1.html')

@app.route('/carga2')
def carga2():
    return render_template('carga2.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    
