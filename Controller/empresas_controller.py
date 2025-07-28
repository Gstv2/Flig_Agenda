# controllers/estabelecimentos_controller.py
from flask import Blueprint, render_template
from Models.estabelecimentos import Estabelecimento
from Controller.auth_controller import login_required


estabelecimento_bp = Blueprint('estabelecimento', __name__)

@estabelecimento_bp.route('/cadastrar_empresa')
@login_required
def cadastrar_empresa():
    return render_template('cadastrar_empresa.html')

