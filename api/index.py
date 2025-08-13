from datetime import datetime
from flask import Flask, render_template, redirect, url_for, session, flash, request
from urllib.parse import unquote  # Adicione no topo do arquivo
from Controller.usuario_controller import usuario_bp
from Controller.horarios_controller import get_horarios_disponiveis, horario_bp, get_horarios_empresa, formatar_horarios, horarios_disponiveis_dict
from Controller.auth_controller import auth_bp, login_required, buscar_usuario_email
from Controller.empresas_controller import empresas_bp, buscar_empresas, buscar_empresa_id, buscar_empresa_categoria, buscar_empresa_por_id
from Controller.servicos_controller import servicos_bp, listar_servicos 

app = Flask(__name__, template_folder='../templates', static_folder='../Static')
app.secret_key = '2895c134719b7d446e1a6f72746b500c33fcb93874b7a604965dad9dfa3d038d'
app.register_blueprint(usuario_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(empresas_bp)
app.register_blueprint(horario_bp)
app.register_blueprint(servicos_bp)


# Rota principal com nome específico
@app.route('/')
def index():  # Nomeie como 'index' para usar no url_for
    return redirect(url_for('home'))  # Redireciona para a rota principal

@app.route('/home')
def home():  # Nomeie como 'index' para usar no url_for
    user = session.get('user', {})
    empresas = buscar_empresas()
    
    if user and empresas:
        return render_template('index.html', empresas=empresas, user=user)
    elif empresas:
        return render_template('index.html', user=None, empresas=empresas)
    elif user:
        return render_template('index.html', user=user, empresas=None)
    else:
        return render_template('index.html', user=None, empresas=None)

# Rota principal com nome específico
@app.route('/minhas_empresas')
@login_required
def minhas_empresas():  # Nomeie como 'index' para usar no url_for
    user = session.get('user', {})
    user_email = user.get('email')
    usuario_response = buscar_usuario_email(user_email)
    
    if not usuario_response or not usuario_response.data:
        flash("Usuário não encontrado no banco de dados", "error")
        return redirect(url_for('auth.login'))
        
    usuario_id = usuario_response.data.get('id')
    if not usuario_id:
        flash("ID do usuário não encontrado na resposta", "error")
        return redirect(url_for('auth.login'))
    print("esse é o ID do user", usuario_id)
    empresas = buscar_empresa_por_id(usuario_id)
    print(empresas)
    print(len(empresas))
    # Contagem total de empresas
    countEmpresas = len(empresas)
    countAtivas = sum(1 for empresa in empresas if empresa.get('Ativo') == True)

    print(countEmpresas)
        # Ou alternativamente, se 'Ativo' for string:
        # countAtivas = sum(1 for empresa in empresas if str(empresa.get('Ativo', '')).lower() == 'true')
    if empresas:
        return render_template('minhas_empresas.html', user=user, empresas=empresas, countEmpresas=countEmpresas, countAtivas=countAtivas)
    else:
        return render_template('minhas_empresas.html', user=user, empresas=None, countEmpresas = 0, countAtivas = 0)
    

# Rota principal com nome específico
@app.route('/editar_perfil')
@login_required
def editar_perfil():
    user = session.get('user', {})
    return render_template('editar_perfil.html', user=user)

@app.route("/empresas/<categoria>")
def empresas_por_categoria(categoria):
    user = session.get('user', {})
    categoria_decodificada = unquote(categoria)
    empresas = buscar_empresa_categoria(categoria_decodificada) or []
    return render_template("empresas.html",empresas=empresas,categoria=categoria_decodificada, user=user)

@app.route('/empresa/selecionar/<int:id_empresa>')
def selecionar_empresa(id_empresa):
    print(f"Buscando empresa ID: {id_empresa}")
    
    empresas = buscar_empresa_id(id_empresa)  # Agora fica claro que retorna uma lista
    print('Empresas encontradas:', empresas)
    
    if not empresas:  # Se a lista estiver vazia
        flash("Empresa não encontrada", "error")
        return redirect(url_for('home'))
    
    empresa = empresas[0]  # Pega o primeiro item da lista
    
    try:
        nome_slug = empresa['nome_fantasia']
        session['empresa_id'] = id_empresa
        print('mostrando aonde está o erro',session['empresa_id'] )
        session.modified = True
        return redirect(url_for('base_empresa', nome_empresa=nome_slug))
    except KeyError:
        flash("Dados da empresa incompletos", "error")
        return redirect(url_for('home'))



@app.route('/empresa/<nome_empresa>')
def base_empresa(nome_empresa):
    user = session.get('user', {})
    id_empresa = session.get('empresa_id')
    
    if not id_empresa:
        flash("Sessão expirada, selecione a empresa novamente", "error")
        return redirect(url_for('home'))
    
    empresas = buscar_empresa_id(id_empresa)
    
    if not empresas:
        flash("Empresa não encontrada", "error")
        return redirect(url_for('home'))
    
    empresa = empresas[0]
    
    # Buscar horários de funcionamento
    horarios = get_horarios_empresa(id_empresa)
    
    # Formatar horários para exibição
    horarios_formatados = formatar_horarios(horarios) if horarios else None
    
    # Buscar serviços da empresa (você precisará implementar esta função)
    servicos = listar_servicos(id_empresa)
    
    data_agendamento = request.args.get('data')
    horarios_disponiveis = []
    
    if data_agendamento:
        dados = horarios_disponiveis_dict(id_empresa, data_agendamento)
        if dados and 'slots' in dados:
            horarios_disponiveis = dados['slots']
    
    return render_template('base_empresa.html', 
                         empresa=empresa, 
                         user=user,
                         horarios=horarios_formatados,
                         servicos=servicos,
                         horarios_disponiveis=horarios_disponiveis,
                         data_agendamento=data_agendamento)
    
@app.template_filter('format_data_br')
def format_data_br(value):
    """Filtro para formatar data no formato brasileiro"""
    if not value:
        return ''
    try:
        data = datetime.strptime(value, '%Y-%m-%d')
        return data.strftime('%d/%m/%Y')
    except ValueError:
        return value
    

@app.route('/dashboard-empresa/<int:id_empresa>')
@login_required
def dashboard_empresa(id_empresa):
    user = session.get('user', {})
    empresa = buscar_empresa_id(id_empresa)[0]
    servicos = listar_servicos(id_empresa)
    return render_template('dashboard_empresa.html', user=user, empresa=empresa, servicos=servicos)

@app.route('/editar-empresa/<int:id_empresa>')
@login_required
def editar_empresa(id_empresa):
    user = session.get('user', {})
    empresa = buscar_empresa_id(id_empresa)[0]
    return render_template('editar_empresa.html', user=user, empresa=empresa)

if __name__ == '__main__':
    app.run(debug=True)