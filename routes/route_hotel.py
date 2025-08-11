from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app as app
import os
from werkzeug.utils import secure_filename

from models.usuario_model import UsuarioModel
from models.reserva_model import ReservaModel
from models.quarto_model import QuartoModel
from models.hotel_model import HotelModel
from datetime import datetime


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
        chave_pix = request.form.get("chave_pix")
        banner = request.files.get("banner")
        with open('registros/users.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f"{nome_hotel} | {cidade_hotel} | {bairro_hotel} | {rua_hotel} | {numero_hotel} | {cnpj_hotel} | {email} | {senha}\n")

        if foto:
            filename = secure_filename(foto.filename)
            caminho_foto = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto.save(caminho_foto)
            
            caminho_relativo_foto = f'uploads/{filename}'


        # Verifica se o CNPJ é válido
        # if not re.match(r'^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$', cnpj_empresa):
        #     flash('CNPJ inválido. Formato esperado: XX.XXx.XXx/XXXX-XX', 'error')
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
            foto=caminho_relativo_foto,
            chave_pix=chave_pix
        )

        # Insere os dados no banco de dados
        if hotel_model.inserir() == True:
                flash("Esse email já está em uso!")
        else:
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
                    'foto': resultado['foto'],
                    'chave_pix': resultado['chave_pix']               
                }

            flash('Empresa cadastrada com sucesso!', 'success')
            return redirect(url_for('gerais.index'))

    return render_template('empresa/cadastro_hotel.html')

@hotel_bp.route('/perfil_hotel', methods=['GET', 'POST'])
def perfil_hotel():
    # registrar()
    if 'hotel' not in session:
        return redirect(url_for('hotel.cadastro_hotel'))
    else:
        hotel = session['hotel'] 

        quarto_model = QuartoModel(id_hotel=hotel['id'])
        quartos = quarto_model.buscar_todos_quartos_do_hotel()

        

         # Lista com todas as informações combinadas
        reservas_detalhadas = []

        for i, quarto in enumerate(quartos):
            # Pega a reserva

            reserva_model = ReservaModel(id_quarto=quarto["id_quarto"])
            reservas = reserva_model.buscar_por_reservas_do_quarto()

            for reserva in reservas:

                usuario_da_reserva_model = ReservaModel(id_usuario=reserva["id_usuario"])
                usuario_da_reserva = usuario_da_reserva_model.buscar_por_usuario_da_reserva()
                

                listacheckin = reserva["data_checkin"].split("-") 
                listacheckout = reserva["data_checkout"].split("-")

                strcheckin = listacheckin[2] + "/" + listacheckin[1] + "/" + listacheckin[0]
                strcheckout = listacheckout[2] + "/" + listacheckout[1] + "/" + listacheckout[0]

                conversao1 = datetime.strptime(strcheckin, "%d/%m/%Y")
                conversao2 = datetime.strptime(strcheckout, "%d/%m/%Y")

                diferenca = conversao2 - conversao1

                tempo_estadia = diferenca.days
                
                del listacheckin
                del listacheckout

                # Junta tudo num dicionário
                reservas_detalhadas.append({
                    'reserva': reserva,
                    'usuario_da_reserva' : usuario_da_reserva,
                    'quarto': quarto,
                    'hotel': hotel,
                    'checkin' : strcheckin,
                    'checkout' : strcheckout
                })


        return render_template('empresa/perfil_hotel.html', hotel=hotel, reservas=reservas_detalhadas)

@hotel_bp.route('/hotel_reserva/<int:id_hotel>', methods=['GET', 'POST'])
def hotel_reserva(id_hotel):
    # registrar()
    
    hotel_model = HotelModel(id_hotel=id_hotel)
    hotel = hotel_model.buscar_por_hotel()

    quarto_model = QuartoModel(id_hotel=id_hotel)
    quartos = quarto_model.buscar_todos_quartos()
        

    return render_template('empresa/hotel_reserva.html', hotel=hotel, quartos=quartos)

@hotel_bp.route('/editar_perfil_hotel', methods=['GET', 'POST'])
def editar_perfil_hotel():
    if 'hotel' not in session:
        return redirect(url_for('hotel.cadastro_hotel'))

    if request.method == 'POST':
        id_hotel = session['hotel']['id']
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        imagem = request.files.get('imagem')
        chave_pix = request.form.get('chave_pix')

        # Usa a foto antiga como padrão
        foto_path = session['hotel']['foto']
        if imagem and imagem.filename != '':
            filename = secure_filename(imagem.filename)
            caminho_foto = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagem.save(caminho_foto)
            foto_path = f'uploads/{filename}'

        # Atualiza no banco
        hotel_model = HotelModel(id_hotel=id_hotel, nome=nome, senha=senha, foto=foto_path, chave_pix=chave_pix)
        hotel_model.atualizar()

        # Atualiza todos os dados da sessão com os valores mais recentes do banco
        hotel_atualizado = HotelModel(id_hotel=id_hotel).buscar_por_hotel()
        session['hotel'] = {
            'id': hotel_atualizado['id_hotel'],
            'nome': hotel_atualizado['nome'],
            'cidade': hotel_atualizado['cidade'],
            'bairro': hotel_atualizado['bairro'],
            'rua': hotel_atualizado['rua'],
            'numero': hotel_atualizado['numero'],
            'cnpj': hotel_atualizado['cnpj'],
            'email': hotel_atualizado['email'],
            'foto': hotel_atualizado['foto'],
            'chave_pix' : hotel_atualizado['chave_pix']
        }

        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for('hotel.perfil_hotel'))

    return render_template('empresa/editar_hotel.html', hotel=session['hotel'])

@hotel_bp.route('/pagina_hotel/<int:id_hotel>', methods=['GET'])
def pagina_hotel(id_hotel):
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

    quarto_model = QuartoModel(id_hotel=id_hotel)
    quartos = quarto_model.buscar_todos_quartos_do_hotel()

    return render_template('empresa/pagina_hotel.html', hotel=hotel, quartos=quartos, icone=icone, endereco=endereco)