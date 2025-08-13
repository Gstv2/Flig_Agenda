from config import supabase
import logging

logger = logging.getLogger(__name__)

class Servico:
    @classmethod
    def criar_servico(cls, dados_servico):
        """Cria um novo serviço associado a uma empresa"""
        try:
            response = supabase.table('servicos').insert({
                'empresa_id': dados_servico['empresa_id'],
                'nome': dados_servico['nome'],
                'descricao': dados_servico.get('descricao', ''),
                'preco': dados_servico['preco']
            }).execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Erro ao criar serviço: {str(e)}")
            return None

    @classmethod
    def buscar_servicos_empresa(cls, empresa_id):
        """Busca todos os serviços de uma empresa"""
        try:
            response = supabase.table('servicos') \
                .select('*') \
                .eq('empresa_id', empresa_id) \
                .execute()
            
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Erro ao buscar serviços: {str(e)}")
            return []

    @classmethod
    def deletar_servico(cls, servico_id):
        """Remove um serviço pelo ID"""
        try:
            response = supabase.table('servicos') \
                .delete() \
                .eq('id', servico_id) \
                .execute()
            
            return True if response.data else False
        except Exception as e:
            logger.error(f"Erro ao deletar serviço: {str(e)}")
            return False

    @classmethod
    def atualizar_servico(cls, servico_id, dados_atualizados):
        """Atualiza um serviço existente"""
        try:
            response = supabase.table('servicos') \
                .update(dados_atualizados) \
                .eq('id', servico_id) \
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Erro ao atualizar serviço: {str(e)}")
            return None
        
        
    @classmethod
    def buscar_servico_por_id(cls, servico_id):
        """Busca um serviço específico por ID"""
        try:
            response = supabase.table('servicos') \
                .select('*') \
                .eq('id', servico_id) \
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Erro ao buscar serviço por ID: {str(e)}")
            return None