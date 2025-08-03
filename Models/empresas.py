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
    