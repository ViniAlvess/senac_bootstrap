import mysql.connector  
from flask import Flask, render_template,request, url_for, flash, redirect , session , send_from_directory
from forms import formLogin , formNovoUsuario, formCadastroProduto
from hashlib import sha256
from flask_uploads import UploadSet, IMAGES, configure_uploads

app = Flask(__name__)

app.config ['SECRET_KEY'] = '65ad3ecb328fe2f1b810b1031f31d119'
app.config ['UPLOADES_PHOTOS_DEST'] = 'uploads'

upload = UploadSet('photos', IMAGES)
configure_uploads(app, upload)

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
        
        cursor = mydb.cursor()
        
        email = form_login.email.data
        senha = form_login.senha.data
        hashSenha = sha256 (senha.encode())
        
        comando = f'Select * from alunos where email = "{email}"'
        cursor.execute(comando)
        result = cursor.fetchall()
        
        if hashSenha.hexdigest() == result[0][5]:
            session['nome_usuario'] = result [0][1]
            
            flash(f'Login realizado com sucesso: {form_login.email.data}', 'alert-success')
            return redirect(url_for('index'))
        else : 
            flash(f'Usuario ou senha incorreta para : {form_login.email.data}', 'alert-danger')
            return redirect(url_for('login'))
    if form_novo_usuario.validate_on_submit() and 'submitCadastro' in request.form:
    
        cursor = mydb.cursor()
        
        nome = form_novo_usuario.nome.data
        telefone = form_novo_usuario.celular.data
        email = form_novo_usuario.email.data
        cpf = form_novo_usuario.cpf.data
        senha = form_novo_usuario.senha.data
        hashSenha = sha256(senha.encode())
        
        query = f'INSERT INTO alunos (nome,email,telefone,cpf,senha) VALUES ("{nome}","{email}","{telefone}","{cpf}","{hashSenha.hexdigest()}")'
        print(query)
        cursor.execute(query)
        mydb.commit()
        
        flash(f'Cadastro realizado com sucesso: {form_novo_usuario.nome.data}' , 'alert-success')
        return redirect(url_for('index'))

    
    return render_template('login.html',titulo=titulo,descricao=descricao,form_login=form_login,form_novo_usuario=form_novo_usuario)

@app.route('/ead')
def ead(): 
    return render_template('ead.html')

@app.route('/contato')
def contato(): 
    return render_template('contato.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/uploads/<filename')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename )

@app.route('/cadastro_curso', methods=['GET','POST'])
def cadastrocurso():
    if session.get("nome_usuario"):
        titulo = 'Cdastro de curso'

if __name__ =='__main__':
    app.run(debug=True)