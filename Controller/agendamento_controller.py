from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from Models.agendamentos import Agendamento, timedelta
from Models.empresas import Empresas
from Controller.auth_controller import login_required
from datetime import datetime
import logging

agendamento_bp = Blueprint('agendamento', __name__)
logger = logging.getLogger(__name__)

@agendamento_bp.route('/agendar/<int:empresa_id>', methods=['GET', 'POST'])
@login_required
def agendar(empresa_id):
    user = session.get('user', {})
    if not user:
        flash("Faça login para agendar", "error")
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        data = request.form.get('data')
        hora_inicio = request.form.get('hora_inicio')
        servico_id = request.form.get('servico_id')
        
        if not all([data, hora_inicio, servico_id]):
            flash("Preencha todos os campos", "error")
            return redirect(request.url)
        
        # Calcula hora_fim (ex: 1 hora depois)
        hora_fim = (datetime.strptime(hora_inicio, '%H:%M') + timedelta(hours=1)).strftime('%H:%M')
        
        agendamento, erro = Agendamento.criar_agendamento(
            usuario_id=user.get('id'),
            empresa_id=empresa_id,
            servico_id=servico_id,
            data_agendamento=data,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )
        
        if erro:
            flash(f"Erro ao agendar: {erro}", "error")
        else:
            flash("Agendamento realizado com sucesso!", "success")
            return redirect(url_for('agendamento.meus_agendamentos'))
    
    # GET: Mostrar formulário
    empresa, _ = Empresas.buscar_empresa_id(empresa_id)
    servicos, _ = Empresas.listar_servicos(empresa_id)  # Você precisará implementar isso
    
    return render_template('agendar.html', empresa=empresa, servicos=servicos)

@agendamento_bp.route('/meus-agendamentos')
@login_required
def meus_agendamentos():
    user = session.get('user', {})
    agendamentos, erro = Agendamento.listar_agendamentos_usuario(user.get('id'))
    
    if erro:
        flash(f"Erro ao carregar agendamentos: {erro}", "error")
        agendamentos = []
    
    return render_template('meus_agendamentos.html', agendamentos=agendamentos)

@agendamento_bp.route('/agendamentos-empresa')
@login_required
def agendamentos_empresa():
    user = session.get('user', {})
    # Verifica se o usuário tem empresa
    empresa, _ = Empresas.buscar_empresa_por_usuario(user.get('id'))
    
    if not empresa:
        flash("Você não possui uma empresa cadastrada", "error")
        return redirect(url_for('index'))
    
    agendamentos, erro = Agendamento.listar_agendamentos_empresa(empresa.get('id'))
    
    if erro:
        flash(f"Erro ao carregar agendamentos: {erro}", "error")
        agendamentos = []
    
    return render_template('agendamentos_empresa.html', agendamentos=agendamentos, empresa=empresa)

@agendamento_bp.route('/cancelar-agendamento/<int:agendamento_id>', methods=['POST'])
@login_required
def cancelar_agendamento(agendamento_id):
    user = session.get('user', {})
    _, erro = Agendamento.cancelar_agendamento(agendamento_id, user.get('id'))
    
    if erro:
        flash(f"Erro ao cancelar: {erro}", "error")
    else:
        flash("Agendamento cancelado com sucesso", "success")
    
    return redirect(url_for('agendamento.meus_agendamentos'))

@agendamento_bp.route('/atualizar-status/<int:agendamento_id>', methods=['POST'])
@login_required
def atualizar_status(agendamento_id):
    novo_status = request.form.get('status')
    if novo_status not in ['confirmado', 'cancelado', 'concluido']:
        flash("Status inválido", "error")
        return redirect(url_for('agendamento.agendamentos_empresa'))
    
    _, erro = Agendamento.atualizar_status(agendamento_id, novo_status)
    
    if erro:
        flash(f"Erro ao atualizar status: {erro}", "error")
    else:
        flash("Status atualizado com sucesso", "success")
    
    return redirect(url_for('agendamento.agendamentos_empresa'))