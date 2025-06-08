from flask import Flask, render_template, request, redirect, url_for, flash, session
from connect import Database # Importação da Classe com as funções de banco de dados
import sqlite3
import re
import os
from werkzeug.utils import secure_filename
from datetime import datetime

from models.usuario_model import UsuarioModel
from models.administrador_model import AdministradorModel

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
        icone = "/static/{}".format(session['usuario']['foto'])
        endereco = "/perfil_usuarios"
    elif 'adm' in session:
        icone = "/static/{}".format(session['adm']['foto'])
        endereco = "/perfil_adm"
    else:
        icone = "/static/imagens/user.png"
        endereco = "/cadastro"
    texto = "Vamos ver"
    return render_template('index.html', texto=texto, icone=icone, endereco=endereco)

@app.route('/pontos')
def pontos():
    if 'usuario' in session:
        icone = "/static/{}".format(session['usuario']['foto'])
        endereco = "/perfil_usuarios"
    elif 'adm' in session:
        icone = "/static/{}".format(session['adm']['foto'])
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

    usuario = UsuarioModel.buscar_por_email_senha(email, senha)
    adm
    
    if usuario:
        session['usuario'] = {
                    'id': usuario['id_usuario'],
                    'nome': usuario['nome'],
                    'email': usuario['email'],
                    'senha': usuario['senha'],
                    'cpf': usuario['cpf'],
                    'foto': usuario['imagem']
                }
        return redirect(url_for("perfil_usuarios"))
    elif adm:
        session['adm'] = {
                    'id': adm['id_adm'],
                    'nome': adm['nome'],
                    'cpf': adm['cpf'],
                    'email': adm['email'],
                    'senha': adm['senha'],
                    'foto': adm['foto']
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

            db = Database()
            db.connect()
            sql = "INSERT INTO usuarios (nome, cpf, email, senha, imagem) VALUES (?,?,?,?,?)"
            db.execute(sql,(nome_usuario,cpf_usuario,email_usuario,senha_usuario,caminho_relativo))
            db.commit()

            sql = "SELECT * FROM usuarios WHERE email=? and senha=?"
            db.execute(sql, (email_usuario, senha_usuario))
            resultado = db.fetchone()
            if resultado:
                # Guarda na session os dados do usuario em forma de dicionario
                session['usuario'] = {
                    'id': resultado[0],
                    'nome': resultado[1],
                    'email': resultado[2],
                    'senha': resultado[3],
                    'cpf': resultado[4],
                    'foto': resultado[5]
                }
            db.close()

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

            db = Database()
            db.connect()
            sql = "INSERT INTO administradores(nome, cpf, email, senha, imagem) VALUES (?, ?, ?, ?, ?)"
            db.execute(sql, (nome_adm, cpf_adm, email_adm, senha_adm, caminho_relativo_foto_adm))
            db.commit()

            sql = "SELECT * FROM administradores WHERE email=? and senha=?"
            db.execute(sql, (email_adm, senha_adm))
            resultado = db.fetchone()
            
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
            db.close()
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
    foto = request.files.get('foto')
    if foto:
        foto_nome = "uploads/{}".format(foto.filename)
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
        foto.save(caminho)
    else:
        foto_nome = session['adm']['imagem']
    if nome:
        db = Database()
        db.connect()
        sql = "UPDATE administradores SET nome=?, email=?, senha=?, imagem=? WHERE id_adm=?"
        db.execute(sql, (nome, email, senha, foto_nome, id))
        db.commit()
        sql = "SELECT * FROM administradores WHERE id_adm=?"
        db.execute(sql, (id,))
        adm = db.fetchone()
        db.close()
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


@app.route("/perfil_usuarios", methods=['GET','POST'])
def perfil_usuarios():
    registrar()
    # verifica se o usuario está logado
    if 'usuario' not in session:
        return redirect(url_for('cadastro_usuario'))
    else:
        usuario = session['usuario']

        # Conecta ao banco
        db = Database()
        db.connect()

        # Busca reservas do usuário
        sql = "SELECT * FROM reservas WHERE id_usuario=?"
        db.execute(sql, (usuario['id'],))
        reservas = db.fetchall()

        # Lista com todas as informações combinadas
        reservas_detalhadas = []

        for reserva in reservas:
            # Pega o quarto
            db.execute("SELECT * FROM quartos WHERE id_quarto=?", (reserva['id_quarto'],))
            quarto = db.fetchone()

            # Pega o hotel do quarto
            db.execute("SELECT * FROM hoteis WHERE id_hotel=?", (quarto['id_hotel'],))
            hotel = db.fetchone()

            # Junta tudo num dicionário
            reservas_detalhadas.append({
                'reserva': reserva,
                'quarto': quarto,
                'hotel': hotel
            })

            db.close()

        return render_template('/usuario/perfil_usuario.html', usuario=usuario, reservas=reservas_detalhadas)

@app.route("/editar_perfil_usuario", methods=['GET', 'POST'])
def editar_perfil_usuario():
    id = session['usuario']['id']
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    foto = request.files['foto']
    if foto:
        foto_nome = "uploads/{}".format(foto.filename)
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
        foto.save(caminho)
    else:
        foto_nome = session['usuario']['foto']
    if nome:
        db = Database()
        db.connect()
        sql = "UPDATE usuarios SET nome=?, email=?, senha=?, imagem=? WHERE id_usuario=?"
        db.execute(sql, (nome, email, senha, foto_nome, id))
        db.commit()
        sql = "SELECT * FROM usuarios WHERE id_usuario=?"
        db.execute(sql, (id,))
        usuario = db.fetchone()
        db.close()
        session['usuario'] = {
                    'id': usuario[0],
                    'nome': usuario[1],
                    'email': usuario[2],
                    'senha': usuario[3],
                    'cpf': usuario[4],
                    'foto': usuario[5]
                    }             
        return redirect(url_for('perfil_usuarios'))
    return render_template('/usuario/editar_perfil_usuario.html')


@app.route('/reservas', methods=['GET', 'POST'])
def reservas():
    registrar()
    imagem = request.form.get("foto")
    id = 18
    db = Database() 
    db.connect() 
    sql = 'UPDATE usuarios SET imagem=? WHERE id=?'
    db.execute(sql, (imagem, id))
    db.commit()

    db.close()
    
    return render_template('reservas.html')

@app.route('/cancelar_reserva', methods=['GET', 'POST'])
def cancelar_reserva():
    registrar()
    if request.method == 'POST':
        reserva_id = request.form.get('id_reserva')
        
        db = Database()
        db.connect()
        
        sql = "DELETE FROM reservas WHERE id_reserva=?"
        db.execute(sql, (reserva_id,))
        db.commit()
        
        db.close()
        
        flash('Reserva cancelada com sucesso!', 'success')
        return redirect(url_for('perfil_usuarios'))
    
    flash('Erro ao cancelar a reserva.', 'error')
    return redirect(url_for('perfil_usuarios'))

@app.route('/quartos', methods=['GET', 'POST'])
def quartos():
    mes_disponivel = request.form.get("mes")
    imagem = request.form.get("foto")
    andar = request.form.get("andar")
    numero_quarto = request.form.get("quarto")
    preco = request.form.get("preco")
    id_hotel = request.form.get("id_hotel")

    db = Database() 
    db.connect() 
    sql = 'UPDATE quartos SET andar=?, numero_quarto=?, preco=?, mes_disponivel=?, imagem=?, id_hotel=? WHERE id = ?'
    db.execute(sql, (andar, numero_quarto, preco, mes_disponivel, imagem, id_hotel, id))
    db.commit()

    db.close()
    
    return render_template('quartos.html')

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
