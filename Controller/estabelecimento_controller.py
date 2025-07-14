# controllers/estabelecimentos_controller.py
from flask import Blueprint, render_template
from Models.estabelecimentos import Estabelecimento

estabelecimento_bp = Blueprint('estabelecimento', __name__)

@estabelecimento_bp.route('/estabelecimentos')
def listar_estabelecimentos():
    estabelecimentos = Estabelecimento.listar_todos()
    return render_template('estabelecimentos.html', estabelecimentos=estabelecimentos)

