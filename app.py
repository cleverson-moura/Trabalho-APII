from flask import Flask, render_template, request, redirect, url_for, flash, session
#from models.connect import Database # Importação da Classe com as funções de banco de dados
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from routes import register_blueprints

from models.usuario_model import UsuarioModel
from models.reserva_model import ReservaModel
from models.quarto_model import QuartoModel
from models.hotel_model import HotelModel

def registrar():
    ip_usuario = request.remote_addr
    tempo_acesso = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    url_visitada = request.path
    ip_usuario = request.remote_addr
    with open('registros/registros_acessos.txt', 'a') as f:
        f.write(f'{tempo_acesso} | IP:{ip_usuario} | URL:{url_visitada}\n')
        ## Parte q registra o acesso em arquivo.txt ##

app = Flask(__name__)
app.secret_key = "123"
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

# Certifique-se que a pasta exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
register_blueprints(app)

@app.route('/pontos')
def pontos():
    if 'usuario' in session:
        icone = "/static/{}".format(session['usuario']['imagem'])
        endereco = "/perfil_usuario"
    elif 'hotel' in session:
        icone = "/static/{}".format(session['hotel']['foto'])
        endereco = "/perfil_hotel"
    else:
        icone = "/static/imagens/user.png"
        endereco = "/login"
    texto = "Vamos ver"
    registrar()
    # usando o osjeto de conexão com banco de dados
    #connect = sqlite3.connect("database/banco/banco_de_dados.db") # cria o objeto
    #cursor = connect.cursor() # conecta ao banco
    #cursor.execute('SELECT * FROM teste') # executa o SQL
    #ponto = cursor.fetchall() # retorna uma lista com as linhas da tabela
    #tamanho = len(ponto)
    #connect.close()
    return render_template('pontos.html', icone=icone, endereco=endereco)


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

@app.route('/salvar_quartos', methods=['GET'])
def exibir_formulario_quarto():
    return render_template('quarto/salvar_quartos.html')

@app.route('/salvar_quarto', methods=['POST'])
def salvar_quarto():
    mes_disponivel = request.form.get('mes_disponivel')
    andar = request.form.get('andar')
    numero = request.form.get('numero_quarto')
    preco = request.form.get('preco')
    imagem = request.files['imagem']

    if imagem and imagem.filename != '':
        nome_arquivo = secure_filename(imagem.filename)
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
        imagem.save(caminho)
        imagem_path = f'uploads/{nome_arquivo}'
    else:
        imagem_path = 'imagens/default.png'

    id_hotel = session['hotel']['id']
    quarto = QuartoModel(
        andar=andar,
        numero=numero,
        preco=preco,
        imagem=imagem_path,
        mes_disponivel=mes_disponivel,
        id_hotel=id_hotel
    )
    quarto.inserir()

    flash('Quarto cadastrado com sucesso!', 'success')
    return redirect('/salvar_quartos')

if __name__=="__main__":
    app.run(debug=True)

