from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from Models.usuarios import Usuario
from Controller.auth_controller import login_required

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/atualizar_dados', methods=['POST'])
def atualizar_dados_usuario():
    nome = request.form.get('nome')
    bio = request.form.get('bio')
    telefone = request.form.get('telefone')
    file = request.files.get('foto_perfil')

    url_foto = None
    if file and file.filename != "":
        url_foto, erro_upload = Usuario.upload_foto_perfil(file)
        if erro_upload:
            flash(f"Erro ao enviar foto de perfil: {erro_upload}", 'error')
            return redirect(url_for('index'))

    # Atualiza os dados no Supabase
    resultado, erro = Usuario.atualizar_dados(nome, bio, telefone, url_foto)

    if erro:
        flash(f"Erro ao atualizar dados: {erro}", 'error')
    else:
        # Atualiza a sessão diretamente com os dados fornecidos
        session['user'].update({
            'nome': nome,
            'bio': bio,
            'telefone': telefone,
        })

        if url_foto:
            session['user']['foto_perfil'] = url_foto

        flash("Dados atualizados com sucesso!", 'success')

    return redirect(url_for('index'))



@usuario_bp.route('/alterar_senha', methods=['POST'])
def alterar_senha():
    senha_atual = request.form.get('senha_atual')
    nova_senha = request.form.get('nova_senha')
    confirmar_senha = request.form.get('confirmar_senha')

    sucesso, erro = Usuario.alterar_senha(senha_atual, nova_senha, confirmar_senha)

    if erro:
        flash(erro, 'error')
    else:
        flash("Senha atualizada com sucesso!", 'success')

    return redirect(url_for('index'))  # ou outra rota de retorno
