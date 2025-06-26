from src.config import supabase

class Usuario:
    @staticmethod
    def cadastrar(nome, email, senha):
        dados = {
            "nome": nome,
            "email": email,
            "senha": senha  # Em produção, use hashing seguro!
        }
        resposta = supabase.table("Usuario").insert(dados).execute()
        return resposta
