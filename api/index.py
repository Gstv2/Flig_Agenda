from flask import Flask, render_template, redirect, url_for, session, flash, request
from Controller.usuario_controller import usuario_bp
from Controller.auth_controller import auth_bp, login_required
from Controller.empresas_controller import empresas_bp, buscar_empresas, buscar_empresa_id, buscar_empresa_categoria

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
    if user:
        empresas = buscar_empresas()
        return render_template('index.html', empresas=empresas, user=user)
    else:
        return render_template('index.html', user=None, empresas=None)

# Rota principal com nome específico
@app.route('/minhas_empresas')
@login_required
def minhas_empresas():  # Nomeie como 'index' para usar no url_for
    user = session.get('user', {})
    return render_template('minhas_empresas.html', user=user)

# Rota principal com nome específico
@app.route('/editar_perfil')
@login_required
def editar_perfil():
    user = session.get('user')
    return render_template('editar_perfil.html', user=user)

@app.route("/empresas/<categoria>")
def empresas_por_categoria(categoria):
    user = session.get('user', {})
    empresas = buscar_empresa_categoria(categoria) or []
    return render_template("empresas.html",empresas=empresas,categoria=categoria, user=user)

@app.route('/empresa/selecionar/<int:id_empresa>')
@login_required
def selecionar_empresa(id_empresa):
    print(f"Buscando empresa ID: {id_empresa}")
    
    empresa = buscar_empresa_id(id_empresa)
    print('teste',empresa)
    
    if not empresa:
        flash("Empresa não encontrada", "error")
        print('Empresa não encontrada')
        return redirect(url_for('home'))
    
    # Verificação adicional de tipo
    if isinstance(empresa, dict):
        try:
            nome_slug = empresa['nome_fantasia']
            session['empresa_id'] = id_empresa
            session.modified = True
            return redirect(url_for('base_empresa', nome_empresa=nome_slug))
        except KeyError:
            flash("Dados da empresa incompletos", "error")
            print('Dados da empresa incompletos')
            return redirect(url_for('home'))
    else:
        flash("Formato de dados inválido para a empresa", "error")
        print('Formato de dados inválido para a empresa')
        return redirect(url_for('home'))



@app.route('/empresa/<nome_empresa>')
@login_required
def base_empresa(nome_empresa):
    user = session.get('user', {})
    print(f"Sessão atual: {session}")  # Debug
    id_empresa = session.get('empresa_id')
    
    if not id_empresa:
        print("ID não encontrado na sessão")  # Debug
        flash("Sessão expirada, selecione a empresa novamente", "error")
        return redirect(url_for('home'))
    
    empresa = buscar_empresa_id(id_empresa)
    print(f"Empresa encontrada: {empresa}")  # Debug
    
    if not empresa:
        flash("Empresa não encontrada", "error")
        return redirect(url_for('home'))
    
    return render_template('base_empresa.html', empresa=empresa, user=user)

@app.route('/dashboard-empresa')
def dashboard_empresa():
    user = session.get('user', {})
    return render_template('dashboard_empresa.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)