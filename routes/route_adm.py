from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app as app
import os
from werkzeug.utils import secure_filename

from models.usuario_model import UsuarioModel
from models.reserva_model import ReservaModel
from models.quarto_model import QuartoModel
from models.hotel_model import HotelModel
from models.administrador_model import AdministradorModel

adm_bp = Blueprint('adm', __name__, template_folder='../templates')

@adm_bp.route('/cadastro_adm', methods=['GET', 'POST'])
def cadastro_adm():
    # registrar()
    if request.method == "POST":
        nome_adm = request.form.get("nome")
        email_adm = request.form.get("email")
        senha_adm = request.form.get("senha")
        cpf_adm = request.form.get("cpf")
        foto_adm = request.files.get('foto-adm')
        with open('registros/users.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f"{nome_adm} | {email_adm} | {cpf_adm}\n")

        

        if foto_adm:
            filename = secure_filename(foto_adm.filename)
            caminho_foto_adm = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto_adm.save(caminho_foto_adm)
            
            caminho_relativo_foto_adm = f'uploads/{filename}'

            adm = AdministradorModel(
                nome=nome_adm,
                cpf=cpf_adm,
                email=email_adm,
                senha=senha_adm,
                imagem=caminho_relativo_foto_adm
            )

            adm.inserir()

            resultado = adm.buscar_por_email_senha()
            
            if resultado:
                session['adm'] = {
                    'id': resultado['id_adm'],
                    'nome': resultado['nome'],
                    'email': resultado['email'],
                    'senha': resultado['senha'],
                    'cpf': resultado['cpf'],
                    'id_hotel': resultado['id_hotel'],
                    'imagem': resultado['imagem']
                }
            return redirect(url_for('adm.perfil_adm'))
    return render_template('administrador/cadastro_adm.html')

@adm_bp.route('/perfil_adm', methods=['GET', 'POST'])
def perfil_adm():

    # registrar()
    if 'adm' not in session:
        return redirect(url_for('adm.cadastro_adm'))
    else:
        adm = session['adm']
        return render_template('administrador/perfil_adm.html',adm=adm)
    
@adm_bp.route("/editar_perfil_adm", methods=['GET', 'POST'])
def editar_perfil_adm():
    id = session['adm']['id']
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
        foto_nome = session['adm']['imagem']
    if nome:
        adm_model = AdministradorModel(
            id_administrador=id,
            nome=nome,
            email=email,
            senha=senha,
            imagem=foto_nome
        )
        adm_model.atualizar()
        adm = adm_model.buscar_por_id()
        session['adm'] = {
                    'id': adm['id_adm'],
                    'nome': adm['nome'],
                    'email': adm['email'],
                    'senha': adm['senha'],
                    'id_hotel': adm['id_hotel'],
                    'cpf': adm['cpf'],
                    'imagem': adm['imagem']
                    }             
        return redirect(url_for('adm.perfil_adm'))
    return render_template('/administrador/editar_perfil_adm.html')