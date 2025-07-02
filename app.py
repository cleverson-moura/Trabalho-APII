from flask import Flask, render_template, request, redirect, url_for, flash, session
#from models.connect import Database # Importação da Classe com as funções de banco de dados
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from routes import register_blueprints

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
    elif 'adm' in session:
        icone = "/static/{}".format(session['adm']['imagem'])
        endereco = "/perfil_adm"
    else:
        icone = "/static/imagens/user.png"
        endereco = "/cadastro"
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

#@app.route('/salvar_quartos')
#   def salvar_quartos():
#        return render_template('salvar_quartos.html')

if __name__=="__main__":
    app.run(debug=True)
