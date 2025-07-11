from flask import Blueprint, render_template, session, redirect, url_for, request

from models.quarto_model import QuartoModel
from models.hotel_model import HotelModel

quarto_bp = Blueprint('quarto', __name__, template_folder='../templates')

@quarto_bp.route('/quartos_reserva/<int:id_hotel>', methods=['GET', 'POST'])
def quartos_reserva(id_hotel):
    if 'usuario' in session:
        icone = "/static/{}".format(session['usuario']['imagem'])
        endereco = "/perfil_usuario"
    elif 'hotel' in session:
        icone = "/static/{}".format(session['hotel']['foto'])
        endereco = "/perfil_hotel"
    else:
        icone = "/static/imagens/user.png"
        endereco = "/login"

    hotel_model = HotelModel(id_hotel=id_hotel)
    hotel = hotel_model.buscar_por_hotel()

    return render_template('quartos/quartos_hotel.html', icone=icone, endereco=endereco, hotel=hotel)