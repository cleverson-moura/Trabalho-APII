from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app as app
import os
from werkzeug.utils import secure_filename

from models.usuario_model import UsuarioModel
from models.reserva_model import ReservaModel
from models.quarto_model import QuartoModel
from models.hotel_model import HotelModel

empresa_bp = Blueprint('empresa', __name__, template_folder='../templates')

@empresa_bp.route('/cadastro_empresa', methods=['GET', 'POST'])
def cadastro_empresa():
    # registrar()
    if request.method == "POST":
        nome_empresa = request.form.get("nome")
        cidade_empresa = request.form.get("cidade")
        bairro_empresa = request.form.get("bairro")
        rua_empresa = request.form.get("rua")
        numero_empresa = request.form.get("numero")
        cnpj_empresa = request.form.get("cnpj")
        id_ponto = request.form.get("id_ponto")
        with open('registros/users.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f"{nome_empresa} | {cidade_empresa} | {bairro_empresa} | {rua_empresa} | {numero_empresa} | {cnpj_empresa} | {id_ponto}\n")


        # Verifica se o CNPJ é válido
        # if not re.match(r'^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$', cnpj_empresa):
        #     flash('CNPJ inválido. Formato esperado: XX.XXX.XXX/XXXX-XX', 'error')
        #     return redirect(url_for('cadastro_empresa'))

        # Cria o objeto HotelModel
        hotel_model = HotelModel(
            nome=nome_empresa,
            cidade=cidade_empresa,
            bairro=bairro_empresa,
            rua=rua_empresa,
            numero=numero_empresa,
            cnpj=cnpj_empresa,
            id_ponto=id_ponto
        )

        # Insere os dados no banco de dados
        hotel_model.inserir()

        flash('Empresa cadastrada com sucesso!', 'success')
        return redirect(url_for('gerais.index'))

    return render_template('empresa/cadastro_empresa.html')

@empresa_bp.route('/hotel_reserva/<int:id_hotel>', methods=['GET', 'POST'])
def hotel_reserva(id_hotel):
    # registrar()
    
    hotel_model = HotelModel(id_hotel=id_hotel)
    hotel = hotel_model.buscar_por_hotel()

    quarto_model = QuartoModel(id_hotel=id_hotel)
    quartos = quarto_model.buscar_todos_quartos()
        

    return render_template('empresa/hotel_reserva.html', hotel=hotel, quartos=quartos)