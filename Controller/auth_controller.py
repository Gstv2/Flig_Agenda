from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from Models.auth import Auth

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
            return redirect(url_for('auth.cadatro'))  # Usando blueprint
        
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

@auth_bp.route('/logout')
def logout():
    Auth.logout()
    session.pop('user_token', None)
    flash("Você foi deslogado com sucesso.", 'info')
    return redirect(url_for('index'))  # Redireciona para a rota raiz