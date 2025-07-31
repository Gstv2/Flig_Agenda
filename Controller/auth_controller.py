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

        # Primeiro, tenta cadastrar
        usuario, erro = Auth.cadastrar_usuario(email, senha, dados_extras)
        
        if erro:
            if 'User already registered' in erro:
                flash("Este e-mail já está em uso. Tente fazer login ou recupere sua senha.", 'error')
            elif 'Password should contain at least' in erro:
                flash("A senha deve ter no mínimo 8 caracteres, incluindo letras maiúsculas, minúsculas, números e símbolos especiais.", 'error')
            else:
                flash(f"Erro ao cadastrar: {erro}", 'error')
            return redirect(url_for('auth.cadastro'))

        # Depois do cadastro, tenta fazer login
        sessao, erro_login = Auth.login(email, senha)

        if erro_login:
            flash("Cadastro feito, mas houve um erro ao logar. Faça login manualmente.", "warning")
            return redirect(url_for('auth.login'))

        # Armazena dados na sessão
        session['user'] = {
            'id': usuario.id,
            'email': usuario.email,
            'nome': usuario.user_metadata.get('nome'),
            'bio': usuario.user_metadata.get('bio'),  # ← aqui
            'access_token': sessao.session.access_token
        }


        flash("Cadastro e login realizados com sucesso!", 'success')
        return redirect(url_for('index'))
    
    return render_template('registro.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        sessao, erro = Auth.login(email, senha)
        
        if erro:
            if 'Invalid login credentials' in erro:
                flash("E-mail ou senha incorretos. Verifique e tente novamente.", 'error')
            elif 'Email not confirmed' in erro:
                flash("E-mail ainda não confirmado. Verifique sua caixa de entrada.", 'error')
            else:
                flash(f"Erro ao fazer login: {erro}", 'error')
            return redirect(url_for('auth.login'))

        print("Acessando a rota principal")
        # Pega dados do usuário via token
        usuario = Auth.get_usuario_atual(sessao.session.access_token)
        
        # Armazena dados básicos da sessão do Supabase Auth
        session['user'] = {
            'id': usuario.id,
            'email': usuario.email,
            'access_token': sessao.session.access_token
        }

        # Busca dados extras da tabela 'usuarios' no Supabase
        dados_usuario = Auth.buscar_usuario(usuario)

        if dados_usuario.data:
            session['user'].update({
                'nome': dados_usuario.data.get('nome'),
                'bio': dados_usuario.data.get('bio'),
                'foto_perfil': dados_usuario.data.get('foto_perfil'),
                'telefone': dados_usuario.data.get('telefone')
            })
            flash("Login realizado com sucesso!", 'success')
            return redirect(url_for('index'))
        else:
            print("Usuário não encontrado na tabela 'usuarios'.")
    
    return render_template('login.html')



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Você precisa estar logado para acessar esta página.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/logout')
def logout():
    if 'user' in session:
        Auth.logout()  # Sem argumento
        session.clear()
        flash("Você foi deslogado com sucesso.", 'info')
    return redirect(url_for('auth.login'))
