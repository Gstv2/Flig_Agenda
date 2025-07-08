from flask import Flask, render_template
from Controller.usuario_controller import usuario_bp

app = Flask(__name__, template_folder='View/templates', static_folder='View/Static')

app.register_blueprint(usuario_bp)

# Rota principal com nome específico
@app.route('/')
def index():  # Nomeie como 'index' para usar no url_for
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Página de login
@app.route('/login')
def login():
    return render_template('login.html')

# Página de registro
@app.route('/registro')
def registro():
    return render_template('registro.html')

# Página de salões de beleza
@app.route('/saloes')
def saloes():
    return render_template('saloes.html')

# Página mock de um salão específico
@app.route('/salao-mock')
def salao_mock():
    return render_template('salao_mock.html')


if __name__ == '__main__':
    app.run(debug=True)