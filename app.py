from flask import Flask, render_template, request, redirect, url_for, flash
from connect import Database # Importação da Classe com as funções de banco de dados
import re

# def conectar_banco():
#     con = sqlite3.connect("banco_de_dados.db")
#     return con

app = Flask(__name__) 

# def get_db_connection():
#     conn = sqlite3.connect('banco_de_dados.db')
#     conn.row_factory = sqlite3.Row
#     return conn

@app.route('/')
def index():
    texto = "Vamos ver"
    return render_template('index.html', texto=texto)

@app.route('/pontos')
def pontos():
    # usando o osjeto de conexão com banco de dados
    db = Database() # cria o objeto
    db.connect() # conecta ao banco
    db.execute('SELECT * FROM teste') # executa o SQL
    ponto = db.fetchall() # retorna uma lista com as linhas da tabela
    db.close()
    
    
    return render_template('pontos.html', ponto=ponto)

@app.route('/cadastro')
def cadastro():
    return render_template('Popup_cadastro.html')

@app.route('/cadastro-usuario')
def cadastro_usuario():
    return render_template('cadastro_usuario.html')

@app.route('/cadastro-empresas')
def cadastro_empresas():
    return render_template('cadastro_empresas.html')

@app.route('/perfil-empresas')
def perfil_empresas():
    return render_template('perfil_empresas.html')

@app.route('/perfil-usuarios')
def perfil_usuarios():
    return render_template('perfil_usuarios.html')

@app.route('/reservas')
def reservas():
    return render_template('reservas.html')

@app.route('/quem-somos')
def quem_somos():
    return render_template('quem_somos.html')




#@app.route('hoteis')
#def style():
    #return render_template('')

if __name__=="__main__":
    app.run(debug=True)