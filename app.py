from flask import Flask, render_template, request, redirect, url_for, flash, session
#from models.connect import Database # Importação da Classe com as funções de banco de dados
import sqlite3
import re
import os
from werkzeug.utils import secure_filename
from datetime import datetime

from models.usuario_model import UsuarioModel
from models.administrador_model import AdministradorModel
from models.reserva_model import ReservaModel
from models.quarto_model import QuartoModel
from models.hotel_model import HotelModel

def registrar():
    ip_usuario = request.remote_addr
    tempo_acesso = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    url_visitada = request.path
    ip_usuario = request.remote_addr
    with open('registros/registros_acessos.txt', 'w') as f:
        f.write(f'{tempo_acesso} | IP:{ip_usuario} | URL:{url_visitada}\n')
        ## Parte q registra o acesso em arquivo.txt ##

app = Flask(__name__)
app.secret_key = "123"
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

# Certifique-se que a pasta exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    if 'usuario' in session:
        icone = "/static/{}".format(session['usuario']['imagem'])
        endereco = "/perfil_usuarios"
    elif 'adm' in session:
        icone = "/static/{}".format(session['adm']['imagem'])
        endereco = "/perfil_adm"
    else:
        icone = "/static/imagens/user.png"
        endereco = "/cadastro"
    texto = "Vamos ver"

    hoteis_model = HotelModel()
    hoteis = hoteis_model.buscar_todos_hoteis()
    return render_template('index.html', texto=texto, icone=icone, endereco=endereco, hoteis=hoteis)

@app.route('/pontos')
def pontos():
    if 'usuario' in session:
        icone = "/static/{}".format(session['usuario']['imagem'])
        endereco = "/perfil_usuarios"
    elif 'adm' in session:
        icone = "/static/{}".format(session['adm']['imagem'])
        endereco = "/perfil_adm"
    else:
        icone = "/static/imagens/user.png"
        endereco = "/cadastro"
    texto = "Vamos ver"
    #registrar()
    # usando o osjeto de conexão com banco de dados
    #connect = sqlite3.connect("database/banco/banco_de_dados.db") # cria o objeto
    #cursor = connect.cursor() # conecta ao banco
    #cursor.execute('SELECT * FROM teste') # executa o SQL
    #ponto = cursor.fetchall() # retorna uma lista com as linhas da tabela
    #tamanho = len(ponto)
    #connect.close()
    return render_template('pontos.html', icone=icone, endereco=endereco)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    registrar()
    email = request.form.get("nome")
    senha = request.form.get("senha")

    usuario_model = UsuarioModel(email=email, senha=senha)
    usuario = usuario_model.buscar_por_email_senha()

    adm_model = AdministradorModel(email=email, senha=senha)
    adm = adm_model.buscar_por_email_senha()
    
    if usuario:
        session['usuario'] = {
                    'id': usuario['id_usuario'],
                    'nome': usuario['nome'],
                    'email': usuario['email'],
                    'senha': usuario['senha'],
                    'cpf': usuario['cpf'],
                    'imagem': usuario['imagem']
                }
        return redirect(url_for("perfil_usuarios"))
    elif adm:
        session['adm'] = {
                    'id': adm['id_adm'],
                    'nome': adm['nome'],
                    'cpf': adm['cpf'],
                    'email': adm['email'],
                    'senha': adm['senha'],
                    'imagem': adm['imagem']
                }
        return redirect(url_for("perfil_adm"))
    else:
        print("Erro")
        
    
    return render_template('Popup_cadastro.html')

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    registrar()
    if request.method == "POST":
        nome_usuario = request.form.get('nome')
        cpf_usuario = request.form.get('cpf')
        email_usuario = request.form.get('email')
        senha_usuario = request.form.get('senha')
        foto_usuario = request.files.get('imagem')

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
            usuario.inserir()

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
            

            return redirect(url_for('perfil_usuarios'))
        
    return render_template('/usuario/cadastro_usuario.html')

@app.route('/cadastro_adm', methods=['GET', 'POST'])
def cadastro_adm():
    registrar()
    if request.method == "POST":
        nome_adm = request.form.get("nome")
        email_adm = request.form.get("email")
        senha_adm = request.form.get("senha")
        cpf_adm = request.form.get("cpf")
        foto_adm = request.files.get('foto-adm')

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
            return redirect(url_for('perfil_adm'))
    return render_template('administrador/cadastro_adm.html')

@app.route('/perfil_adm', methods=['GET', 'POST'])
def perfil_adm():

    registrar()
    if 'adm' not in session:
        return redirect(url_for('cadastro_adm'))
    else:
        adm = session['adm']
        return render_template('administrador/perfil_adm.html',adm=adm)
    
@app.route("/editar_perfil_adm", methods=['GET', 'POST'])
def editar_perfil_adm():
    id = session['adm']['id']
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    foto = request.files.get('imagem')
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
        return redirect(url_for('perfil_adm'))
    return render_template('/administrador/editar_perfil_adm.html')

@app.route('/cadastro_empresa', methods=['GET', 'POST'])
def cadastro_empresa():
    registrar()
    if request.method == "POST":
        nome_empresa = request.form.get("nome")
        cidade_empresa = request.form.get("cidade")
        bairro_empresa = request.form.get("bairro")
        rua_empresa = request.form.get("rua")
        numero_empresa = request.form.get("numero")
        cnpj_empresa = request.form.get("cnpj")
        id_ponto = request.form.get("id_ponto")

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
        return redirect(url_for('index'))

    return render_template('empresa/cadastro_empresa.html')

@app.route("/perfil_usuarios", methods=['GET','POST'])
def perfil_usuarios():
    registrar()
    # verifica se o usuario está logado
    if 'usuario' not in session:
        return redirect(url_for('cadastro_usuario'))
    else:
        usuario = session['usuario']
        
        reserva_model = ReservaModel(usuario['id'], None, None, None)
        reservas = reserva_model.buscar_por_reservas()

        # Lista com todas as informações combinadas
        reservas_detalhadas = []

        for reserva in reservas:
            # Pega o quarto
            quarto_model = QuartoModel(reserva['id_quarto'], None, None, None, None, None, None, None)
            quarto = quarto_model.buscar_por_quarto()

            # Pega o hotel do quarto
            hotel_model = HotelModel(quarto['id_hotel'], None, None, None, None, None, None, None)
            hotel = hotel_model.buscar_por_hotel()

            # Junta tudo num dicionário
            reservas_detalhadas.append({
                'reserva': reserva,
                'quarto': quarto,
                'hotel': hotel
            })

        return render_template('/usuario/perfil_usuario.html', usuario=usuario, reservas=reservas_detalhadas)

@app.route("/editar_perfil_usuario", methods=['GET', 'POST'])
def editar_perfil_usuario():
    id = session['usuario']['id']
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    foto = request.files.get('imagem')
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
        return redirect(url_for('perfil_usuarios'))
    return render_template('/usuario/editar_perfil_usuario.html')


# @app.route('/reservas', methods=['GET', 'POST'])
# def reservas():
#     registrar()
#     imagem = request.form.get("foto")
#     id = 18
#     db = Database() 
#     db.connect() 
#     sql = 'UPDATE usuarios SET imagem=? WHERE id=?'
#     db.execute(sql, (imagem, id))
#     db.commit()

#     db.close()
    
#     return render_template('reservas.html')

# @app.route('/cancelar_reserva', methods=['GET', 'POST'])
# def cancelar_reserva():
#     registrar()
#     if request.method == 'POST':
#         reserva_id = request.form.get('id_reserva')
        
#         db = Database()
#         db.connect()
        
#         sql = "DELETE FROM reservas WHERE id_reserva=?"
#         db.execute(sql, (reserva_id,))
#         db.commit()
        
#         db.close()
        
#         flash('Reserva cancelada com sucesso!', 'success')
#         return redirect(url_for('perfil_usuarios'))
    
#     flash('Erro ao cancelar a reserva.', 'error')
#     return redirect(url_for('perfil_usuarios'))

# @app.route('/quartos', methods=['GET', 'POST'])
# def quartos():
#     mes_disponivel = request.form.get("mes_disponivel")
#     imagem = request.form.get("imagem")
#     andar = request.form.get("andar")
#     numero_quarto = request.form.get("numero_quarto")
#     preco = request.form.get("preco")
#     id_hotel = session["empresa"]["id"]

#     db = Database() 
#     db.connect() 
#     sql = 'UPDATE quartos SET andar=?, numero_quarto=?, preco=?, mes_disponivel=?, imagem=?, id_hotel=? WHERE id = ?'
#     db.execute(sql, (andar, numero_quarto, preco, mes_disponivel, imagem, id_hotel, id))
#     db.commit()

#     db.close()
    
#     return render_template('quartos.html')

@app.route('/quem_somos')
def quem_somos():
    return render_template('quem_somos.html')

@app.route('/sair')
def sair():
    registrar()
    session.pop('usuario', None)
    session.pop('adm', None)
    return redirect(url_for('index'))

#@app.route('hoteis')
#def style():
    #return render_template('')

if __name__=="__main__":
    app.run(debug=True)
