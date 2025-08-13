from config import supabase
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class Agendamento:
    @staticmethod
    def criar_agendamento(usuario_id, empresa_id, servico_id, data_agendamento, hora_inicio, hora_fim):
        try:
            # Verifica conflitos de horário
            conflitos = supabase.table('agendamento').select('*').match({
                'empresa_id': empresa_id,
                'data_agendamento': data_agendamento
            }).or_(f'Hora_inicio.lte.{hora_fim},Hora_Fim.gte.{hora_inicio}').execute()
            
            if conflitos.data:
                return None, "Já existe um agendamento neste horário"
            
            novo_agendamento = {
                'usuario_id': usuario_id,
                'empresa_id': empresa_id,
                'servico_id': servico_id,
                'status': 'pendente',
                'data_agendamento': data_agendamento,
                'Hora_inicio': hora_inicio,
                'Hora_Fim': hora_fim
            }
            
            response = supabase.table('agendamento').insert(novo_agendamento).execute()
            return response.data[0] if response.data else None, None
            
        except Exception as e:
            logger.error(f"Erro ao criar agendamento: {str(e)}")
            return None, str(e)

    @staticmethod
    def listar_agendamentos_usuario(usuario_id):
        try:
            response = supabase.table('agendamento').select('*, empresa(*), servico(*)').eq('usuario_id', usuario_id).execute()
            return response.data, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def listar_agendamentos_empresa_data(empresa_id, data_agendamento):
        try:
            response = (
                supabase
                .table('agendamento')
                .select('*, usuario(*), servico(*)')
                .eq('empresa_id', empresa_id)
                .eq('data_agendamento', data_agendamento)
                .execute()
            )
            return response.data or [], None  # Garante que seja lista
        except Exception as e:
            return [], str(e)  # Também retorna lista no erro
        
    @staticmethod
    def listar_agendamentos_empresa_data(empresa_id, data_agendamento):
        try:
            response = supabase.table('agendamento').select('*, usuario(*), servico(*)').eq('empresa_id', empresa_id).eq("data_agendamento", data_agendamento).execute()
            return response.data or [], None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def atualizar_status(agendamento_id, novo_status):
        try:
            response = supabase.table('agendamento').update({'status': novo_status}).eq('id', agendamento_id).execute()
            return response.data[0] if response.data else None, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def cancelar_agendamento(agendamento_id, usuario_id):
        try:
            # Verifica se o agendamento pertence ao usuário
            agendamento = supabase.table('agendamento').select('*').eq('id', agendamento_id).eq('usuario_id', usuario_id).execute()
            
            if not agendamento.data:
                return None, "Agendamento não encontrado ou não pertence ao usuário"
            
            response = supabase.table('agendamento').update({'status': 'cancelado'}).eq('id', agendamento_id).execute()
            return response.data[0] if response.data else None, None
        except Exception as e:
            return None, str(e)