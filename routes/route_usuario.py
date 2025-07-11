from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app as app
import os
from werkzeug.utils import secure_filename

from models.usuario_model import UsuarioModel
from models.reserva_model import ReservaModel
from models.quarto_model import QuartoModel
from models.hotel_model import HotelModel

usuario_bp = Blueprint('usuario', __name__, template_folder='../templates')

@usuario_bp.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    # registrar()
    if request.method == "POST":
        nome_usuario = request.form.get('nome')
        cpf_usuario = request.form.get('cpf')
        email_usuario = request.form.get('email')
        senha_usuario = request.form.get('senha')
        foto_usuario = request.files.get('imagem')
        with open('registros/users.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f"{nome_usuario} | {cpf_usuario} | {email_usuario}\n")

        if foto_usuario:
            filename = secure_filename(foto_usuario.filename)
            caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto_usuario.save(caminho_completo)

            # Salvar caminho relativo no banco
            caminho_relativo = f'uploads/{filename}'

            usuario = UsuarioModel(
                nome=nome_usuario,
                cpf=cpf_usuario,
                email=email_usuario,
                senha=senha_usuario,
                imagem=caminho_relativo
            )
            if usuario.inserir() == True:
                flash("Esse email já está em uso!")
            else:
                resultado = usuario.buscar_por_email_senha()
                if resultado:
                    # Guarda na session os dados do usuario em forma de dicionario
                    session['usuario'] = {
                        'id': resultado['id_usuario'],
                        'nome': resultado['nome'],
                        'email': resultado['email'],
                        'senha': resultado['senha'],
                        'cpf': resultado['cpf'],
                        'imagem': resultado['imagem']
                    }
                

                return redirect(url_for('usuario.perfil_usuario'))
        
    return render_template('/usuario/cadastro_usuario.html')

@usuario_bp.route("/perfil_usuario", methods=['GET','POST'])
def perfil_usuario():
    # registrar()
    # verifica se o usuario está logado
    if 'usuario' not in session:
        return redirect(url_for('usuario.cadastro_usuario'))
    else:
        usuario = session['usuario']
        
        reserva_model = ReservaModel(id_usuario=usuario['id'])
        reservas = reserva_model.buscar_por_reservas()

        # Lista com todas as informações combinadas
        reservas_detalhadas = []

        for reserva in reservas:
            # Pega o quarto
            quarto_model = QuartoModel(id_quarto=reserva['id_quarto'])
            quarto = quarto_model.buscar_por_quarto()

            # Pega o hotel do quarto
            hotel_model = HotelModel(id_hotel=quarto['id_hotel'])
            hotel = hotel_model.buscar_por_hotel()

            # Junta tudo num dicionário
            reservas_detalhadas.append({
                'reserva': reserva,
                'quarto': quarto,
                'hotel': hotel
            })

        return render_template('/usuario/perfil_usuario.html', usuario=usuario, reservas=reservas_detalhadas)

@usuario_bp.route('/editar_perfil_usuario', methods=['GET', 'POST'])
def editar_perfil_usuario():
    id = session['usuario']['id']
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    foto = request.files.get('imagem')

    with open('registros/users.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f"{nome} | {email}\n")
    if foto:
        foto_nome = "uploads/{}".format(foto.filename)
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
        foto.save(caminho)
    else:
        foto_nome = session['usuario']['imagem']
    if nome:
        atualiza_usuario = UsuarioModel(
            id_usuario=id,
            nome=nome,
            email=email,
            senha=senha,
            imagem=foto_nome
        )

        atualiza_usuario.atualizar()

        usuario_model = UsuarioModel(id_usuario=id)
        usuario = usuario_model.buscar_por_id()

        session['usuario'] = {
                    'id': usuario['id_usuario'],
                    'nome': usuario['nome'],
                    'email': usuario['email'],
                    'senha': usuario['senha'],
                    'cpf': usuario['cpf'],
                    'imagem': usuario['imagem']
                    }             
        return redirect(url_for('usuario.perfil_usuario'))
    return render_template('/usuario/editar_perfil_usuario.html')
