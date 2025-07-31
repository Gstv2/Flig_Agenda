from config import supabase
from werkzeug.security import generate_password_hash

class Auth:
    @staticmethod
    def cadastrar_usuario(email: str, senha: str, dados_extras: dict = None):
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
            # 1. Cria usuário no Auth do Supabase
            auth_response = supabase.auth.sign_up({
                'email': email,
                'password': senha,
            })
            
            if auth_response.user is None:
                return None, "Erro ao criar usuário"
            
            # 2. Salva dados extras na tabela de perfis (se fornecido)
            if dados_extras:
                dados_extras['email'] = email
                
                profile_response = supabase.table('usuarios').insert(dados_extras).execute()
                
                if not profile_response.data:
                    # Rollback: remove usuário do Auth se falhar ao criar perfil
                    supabase.auth.admin.delete_user(auth_response.user.id)
                    return None, "Erro ao criar perfil do usuário"
            
            return auth_response.user, None
            
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