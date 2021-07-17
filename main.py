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

if __name__ == '__main__':
    app.run(debug=True)
