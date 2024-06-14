from flask import Flask, render_template, request, redirect, url_for, flash, Response, stream_with_context
from flask_mysqldb import MySQL
from decouple import config
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import time

app = Flask(__name__)

# Configuración de base de datos SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{config("USER_DB")}:{config("PASSWORD_DB")}@{config("HOST_DB")}/{config("NAME_DB")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'bx99xa4xa6x1axc9x10irxfexdeex12x0esx98dfsfsdfsdfsd'

db = SQLAlchemy(app)

# Configuración de base de datos MySQL para Flask-MySQLdb
app.config['MYSQL_DATABASE_HOST'] = config('HOST_DB')
app.config['MYSQL_DATABASE_USER'] = config('USER_DB')
app.config['MYSQL_DATABASE_PASSWORD'] = config('PASSWORD_DB')
app.config['MYSQL_DATABASE_DB'] = config('NAME_DB')
mysql = MySQL(app)

# Configuración de Flask-Bcrypt
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'iniciarsesion'

class Usuarios(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    contraseña = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now)

    def set_password(self, password):
        self.contraseña = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.contraseña, password)

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

def _datos(cur):
    cur.execute('SELECT fecha1, corriente1, potencia1, consumo1 FROM datos_tiempo_real1 WHERE id = (SELECT MAX(id) FROM datos_tiempo_real1)')
    datos_tiempo_real1 = cur.fetchall()
    cur.execute('SELECT fecha2, corriente2, potencia2, consumo2 FROM datos_tiempo_real2 WHERE id = (SELECT MAX(id) FROM datos_tiempo_real2)')
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
    cur = mysql.connection.cursor()
    enviar = _datos(cur)
    return Response(stream_with_context(enviar), mimetype='text/event-stream')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('perfil'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        clave = request.form.get('clave')
        confirClave = request.form.get('confirClave')

        if clave != confirClave:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('registro'))

        nuevo_usuario = Usuarios(nombre=nombre, email=email, telefono=telefono)
        nuevo_usuario.set_password(clave)  # Aquí se utiliza set_password para almacenar la contraseña de forma segura
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Cuenta creada exitosamente. Ahora puedes iniciar sesión.', 'exito')
        return redirect(url_for('iniciarsesion'))

    return render_template('registro.html')


@app.route('/iniciarsesion', methods=['GET', 'POST'])
def iniciarsesion():
    if not current_user.is_authenticated:
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            contraseña = request.form.get('clave')
            usuario = Usuarios.query.filter_by(nombre=nombre).first()

            if usuario and usuario.check_password(contraseña):  # Utiliza check_password para verificar la contraseña
                login_user(usuario, remember=request.form.get('recordar'))
                return redirect('/perfil')
            else:
                flash('La contraseña o el usuario no coinciden', 'error')

        return render_template('login.html')
    return redirect('/perfil')

@app.route('/perfil', methods=['GET', 'POST'])
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
    with app.app_context():
        db.create_all()
    app.run(debug=True)
