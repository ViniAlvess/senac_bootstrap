import mysql.connector  
from flask import Flask, render_template,request, url_for, flash, redirect 
from forms import formLogin , formNovoUsuario
from hashlib import sha256

app = Flask(__name__)

app.config ['SECRET_KEY'] = '65ad3ecb328fe2f1b810b1031f31d119'

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'P@$$w0rd',
    database = 'ead_senac',
)

@app.route('/')
def index(): 
    return render_template ('index.html')

@app.route('/base')
def base(): 
    return render_template('base.html')

@app.route('/cursos')
def cursos(): 
    return render_template('cursos.html')

@app.route('/login', methods=['get','post'])
def login(): 
    titulo ='Login de acesso'
    descricao = 'Formulario de login'
    
    form_login = formLogin()
    form_novo_usuario = formNovoUsuario()
    
    if form_login.validate_on_submit() and 'submitLogin' in request.form:
        flash(f'Login realizado com sucesso: {form_login.email.data}', 'alert-success')
        return redirect(url_for('index'))
    
    if form_novo_usuario.validate_on_submit() and 'submitCadastro' in request.form:
    
     cursor = mydb.cursor()

    
    return render_template('login.html',titulo=titulo,descricao=descricao,form_login=form_login,form_novo_usuario=form_novo_usuario)

@app.route('/ead')
def ead(): 
    return render_template('ead.html')

@app.route('/contato')
def contato(): 
    return render_template('contato.html')

if __name__ =='__main__':
    app.run(debug=True)