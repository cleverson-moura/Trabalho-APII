from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app as app
import os
from werkzeug.utils import secure_filename

from models.usuario_model import UsuarioModel
from models.reserva_model import ReservaModel
from models.quarto_model import QuartoModel
from models.hotel_model import HotelModel


reservas_bp = Blueprint('reservas', __name__, template_folder='../templates')

@reservas_bp.route('/reservas', methods=['GET', 'POST'])
def reservas():
    # registrar()
    reserva_model = ReservaModel()
    if 'usuario' in session:
        if request.method == 'POST':
            id_usuario = session['usuario']['id']
            id_quarto = request.form.get('id_quarto')
            tempo_estadia = request.form.get('tempo_estadia')

            reserva_model = ReservaModel(
                id_usuario=id_usuario,
                id_quarto=id_quarto,
                tempo_estadia=tempo_estadia
            )
            
            reserva_model.fazer_reserva()
            
            flash('Reserva feita com sucesso!', 'success')
            return redirect(url_for('usuario.perfil_usuario'))
    #else:
        #flash('Você precisa estar logado para fazer uma reserva.', 'error')
        #return redirect(url_for('gerais.login'))

@reservas_bp.route('/cancelar_reserva', methods=['GET', 'POST'])
def cancelar_reserva():
    # registrar()
    if request.method == 'POST':
        reserva_id = request.form.get('id_reserva')
        
        reserva_model = ReservaModel(id_reserva=reserva_id)
        reserva_model.cancelar_reserva()
        
        flash('Reserva cancelada com sucesso!', 'success')
        return redirect(url_for('usuario.perfil_usuario'))
    
    flash('Erro ao cancelar a reserva.', 'error')
    return redirect(url_for('usuario.perfil_usuario'))