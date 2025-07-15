from flask import Blueprint, render_template, session, redirect, url_for, request

from models.quarto_model import QuartoModel
from models.hotel_model import HotelModel
from models.reserva_model import ReservaModel

quarto_bp = Blueprint('quarto', __name__, template_folder='../templates')

@quarto_bp.route('/quartos_reserva/<int:id_hotel>', methods=['GET', 'POST'])
def quartos_reserva(id_hotel):
    if 'usuario' in session:
        botao_reserva_texto = "Reservar quarto!"
        icone = "/static/{}".format(session['usuario']['imagem'])
        endereco = "/perfil_usuario"
    elif 'hotel' in session:
        botao_reserva_texto = "Reservar quarto!"
        icone = "/static/{}".format(session['hotel']['foto'])
        endereco = "/perfil_hotel"
    else:
        botao_reserva_texto = "Faça Login Para Reservar"
        icone = "/static/imagens/user.png"
        endereco = "/login"

    hotel_model = HotelModel(id_hotel=id_hotel)
    hotel = hotel_model.buscar_por_hotel()

    quarto_model = QuartoModel(id_quarto=id_hotel)
    quarto = quarto_model.buscar_por_quarto()

    rota = "/quartos_reserva/{}".format(id_hotel)

    data_checkin = request.form.get("checkin")
    data_checkout = request.form.get("checkout")

    if request.method == "POST" and "usuario" in session:
        reserva = ReservaModel(None, session["usuario"]["id"], id_hotel, None, data_checkin, data_checkout)
        reserva.fazer_reserva()
    else:
        redirect(url_for("gerais.login"))

    return render_template('quartos/quartos_hotel.html', icone=icone, endereco=endereco, hotel=hotel, quarto=quarto, rota=rota, botao_reserva_texto=botao_reserva_texto)