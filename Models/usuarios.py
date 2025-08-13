import os
import time
import uuid
from flask import session
from Models.auth import Auth
from config import supabase


class Usuario:
    @staticmethod
    def upload_foto_perfil(file):
        """Faz upload da foto para o Supabase Storage, substituindo a anterior"""
        try:
            # Verificações iniciais
            if 'user' not in session or 'email' not in session['user']:
                return None, "Usuário não autenticado"

            email = session['user']['email']
            
            # 1. Busca dados atuais do usuário
            user_response = supabase.table('usuarios').select('foto_perfil').eq('email', email).execute()
            user_data = user_response.data[0] if user_response.data else None
            
            # 2. Remove a foto antiga se existir
            if user_data and user_data.get('foto_perfil'):
                try:
                    old_url = user_data['foto_perfil']
                    old_filename = old_url.split('/')[-1].split('?')[0]
                    delete_response = supabase.storage.from_('fotosperfil').remove([old_filename])
                    if hasattr(delete_response, 'error'):
                        print(f"Erro ao deletar arquivo antigo: {delete_response.error}")
                except Exception as e:
                    print(f"Exceção ao remover arquivo antigo: {str(e)}")

            # 3. Validação do novo arquivo
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in ('.jpg', '.jpeg', '.png', '.gif'):
                return None, "Formato de imagem inválido (use JPG, PNG ou GIF)"

            # 4. Gera novo nome de arquivo
            filename = f"profile_{email}_{uuid.uuid4()}{ext}"
            file_content = file.read()

            # 5. Upload da nova foto
            upload_response = supabase.storage.from_('fotosperfil').upload(
                file=file_content,
                path=filename,
                file_options={
                    "content-type": file.content_type,
                    "cache-control": "public, max-age=31536000"
                }
            )

            if hasattr(upload_response, 'error'):
                return None, f"Erro no upload: {upload_response.error}"

            # 6. Gera URL pública (sem timestamp inicialmente)
            new_url = supabase.storage.from_('fotosperfil').get_public_url(filename)
            
            # 7. Atualiza no banco de dados
            update_response = supabase.table('usuarios').update(
                {'foto_perfil': new_url}
            ).eq('email', email).execute()
            
            if hasattr(update_response, 'error'):
                return None, f"Erro ao atualizar perfil: {update_response.error}"

            # 8. Retorna URL com timestamp para evitar cache
            return f"{new_url}?t={int(time.time())}", None

        except Exception as e:
            return None, f"Erro interno: {str(e)}"
        finally:
            file.seek(0)


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