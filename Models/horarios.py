from flask import session
from config import supabase

class HorarioFuncionamento:
    @staticmethod
    def criar_horario(dados_horario):
        """Cria um novo horário de funcionamento"""
        try:
            response = supabase.table('horario_funcionamento').insert(dados_horario).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao criar horário: {e}")
            return None

    @staticmethod
    def buscar_todos_horarios():
        """Busca todos os horários de funcionamento"""
        try:
            response = supabase.table('horario_funcionamento').select('*').execute()
            return response.data
        except Exception as e:
            print(f"Erro ao buscar horários: {e}")
            return None
            
    @staticmethod
    def buscar_horario_por_empresa(empresa_id):
        """Busca horários por ID da empresa"""
        try:
            response = supabase.table('horario_funcionamento').select("*").eq("empresa_id", empresa_id).execute()
            return response.data if response.data else None
        except Exception as e:
            print(f"Erro ao buscar horários da empresa: {e}")
            return None

    @staticmethod
    def atualizar_horario(horario_id, dados_atualizados):
        """Atualiza um horário existente"""
        try:
            response = supabase.table('horario_funcionamento').update(dados_atualizados).eq('id', horario_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao atualizar horário: {e}")
            return None

    @staticmethod
    def deletar_horario(horario_id):
        """Remove um horário"""
        try:
            response = supabase.table('horario_funcionamento').delete().eq('id', horario_id).execute()
            return True if response.data else False
        except Exception as e:
            print(f"Erro ao deletar horário: {e}")
            return False
