from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app as app
import os
from werkzeug.utils import secure_filename

from models.usuario_model import UsuarioModel
from models.reserva_model import ReservaModel
from models.quarto_model import QuartoModel
from models.hotel_model import HotelModel

hotel_bp = Blueprint('hotel', __name__, template_folder='../templates')

@hotel_bp.route('/cadastro_hotel', methods=['GET', 'POST'])
def cadastro_hotel():
    # registrar()
    if request.method == "POST":
        nome_hotel = request.form.get("nome")
        cidade_hotel = request.form.get("cidade")
        bairro_hotel = request.form.get("bairro")
        rua_hotel = request.form.get("rua")
        numero_hotel = request.form.get("numero")
        cnpj_hotel = request.form.get("cnpj")
        email = request.form.get("email")
        senha = request.form.get("senha")
        foto = request.files.get("foto")
        with open('registros/users.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f"{nome_hotel} | {cidade_hotel} | {bairro_hotel} | {rua_hotel} | {numero_hotel} | {cnpj_hotel} | {email} | {senha}\n")

        if foto:
            filename = secure_filename(foto.filename)
            caminho_foto = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto.save(caminho_foto)
            
            caminho_relativo_foto = f'uploads/{filename}'


        # Verifica se o CNPJ é válido
        # if not re.match(r'^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$', cnpj_empresa):
        #     flash('CNPJ inválido. Formato esperado: XX.XXX.XXX/XXXX-XX', 'error')
        #     return redirect(url_for('cadastro_empresa'))

        # Cria o objeto HotelModel
        hotel_model = HotelModel(
            nome=nome_hotel,
            cidade=cidade_hotel,
            bairro=bairro_hotel,
            rua=rua_hotel,
            numero=numero_hotel,
            cnpj=cnpj_hotel,
            email=email,
            senha=senha,
            foto=caminho_relativo_foto
        )

        # Insere os dados no banco de dados
        hotel_model.inserir()

        resultado = hotel_model.buscar_por_email_senha()
            
        if resultado:
            session['hotel'] = {
                'id': resultado['id_hotel'],
                'nome': resultado['nome'],
                'cidade': resultado['cidade'],
                'bairro': resultado['bairro'],
                'rua': resultado['rua'],
                'numero': resultado['numero'],
                'cnpj': resultado['cnpj'],
                'email': resultado['email'],
                'foto': resultado['foto']                
            }

        flash('Empresa cadastrada com sucesso!', 'success')
        return redirect(url_for('gerais.index'))

    return render_template('hotel/cadastro_hotel.html')

@hotel_bp.route('/perfil_hotel', methods=['GET', 'POST'])
def perfil_hotel():
    # registrar()
    if 'hotel' not in session:
        return redirect(url_for('hotel.cadastro_hotel'))
    else:
        hotel = session['hotel']    
        return render_template('empresa/perfil_hotel.html', hotel=hotel)

@hotel_bp.route('/hotel_reserva/<int:id_hotel>', methods=['GET', 'POST'])
def hotel_reserva(id_hotel):
    # registrar()
    
    hotel_model = HotelModel(id_hotel=id_hotel)
    hotel = hotel_model.buscar_por_hotel()

    quarto_model = QuartoModel(id_hotel=id_hotel)
    quartos = quarto_model.buscar_todos_quartos()
        

    return render_template('empresa/hotel_reserva.html', hotel=hotel, quartos=quartos)