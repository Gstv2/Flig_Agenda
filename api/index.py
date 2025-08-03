from flask import Flask, render_template, redirect, url_for, session, flash
from Controller.usuario_controller import usuario_bp
from Controller.auth_controller import auth_bp, login_required
from Controller.empresas_controller import empresas_bp, buscar_empresas

app = Flask(__name__, template_folder='../templates', static_folder='../Static')
app.secret_key = '2895c134719b7d446e1a6f72746b500c33fcb93874b7a604965dad9dfa3d038d'

app.register_blueprint(usuario_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(empresas_bp)


# Rota principal com nome específico
@app.route('/')
def index():  # Nomeie como 'index' para usar no url_for
    return redirect(url_for('home'))  # Redireciona para a rota principal

@app.route('/home')
def home():  # Nomeie como 'index' para usar no url_for
    user = session.get('user', {})
    print('tomar no cu')
    print(user.get('email'), user.get('nome'), user.get('bio'))
    print(user)# Debug: Verifica se o usuário está na sessão
    if user:
        empresas = buscar_empresas()
        return render_template('index.html', empresas=empresas, user=user)
    else:
        return render_template('index.html', user=None, empresas=None)

# Rota principal com nome específico
@app.route('/minhas_empresas')
@login_required
def minhas_empresas():  # Nomeie como 'index' para usar no url_for
    return render_template('minhas_empresas.html')

# Rota principal com nome específico
@app.route('/editar_perfil')
@login_required
def editar_perfil():
    user = session.get('user')
    return render_template('editar_perfil.html', user=user)

# Página de salões de beleza
@app.route('/saloes')
@login_required
def saloes():
    return render_template('saloes.html')

# Página mock de um salão específico
@app.route('/base_empresa')
@login_required
def base_empresa():
    return render_template('base_empresa.html')


if __name__ == '__main__':
    app.run(debug=True)