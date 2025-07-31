# models/estabelecimentos.py
from config import supabase

class Estabelecimento():
    @staticmethod
    def criar_empresas():
        try:
            response = supabase.table('empresas').insert({
            "usuario_id": 'usuario_id',
            "nome_fantasia": 'nome_fantasia',
            "cnpj": 'cnpj',
            "descricao": 'descricao',
            "endereco": 'endereco',
            "telefone": 'telefone'
            }).execute()
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