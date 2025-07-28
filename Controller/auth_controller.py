from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from Models.auth import Auth
from functools import wraps

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        dados_extras = {'nome': nome}
        
        usuario, erro = Auth.cadastrar_usuario(email, senha, dados_extras)
        
        if erro:
            flash(f"Erro no cadastro: {erro}", 'error')
            return redirect(url_for('auth.cadastro'))  # Usando blueprint
        
        flash("Cadastro realizado com sucesso! Faça login.", 'success')
        return redirect(url_for('index'))  # Redireciona para a rota raiz
    
    return render_template('registro.html')  # Renderiza diretamente

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        sessao, erro = Auth.login(email, senha)
        
        if erro:
            flash(f"Erro no login: {erro}", 'error')
            return redirect(url_for('auth.login'))  # Usando blueprint
        
        session['user_token'] = sessao.session.access_token
        flash("Login realizado com sucesso!", 'success')
        return redirect(url_for('index'))  # Redireciona para a rota raiz
    
    return render_template('login.html')  # Renderiza diretamente

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

@auth_bp.route('/logout')
def logout():
    print("teste")
    Auth.logout()
    session.pop('user_token', None)
    flash("Você foi deslogado com sucesso.", 'info')
    return redirect(url_for('auth.login'))  # Redireciona para a rota raiz