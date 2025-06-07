from flask import Flask, render_template, request, redirect, url_for, flash, session
from connect import Database # Importação da Classe com as funções de banco de dados
import sqlite3
import re
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "123"
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

# Certifique-se que a pasta exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    texto = "Vamos ver"
    return render_template('index.html', texto=texto)

@app.route('/pontos')
def pontos():
    # usando o osjeto de conexão com banco de dados
    connect = sqlite3.connect("banco_de_dados.db") # cria o objeto
    cursor = connect.cursor() # conecta ao banco
    cursor.execute('SELECT * FROM teste') # executa o SQL
    ponto = cursor.fetchall() # retorna uma lista com as linhas da tabela
    tamanho = len(ponto)
    connect.close()
    
    
    return render_template('pontos.html', ponto=ponto, tamanho=tamanho)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    email = request.form.get("nome")
    senha = request.form.get("senha")

    db = Database()
    db.connect()

    sql = ('SELECT * FROM usuarios WHERE email=? AND senha=?')
    db.execute(sql,(email, senha))
    usuario = db.fetchone()

    sql = "SELECT * FROM administradores WHERE email=? AND senha=?"
    db.execute(sql,(email, senha))
    empresa = db.fetchone()

    db.close()
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
    elif empresa:
        session['empresa'] = {
                    'id': empresa['id_adm'],
                    'nome': empresa['nome'],
                    'cpf': empresa['cpf'],
                    'email': empresa['email'],
                    'senha': empresa['senha']
                    # 'imagem': empresa[5]
                }
        return redirect(url_for("perfil_empresas"))
    else:
        print("Erro")
        
    
    return render_template('Popup_cadastro.html')

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == "POST":
        nome_usuario = request.form.get('nome')
        cpf_usuario = request.form.get('cpf')
        email_usuario = request.form.get('email')
        senha_usuario = request.form.get('senha')
        foto_usuario = request.files['foto']

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
        
    return render_template('cadastro_usuario.html')

@app.route('/cadastro_empresas', methods=['GET', 'POST'])
def cadastro_empresas():
    if request.method == "POST":
        nome_empresa = request.form.get("nome")
        email_empresa = request.form.get("email")
        senha_empresa = request.form.get("senha")
        cpf_empresa = request.form.get("cpf")
        foto_empresa = request.files['foto-empresa']

        if foto_empresa:
            filename = secure_filename(foto_empresa.filename)
            caminho_foto_empresa = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto_empresa.save(caminho_foto_empresa)
            
            caminho_relativo_foto_empresa = f'uploads/{filename}'

            db = Database()
            db.connect()
            sql = "INSERT INTO administradores(nome, cpf, email, senha, imagem) VALUES (?, ?, ?, ?, ?)"
            db.execute(sql, (nome_empresa, cpf_empresa, email_empresa, senha_empresa, caminho_relativo_foto_empresa))
            db.commit()

            sql = "SELECT * FROM administradores WHERE email=? and senha=?"
            db.execute(sql, (email_empresa, senha_empresa))
            resultado = db.fetchone()
            
            if resultado:
                session['empresa'] = {
                    'id': resultado[0],
                    'nome': resultado[1],
                    'cpf': resultado[2],
                    'email': resultado[3],
                    'senha': resultado[4],
                    'foto': resultado[5]
                }
            db.close()
            return redirect(url_for('perfil_empresas'))
    return render_template('cadastro_empresas.html')

@app.route('/perfil_empresas', methods=['GET', 'POST'])
def perfil_empresas():
    if 'empresa' not in session:
        return redirect(url_for('cadastro_empresas'))
    else:
        empresa = session['empresa']
        return render_template('perfil_empresa.html',empresa=empresa)

@app.route("/perfil_usuarios", methods=['GET','POST'])
def perfil_usuarios():
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

        return render_template('perfil_usuario.html', usuario=usuario, reservas=reservas_detalhadas)

@app.route('/reservas', methods=['GET', 'POST'])
def reservas():
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

@app.route('/quem_somos')
def quem_somos():
    return render_template('quem_somos.html')




#@app.route('hoteis')
#def style():
    #return render_template('')

if __name__=="__main__":
    app.run(debug=True)
