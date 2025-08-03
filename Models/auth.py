from config import supabase
from werkzeug.security import generate_password_hash

class Auth:
    @staticmethod
    def cadastrar_usuario(email: str, senha: str, nome: str, bio:str):
        """
        Cadastra novo usuário usando Supabase Auth
        Args:
            email: Email do usuário
            senha: Senha (será hasheada)
            dados_extras: Dados adicionais para a tabela de perfis
        Returns:
            Tuple (dict, error): Dados do usuário e erro (se houver)
        """
        try:
            # 1. Cadastro no sistema de autenticação
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": senha
            })

            # 2. Cadastro na tabela de usuários
            user_data = {
                "email": email,
                "nome": nome,
                "bio": bio
            }
            
            # 3. Insere na tabela de perfis
            profile_response = supabase.table('usuarios').insert(user_data).execute()
            
            if not profile_response.data:
                # Rollback se falhar
                supabase.auth.admin.delete_user(auth_response.user.id)
                return None, "Erro ao criar perfil do usuário"
            
            # 4. Retorna os dados formatados
            return {
                "id": auth_response.user.id,
                "email": email,
                "nome": nome,
                "bio": bio,
                "auth_user": auth_response.user  # Mantém o objeto original se necessário
            }, None
            
        except Exception as e:
            return None, str(e)

    @staticmethod
    def login(email: str, senha: str):
        """
        Autentica usuário
        Returns:
            Tuple (dict, error): Sessão do usuário e erro (se houver)
        """
        try:
            response = supabase.auth.sign_in_with_password({
                'email': email,
                'password': senha
            })
            return response, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_usuario_atual(access_token):
        # exemplo de como pegar usuário com Supabase
        try:
            usuario_response = supabase.auth.get_user(access_token)
            return usuario_response.user
        except Exception as e:
            print(f"Erro ao obter usuário: {e}")
            return None

    @staticmethod
    def logout():
        """Desloga o usuário"""
        return supabase.auth.sign_out()
    
    
    @staticmethod
    def buscar_usuario(usuario):
        """"
            Faz busca pelo usuario usando o email
        """
        dados_usuario = supabase.table('usuarios').select('*').eq('email', usuario.email).single().execute()
        return  dados_usuario