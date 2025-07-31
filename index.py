from flask import Flask, render_template, redirect, url_for, session, flash
from Controller.usuario_controller import usuario_bp
from Controller.auth_controller import auth_bp, login_required
from Controller.empresas_controller import estabelecimento_bp, buscar_empresas

app = Flask(__name__, template_folder='./templates', static_folder='./Static')
app.secret_key = '2895c134719b7d446e1a6f72746b500c33fcb93874b7a604965dad9dfa3d038d'

app.register_blueprint(usuario_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(estabelecimento_bp)


# Rota principal com nome específico
@app.route('/')
def index():  # Nomeie como 'index' para usar no url_for
    return redirect(url_for('home'))  # Redireciona para a rota principal

@app.route('/home')
def home():  # Nomeie como 'index' para usar no url_for
    user = session.get('user')  # Debug: Verifica se o usuário está na sessão
    if user:
        empresas = buscar_empresas()
        print('CU')  # Chama a função para buscar empresas
        print( empresas )  # Debug: Verifica se as empresas foram carregadas corretasmente
        
        return render_template('index.html', empresas=empresas, user=user)
    else:
        print('CU')
        return render_template('index.html', empresas=None)

# Rota principal com nome específico
@app.route('/minhas_empresas')
@login_required
def minhas_empresas():  # Nomeie como 'index' para usar no url_for
    return render_template('minhas_empresas.html')

# Rota principal com nome específico
@app.route('/editar_perfil')
@login_required
def editar_perfil():  # Nomeie como 'index' para usar no url_for
    return render_template('editar_perfil.html')

# Página de salões de beleza
@app.route('/saloes')
@login_required
def saloes():
    return render_template('saloes.html')

# Página mock de um salão específico
@app.route('/salao-mock')
@login_required
def salao_mock():
    return render_template('salao_mock.html')


if __name__ == '__main__':
    app.run(debug=True)