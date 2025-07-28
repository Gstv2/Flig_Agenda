from flask import Blueprint, render_template, request, redirect, url_for
from Models.usuarios import Usuario
from Controller.auth_controller import login_required

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    return render_template('perfil.html')


