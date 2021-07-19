from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

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
