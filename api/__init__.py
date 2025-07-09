from flask import Flask, render_template, redirect, url_for, session, flash
from functools import wraps
from Controller.usuario_controller import usuario_bp
from Controller.auth_controller import auth_bp

app = Flask(__name__, template_folder='../templates', static_folder='../Static')
app.secret_key = '2895c134719b7d446e1a6f72746b500c33fcb93874b7a604965dad9dfa3d038d'

app.register_blueprint(usuario_bp)
app.register_blueprint(auth_bp)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from Models.auth import Auth
        user = Auth.get_usuario_atual()
        if user is None:
            flash("Você precisa estar logado para acessar esta página", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function



# Rota principal com nome específico
@app.route('/')
def index():  # Nomeie como 'index' para usar no url_for
    return render_template('index.html')

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