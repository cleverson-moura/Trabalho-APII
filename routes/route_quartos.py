from flask import Blueprint, render_template, session, redirect, url_for, request, flash

from models.quarto_model import QuartoModel
from models.hotel_model import HotelModel
from models.reserva_model import ReservaModel
from datetime import datetime, timedelta
import json
import os
from flask import current_app as app
from werkzeug.utils import secure_filename


quarto_bp = Blueprint('quarto', __name__, template_folder='../templates')

@quarto_bp.route('/quartos_reserva/<int:id_hotel>/<int:id_quarto>', methods=['GET', 'POST'])
def quartos_reserva(id_hotel, id_quarto):
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

    quarto_model = QuartoModel(id_quarto=id_quarto)
    quarto = quarto_model.buscar_por_quarto()

    reserva_model = ReservaModel(id_quarto=id_quarto)
    reservas = reserva_model.buscar_todas_reservas()
    
    datas_ocupadas = []
    for reserva in reservas:
        inicio = datetime.strptime(reserva['data_checkin'], "%Y-%m-%d")
        fim = datetime.strptime(reserva['data_checkout'], "%Y-%m-%d")

        while inicio <= fim:
            datas_ocupadas.append(inicio.strftime("%Y-%m-%d"))
            inicio += timedelta(days=1)

    rota = "/quartos_reserva/{}/{}".format(id_hotel, id_quarto)

    data_checkin = request.form.get("checkin")
    data_checkout = request.form.get("checkout")

    if request.method == "POST":
        if "usuario" in session:
            reserva = ReservaModel(None, session["usuario"]["id"], id_hotel, None, data_checkin, data_checkout)
            reserva.fazer_reserva()
        elif "hotel" in session:
            reserva = ReservaModel(None, session["usuario"]["id"], id_hotel, None, data_checkin, data_checkout)
            reserva.fazer_reserva()
        else:
            return redirect(url_for("gerais.login"))

    return render_template('quartos/quartos_hotel.html', icone=icone, endereco=endereco, hotel=hotel, quarto=quarto, rota=rota, botao_reserva_texto=botao_reserva_texto, datas_ocupadas=json.dumps(datas_ocupadas))
@quarto_bp.route('/salvar_quarto', methods=['GET', 'POST'])
def salvar_quarto():
    # Permitir apenas hotel logado
    if 'hotel' not in session:
        flash("Você precisa estar logado como hotel para adicionar um quarto.")
        return redirect(url_for('hotel.cadastro_hotel'))

    if request.method == 'POST':
        descricao = request.form.get('descricao')
        andar = request.form.get('andar')
        numero_quarto = request.form.get('numero_quarto')
        preco = request.form.get('preco')
        imagem_file = request.files.get('imagem')

        caminho_relativo = None
        if imagem_file and imagem_file.filename != '':
            filename = secure_filename(imagem_file.filename)
            caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagem_file.save(caminho_completo)
            caminho_relativo = f'uploads/{filename}'

        # Pega o id do hotel logado
        id_hotel = session['hotel']['id']

        quarto = QuartoModel(
            andar=andar,
            numero=numero_quarto,
            preco=preco,
            imagem=caminho_relativo,
            id_hotel=id_hotel,
            descricao=descricao
        )
        quarto.inserir()

        flash("Quarto adicionado com sucesso!")
        return redirect(url_for('hotel.perfil_hotel'))

    return render_template('quartos/salvar_quartos.html')

@quarto_bp.route('/imagens_quarto/<id_quarto>', methods=['POST'])
def imagens_quarto(id_quarto):
    # Permitir apenas hotel logado
    if 'hotel' not in session:
        flash("Você precisa estar logado como hotel para editar as imagens do quarto.")
        return redirect(url_for('hotel.cadastro_hotel'))
    
    if request.method == 'POST':
        # Lista das imagens do formulário
        imagens = [
            request.files.get('imagem1'),
            request.files.get('imagem2'),
            request.files.get('imagem3'),
            request.files.get('imagem4'),
            request.files.get('imagem5'),
            request.files.get('imagem6')
        ]

        caminhos_relativos = []

        for imagem_file in imagens:
            caminho_relativo = None
            if imagem_file and imagem_file.filename != '':
                filename = secure_filename(imagem_file.filename)
                caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                # Salva o arquivo no diretório de uploads
                imagem_file.save(caminho_completo)
                # Caminho relativo que você salvará no banco
                caminho_relativo = f'uploads/{filename}'
            caminhos_relativos.append(caminho_relativo)

        quarto = QuartoModel(id_quarto=id_quarto)
        quarto.inserir_imagens(
            imagen1=caminhos_relativos[0],
            imagen2=caminhos_relativos[1],
            imagen3=caminhos_relativos[2],
            imagen4=caminhos_relativos[3],
            imagen5=caminhos_relativos[4],
            imagen6=caminhos_relativos[5]
        )

    return redirect(url_for('hotel.perfil_hotel'))

