from config import supabase

class Usuario:
    @staticmethod
    def cadastrar(nome, email, senha):
        # 1. Cadastra no Auth (com segurança total)
        resultado_auth = supabase.auth.sign_up({
            "email": email,
            "password": senha
        })

        if resultado_auth.user is None:
            return {"error": resultado_auth}

        # 2. Armazena nome e email na sua tabela Usuario
        dados = {
            "nome": nome,
            "email": email
        }

        # Se quiser vincular o Supabase Auth ao seu sistema, você pode adicionar o `user_id`:
        # dados["user_id"] = resultado_auth.user.id

        resultado_dados = supabase.table("usuarios").insert(dados).execute()
        return resultado_dados
