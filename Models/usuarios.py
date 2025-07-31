import os
from config import supabase
from flask import session
from werkzeug.utils import secure_filename
from Models.auth import Auth
import uuid

class Usuario:
    @staticmethod
    def upload_foto_perfil(file):
        if not file:
            return None, "Nenhum arquivo enviado."

        email = session.get('user', {}).get('email')
        if not email:
            return None, "Usuário não está logado."

        # Gera um nome único para o arquivo
        filename = secure_filename(file.filename)
        extensao = os.path.splitext(filename)[1]
        nome_arquivo = f"{uuid.uuid4()}{extensao}"

        try:
            # Upload para o bucket
            supabase.storage.from_('fotos_perfil').upload(nome_arquivo, file)

            # URL pública (ajuste o domínio conforme seu projeto Supabase)
            url_publica = f"https://<sua-instancia>.supabase.co/storage/v1/object/public/fotos_perfil/{nome_arquivo}"

            return url_publica, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def atualizar_dados(nome=None, bio=None, telefone=None, foto_perfil=None):
        email = session.get('user', {}).get('email')
        if not email:
            return None, "Usuário não está logado."

        dados_atualizados = {}

        if nome is not None:
            dados_atualizados['nome'] = nome
        if bio is not None:
            dados_atualizados['bio'] = bio
        if telefone is not None:
            dados_atualizados['telefone'] = telefone
        if foto_perfil is not None:
            dados_atualizados['foto_perfil'] = foto_perfil

        if not dados_atualizados:
            return None, "Nenhum dado fornecido para atualização."

        try:
            resultado = supabase.table('usuarios').update(dados_atualizados).eq('email', email).execute()
            return resultado, None
        except Exception as e:
            return None, str(e)
        
        
    @staticmethod
    def alterar_senha(senha_atual, nova_senha, confirmar_senha):
        email = session.get('user', {}).get('email')
        if not email:
            return None, "Usuário não autenticado."

        if nova_senha != confirmar_senha:
            return None, "As senhas não coincidem."

        if len(nova_senha) < 8:
            return None, "A nova senha deve ter no mínimo 8 caracteres."

        # Verifica se a senha atual está correta
        sessao, erro = Auth.login(email, senha_atual)
        if erro:
            return None, "Senha atual incorreta."

        try:
            resposta = supabase.auth.update_user({'password': nova_senha})
            if resposta.user:
                return True, None
            else:
                return None, "Erro desconhecido ao atualizar senha."
        except Exception as e:
            return None, str(e)