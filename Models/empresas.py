# models/estabelecimentos.py
from config import supabase

class Empresas():
    @staticmethod
    def criar_empresas(dados_empresa):
        try:
            response = supabase.table('empresas').insert(dados_empresa).execute()
            return response.data
        except Exception as e:
            print(f"Erro ao cadastrar empresa: {e}")
            return None

    @staticmethod
    def buscar_empresas():
        try:
            response = supabase.table('empresas').select('*').execute()
            print(response)
            return response.data
        except Exception as e:
            print(f"Erro ao buscar empresas: {e}")
            return None
            
    @staticmethod
    def buscar_empresa_id(id):
        try:
            response = supabase.table('empresas').select("*").eq("id", id).execute()
            print(response)
            return response.data[0]
        except Exception as e:
            print(f"Erro ao buscar empresa: {e}")
            return None
        
    @staticmethod
    def buscar_empresas_por_usuario(usuario_id):
        try:
            # Assumindo que há um campo 'usuario_id' na tabela empresas
            response = supabase.table('empresas').select("*").eq("usuario_id", usuario_id).execute()
            print(response)
            return response.data
        except Exception as e:
            print(f"Erro ao buscar empresas por usuário: {e}")
            return None