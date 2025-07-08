from flask import Blueprint, render_template, request, redirect, url_for
from Models.usuarios import Usuario

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        Usuario.cadastrar(nome, email, senha)
        return redirect(url_for('usuario.cadastro'))

    return render_template('cadastro.html')


