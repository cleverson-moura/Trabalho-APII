from flask import Blueprint, render_template, session, redirect, url_for, request

from models.usuario_model import UsuarioModel
from models.reserva_model import ReservaModel
from models.quarto_model import QuartoModel
from models.hotel_model import HotelModel

gerais_bp = Blueprint('gerais', __name__, template_folder='../templates')

@gerais_bp.route('/')
def index():
    # registrar()
    if 'usuario' in session:
        icone = "/static/{}".format(session['usuario']['imagem'])
        endereco = "/perfil_usuario"
    elif 'hotel' in session:
        icone = "/static/{}".format(session['hotel']['imagem'])
        endereco = "/perfil_hotel"
    else:
        icone = "/static/imagens/user.png"
        endereco = "/login"
    texto = "Vamos ver"

    hoteis_model = HotelModel()
    hoteis = hoteis_model.buscar_todos_hoteis()
    return render_template('index.html', texto=texto, icone=icone, endereco=endereco, hoteis=hoteis)

@gerais_bp.route('/login', methods=['GET', 'POST'])
def login():
    # registrar()
    email = request.form.get("email")
    senha = request.form.get("senha")

    usuario_model = UsuarioModel(email=email, senha=senha)
    usuario = usuario_model.buscar_por_email_senha()

    hotel_model = HotelModel(email=email, senha=senha)
    hotel = hotel_model.buscar_por_email_senha()
    
    if usuario:
        session['usuario'] = {
                    'id': usuario['id_usuario'],
                    'nome': usuario['nome'],
                    'email': usuario['email'],
                    'senha': usuario['senha'],
                    'cpf': usuario['cpf'],
                    'imagem': usuario['imagem']
                }
        return redirect(url_for("usuario.perfil_usuario"))

    elif hotel:
        session['hotel'] = {
                    'id': hotel['id_hotel'],
                    'nome': hotel['nome'],
                    'cnpj': hotel['cnpj'],
                    'email': hotel['email'],
                    'cidade': hotel['cidade'],
                    'bairro': hotel['bairro'],
                    'rua': hotel['rua'],
                    'numero': hotel['numero'],
                    'senha': hotel['senha'],
                    'foto': hotel['foto']
                }
        return redirect(url_for("hotel.perfil_hotel"))
    else:
        print("Erro")
        
    
    return render_template('login.html')

@gerais_bp.route('/sair')
def sair():
    # registrar()
    session.clear()
    return redirect(url_for('gerais.index'))