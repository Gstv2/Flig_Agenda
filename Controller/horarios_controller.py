from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, session, flash, redirect, url_for
from Models.horarios import HorarioFuncionamento
from Models.agendamentos import Agendamento
from Controller.auth_controller import login_required
import logging

horario_bp = Blueprint('horario', __name__, url_prefix='/horarios')
logger = logging.getLogger(__name__)

def formatar_horarios(horarios_data):
    """
    Formata os horários para exibição no template
    """
    if not horarios_data:
        return "Horários não definidos"
    
    # Verifica se é uma lista de dicionários (dados) ou Response
    if hasattr(horarios_data, 'data'):
        horarios = horarios_data.data
    else:
        horarios = horarios_data
    
    # Restante da função permanece igual
    grupos = {}
    
    for horario in horarios:
        if not isinstance(horario, dict):
            continue
            
        chave = (
            horario.get('manha_abertura'),
            horario.get('manha_fechamento'),
            horario.get('tarde_abertura'),
            horario.get('tarde_fechamento'),
            horario.get('noite_abertura'),
            horario.get('noite_fechamento')
        )
        
        if chave not in grupos:
            grupos[chave] = []
        grupos[chave].append(horario.get('dia_semana'))
    
    # Ordenar os dias da semana
    ordem_dias = [
        'Segunda-feira',
        'Terça-feira',
        'Quarta-feira',
        'Quinta-feira',
        'Sexta-feira',
        'Sábado',
        'Domingo'
    ]
    
    partes = []
    
    for horario, dias in grupos.items():
        # Ordenar os dias
        dias_ordenados = sorted(dias, key=lambda x: ordem_dias.index(x))
        
        # Formatar o range de dias
        if len(dias_ordenados) > 1:
            primeiro_dia = dias_ordenados[0].split('-')[0]
            ultimo_dia = dias_ordenados[-1].split('-')[0]
            range_dias = f"{primeiro_dia} - {ultimo_dia}"
        else:
            range_dias = dias_ordenados[0].split('-')[0]
        
        # Formatar os períodos
        periodos = []
        
        # Manhã
        if horario[0] and horario[1]:
            periodos.append(f"{horario[0]} - {horario[1]}")
        
        # Tarde
        if horario[2] and horario[3]:
            periodos.append(f"{horario[2]} - {horario[3]}")
        
        # Noite
        if horario[4] and horario[5]:
            periodos.append(f"{horario[4]} - {horario[5]}")
        
        if periodos:
            partes.append(f"{range_dias}: {' e '.join(periodos)}")
    
    return "<br>".join(partes) if partes else "Horários não definidos"

@horario_bp.route('/agendar-multiplos', methods=['POST'])
@login_required
def agendar_multiplos_horarios():
    """Permite agendamento de múltiplos slots de horário"""
    try:
        user = session.get('user')
        if not user:
            return jsonify({"error": "Usuário não autenticado"}), 401
        
        data = request.json
        empresa_id = data.get('empresa_id')
        servico_id = data.get('servico_id')
        slots = data.get('slots', [])  # Lista de horários selecionados
        
        if not all([empresa_id, servico_id, slots]):
            return jsonify({"error": "Dados incompletos"}), 400
        
        # Ordenar slots por horário
        slots_ordenados = sorted(slots, key=lambda x: x['inicio'])
        
        agendamentos_criados = []
        erros = []
        
        # Agrupar slots contíguos
        grupos = []
        grupo_atual = [slots_ordenados[0]]
        
        for slot in slots_ordenados[1:]:
            ultimo_fim = grupo_atual[-1]['fim']
            if slot['inicio'] == ultimo_fim:
                grupo_atual.append(slot)
            else:
                grupos.append(grupo_atual)
                grupo_atual = [slot]
        
        grupos.append(grupo_atual)
        
        # Criar agendamentos para cada grupo
        for grupo in grupos:
            inicio = grupo[0]['inicio']
            fim = grupo[-1]['fim']
            
            # Verificar disponibilidade
            slots_disponiveis, erro = HorarioFuncionamento.gerar_slots_disponiveis(empresa_id, data.get('data'))
            if erro:
                erros.append(f"Erro ao verificar disponibilidade: {erro}")
                continue
                
            slot_livre = any(
                slot['inicio'] == inicio and slot['fim'] == fim and slot['disponivel']
                for slot in slots_disponiveis
            )
            
            if not slot_livre:
                erros.append(f"Slot {inicio}-{fim} não está mais disponível")
                continue
            
            # Criar agendamento
            agendamento, erro = Agendamento.criar_agendamento(
                usuario_id=user['id'],
                empresa_id=empresa_id,
                servico_id=servico_id,
                data_agendamento=data.get('data'),
                hora_inicio=inicio,
                hora_fim=fim
            )
            
            if erro:
                erros.append(f"Erro ao agendar {inicio}-{fim}: {erro}")
            else:
                agendamentos_criados.append(agendamento)
        
        if erros and not agendamentos_criados:
            return jsonify({"error": "Falha em todos os agendamentos", "details": erros}), 400
        
        response = {
            "success": True,
            "agendamentos_criados": agendamentos_criados,
            "total_agendamentos": len(agendamentos_criados),
            "erros": erros if erros else None
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Erro no agendamento múltiplo: {str(e)}")
        return jsonify({"error": "Erro interno no servidor"}), 500

@horario_bp.route('/empresa/<int:empresa_id>', methods=['GET'])
def get_horarios_empresa(empresa_id):
    """Obtém todos os horários de funcionamento de uma empresa"""
    try:
        horarios = HorarioFuncionamento.buscar_horario_por_empresa(empresa_id)
        if horarios is None:
            return jsonify({"error": "Nenhum horário encontrado"}), 404
        return horarios
    except Exception as e:
        logger.error(f"Erro ao buscar horários: {str(e)}")
        return jsonify({"error": "Erro interno ao buscar horários"}), 500

@horario_bp.route('/', methods=['POST'])
@login_required
def criar_horario():
    """Cria um novo horário de funcionamento para a empresa do usuário logado"""
    try:
        user = session.get('user')
        empresa_id = user.get('empresa_id')  # Assumindo que o user tem empresa_id
        
        dados = request.get_json()
        if not dados:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        # Validação básica
        required_fields = ['dia_semana', 'hora_abertura', 'hora_fechamento']
        if not all(field in dados for field in required_fields):
            return jsonify({"error": "Campos obrigatórios faltando"}), 400
        
        dados['empresa_id'] = empresa_id
        novo_horario = HorarioFuncionamento.criar_horario(dados)
        
        if not novo_horario:
            return jsonify({"error": "Falha ao criar horário"}), 400
            
        return jsonify(novo_horario), 201
        
    except Exception as e:
        logger.error(f"Erro ao criar horário: {str(e)}")
        return jsonify({"error": "Erro interno ao criar horário"}), 500

@horario_bp.route('/<int:horario_id>', methods=['PUT'])
@login_required

def atualizar_horario(horario_id):
    """Atualiza um horário existente"""
    try:
        user = session.get('user')
        empresa_id = user.get('empresa_id')
        
        # Verifica se o horário pertence à empresa do usuário
        horario = HorarioFuncionamento.buscar_horario_por_id(horario_id)
        if not horario or horario.get('empresa_id') != empresa_id:
            return jsonify({"error": "Horário não encontrado ou não pertence à sua empresa"}), 404
        
        dados = request.get_json()
        if not dados:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        horario_atualizado = HorarioFuncionamento.atualizar_horario(horario_id, dados)
        if not horario_atualizado:
            return jsonify({"error": "Falha ao atualizar horário"}), 400
            
        return jsonify(horario_atualizado)
        
    except Exception as e:
        logger.error(f"Erro ao atualizar horário: {str(e)}")
        return jsonify({"error": "Erro interno ao atualizar horário"}), 500

@horario_bp.route('/<int:horario_id>', methods=['DELETE'])
@login_required

def deletar_horario(horario_id):
    """Remove um horário de funcionamento"""
    try:
        user = session.get('user')
        empresa_id = user.get('empresa_id')
        
        # Verifica se o horário pertence à empresa do usuário
        horario = HorarioFuncionamento.buscar_horario_por_id(horario_id)
        if not horario or horario.get('empresa_id') != empresa_id:
            return jsonify({"error": "Horário não encontrado ou não pertence à sua empresa"}), 404
        
        sucesso = HorarioFuncionamento.deletar_horario(horario_id)
        if not sucesso:
            return jsonify({"error": "Falha ao deletar horário"}), 400
            
        return jsonify({"message": "Horário deletado com sucesso"}), 200
        
    except Exception as e:
        logger.error(f"Erro ao deletar horário: {str(e)}")
        return jsonify({"error": "Erro interno ao deletar horário"}), 500

@horario_bp.route('/disponiveis/<int:empresa_id>', methods=['GET'])
def get_horarios_disponiveis(empresa_id):
    data = request.args.get('data')
    if not data:
        return jsonify({"error": "Parâmetro 'data' é obrigatório"}), 400

    result = horarios_disponiveis_dict(empresa_id, data)
    if not result:
        return jsonify({"error": "Empresa não possui horários cadastrados"}), 404
    
    return jsonify(result)

@horario_bp.route('/disponiveis-dict/<int:empresa_id>', methods=['GET'])
def horarios_disponiveis_dict(empresa_id, data):
    """Retorna horários disponíveis como dicionário para uso no template"""
    try:
        data = request.args.get('data')
        if not data:
            return jsonify({"error": "Parâmetro 'data' é obrigatório"}), 400
        
        # Validar formato da data
        try:
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD"}), 400
        
        # Busca horários de funcionamento
        horarios_funcionamento = HorarioFuncionamento.buscar_horario_por_empresa(empresa_id)
        if not horarios_funcionamento:
            return jsonify({"error": "Empresa não possui horários cadastrados"}), 404
        
        # Busca agendamentos existentes
        agendamentos, _ = Agendamento.listar_agendamentos_empresa_data(empresa_id, data) or ([], None)
        
        # Gerar slots
        slots = gerar_slots_horarios(horarios_funcionamento, agendamentos, data)
        
        return {
            "slots": slots,
            "dia_semana": obter_dia_semana(data),
            "data": data
        }
        
    except Exception as e:
        logger.error(f"Erro ao buscar horários disponíveis: {str(e)}")
        return {"error": "Erro interno ao buscar horários disponíveis"}

def gerar_slots_horarios(horarios_funcionamento, agendamentos, data):
    """Gera slots de 1 hora baseado nos horários de funcionamento"""
    slots = []
    dia_semana = obter_dia_semana(data).lower()
    
    # Encontrar horário para o dia específico
    horario_dia = next(
        (h for h in horarios_funcionamento if h['dia_semana'].lower() == dia_semana),
        None
    )
    
    if not horario_dia:
        return slots
    
    # Função auxiliar para converter hora para objeto time
    def parse_hora(hora_str):
        try:
            # Tenta converter no formato HH:MM:SS
            return datetime.strptime(hora_str, '%H:%M:%S').time()
        except ValueError:
            try:
                # Tenta converter no formato HH:MM
                return datetime.strptime(hora_str, '%H:%M').time()
            except ValueError:
                # Se não conseguir converter, retorna None
                return None
    
    # Gerar slots para cada período (manhã, tarde, noite)
    periodos = [
        (horario_dia.get('manha_abertura'), horario_dia.get('manha_fechamento')),
        (horario_dia.get('tarde_abertura'), horario_dia.get('tarde_fechamento')),
        (horario_dia.get('noite_abertura'), horario_dia.get('noite_fechamento'))
    ]
    
    for inicio_periodo, fim_periodo in periodos:
        if not inicio_periodo or not fim_periodo:
            continue
            
        # Converter para objetos time
        inicio_time = parse_hora(inicio_periodo)
        fim_time = parse_hora(fim_periodo)
        
        if not inicio_time or not fim_time:
            continue
            
        # Criar objetos datetime para facilitar cálculos
        hora_inicio = datetime.combine(datetime.today(), inicio_time)
        hora_fim = datetime.combine(datetime.today(), fim_time)
        
        # Gerar slots de 1 hora
        while hora_inicio < hora_fim:
            slot_fim = hora_inicio + timedelta(hours=1)
            if slot_fim > hora_fim:
                break
            
            slot_str = hora_inicio.strftime('%H:%M')
            slot_fim_str = slot_fim.strftime('%H:%M')
            
            # Verificar se o slot está disponível
            disponivel = True
            for ag in agendamentos:
                try:
                    ag_inicio = parse_hora(ag['hora_inicio'])
                    ag_fim = parse_hora(ag['hora_fim'])
                    if not ag_inicio or not ag_fim:
                        continue
                        
                    ag_inicio_dt = datetime.combine(datetime.today(), ag_inicio)
                    ag_fim_dt = datetime.combine(datetime.today(), ag_fim)
                    
                    if not (slot_fim <= ag_inicio_dt or hora_inicio >= ag_fim_dt):
                        disponivel = False
                        break
                except (KeyError, TypeError):
                    continue
            
            slots.append({
                'inicio': slot_str,
                'fim': slot_fim_str,
                'disponivel': disponivel
            })
            
            hora_inicio = slot_fim
    
    return slots


def obter_dia_semana(data_str):
    """Retorna o dia da semana por extenso para uma data"""
    dias = [
        'Segunda-feira', 'Terça-feira', 'Quarta-feira',
        'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'
    ]
    data = datetime.strptime(data_str, '%Y-%m-%d')
    return dias[data.weekday()]

def calcular_horarios_disponiveis(horarios_funcionamento, agendamentos):
    """Lógica para calcular horários disponíveis baseado nos agendamentos"""
    # Implementação simplificada - adapte conforme sua necessidade
    disponiveis = []
    
    for horario in horarios_funcionamento:
        # Aqui você implementaria a lógica para verificar slots disponíveis
        # baseado nos agendamentos existentes
        disponiveis.append({
            'dia_semana': horario['dia_semana'],
            'hora_abertura': horario['hora_abertura'],
            'hora_fechamento': horario['hora_fechamento'],
            'slots_disponiveis': []  # Preencher com os horários livres
        })
    
    return disponiveis


