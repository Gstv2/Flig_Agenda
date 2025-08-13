from flask import session
from config import supabase

class HorarioFuncionamento:
    @classmethod
    def criar_horario(cls, dados):
        try:
            # Verifica se já existe um horário para esta empresa/dia
            response = supabase.table('horario_funcionamento') \
                .select('*') \
                .eq('empresa_id', dados['empresa_id']) \
                .eq('dia_semana', dados['dia_semana']) \
                .execute()
            
            if response.data:
                # Atualiza o horário existente
                response = supabase.table('horario_funcionamento') \
                    .update({
                        'manha_abertura': dados.get('manha_abertura'),
                        'manha_fechamento': dados.get('manha_fechamento'),
                        'tarde_abertura': dados.get('tarde_abertura'),
                        'tarde_fechamento': dados.get('tarde_fechamento'),
                        'noite_abertura': dados.get('noite_abertura'),
                        'noite_fechamento': dados.get('noite_fechamento')
                    }) \
                    .eq('id', response.data[0]['id']) \
                    .execute()
            else:
                # Cria um novo horário
                response = supabase.table('horario_funcionamento').insert({
                    'empresa_id': dados['empresa_id'],
                    'dia_semana': dados['dia_semana'],
                    'manha_abertura': dados.get('manha_abertura'),
                    'manha_fechamento': dados.get('manha_fechamento'),
                    'tarde_abertura': dados.get('tarde_abertura'),
                    'tarde_fechamento': dados.get('tarde_fechamento'),
                    'noite_abertura': dados.get('noite_abertura'),
                    'noite_fechamento': dados.get('noite_fechamento')
                }).execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
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
            print(response.data)
            return response.data 
            
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

    # Adicione este método ao seu HorarioFuncionamento model
    @staticmethod
    def deletar_horarios_empresa(empresa_id):
        """Remove todos os horários de uma empresa"""
        try:
            response = supabase.table('horario_funcionamento').delete().eq('empresa_id', empresa_id).execute()
            return True if response.data else False
        except Exception as e:
            print(f"Erro ao deletar horários da empresa: {e}")
            return False
        
    @staticmethod
    def buscar_horario_por_id(horario_id):
        """Busca um horário específico por ID"""
        try:
            response = supabase.table('horario_funcionamento').select('*').eq('id', horario_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao buscar horário por ID: {e}")
            return None