from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from Models.auth import Auth
from functools import wraps

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    user = session.get('user', {})
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Cadastra o usuário
        usuario, erro = Auth.cadastrar_usuario(email, senha, nome, bio='')
        
        if erro:
            erro_str = str(erro).lower()

            if 'invalid login credentials' in erro_str:
                flash("E-mail ou senha incorretos. Verifique e tente novamente.", 'error')
            elif 'email not confirmed' in erro_str or 'confirm your email' in erro_str:
                flash("E-mail ainda não confirmado. Verifique sua caixa de entrada ou spam.", 'error')
            elif 'user already registered' in erro_str or 'email' in erro_str and 'already' in erro_str:
                flash("Este e-mail já está cadastrado. Faça login ou recupere sua senha.", 'error')
            elif 'invalid email' in erro_str or 'email format' in erro_str:
                flash("Formato de e-mail inválido. Digite um endereço válido.", 'error')
            elif ('password' in erro_str and 'character' in erro_str) or 'weak password' in erro_str:
                flash("A senha deve conter no mínimo 8 caracteres, incluindo letras maiúsculas, minúsculas, números e símbolos especiais.", 'error')
            elif 'too many' in erro_str and 'attempts' in erro_str:
                flash("Muitas tentativas de login. Aguarde alguns minutos antes de tentar novamente.", 'error')
            else:
                flash(f"Erro: {erro}", 'error')

            return redirect(url_for('auth.cadastro'))

        # Faz login automático
        sessao, erro_login = Auth.login(email, senha)
        if erro_login:
            flash("Cadastro realizado! Faça login para continuar.", "success")
            return redirect(url_for('auth.login'))

        # Armazena dados na sessão - FORMA CORRETA
        session['user'] = {
            'id': usuario['id'],  # Agora é garantido ser um dicionário
            'email': usuario['email'],
            'nome': usuario['nome'],
            'bio': usuario.get('bio', ''),
            'access_token': sessao.session.access_token
        }

        flash("Cadastro e login realizados com sucesso!", 'success')
        return redirect(url_for('index'))
    
    return render_template('registro.html', user=user)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    user = session.get('user', {})
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        sessao, erro = Auth.login(email, senha)
        
        if erro:
            erro_str = str(erro).lower()
            if 'invalid login credentials' in erro_str:
                flash("E-mail ou senha incorretos. Verifique e tente novamente.", 'error')
            elif 'email not confirmed' in erro_str:
                flash("E-mail ainda não confirmado. Verifique sua caixa de entrada.", 'error')
            elif 'password' in erro_str and 'character' in erro_str:
                flash("A senha deve conter no mínimo 8 caracteres, incluindo letras maiúsculas, minúsculas, números e símbolos especiais.", 'error')
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
    
    return render_template('login.html', user=user)



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
