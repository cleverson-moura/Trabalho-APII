from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import re

def conectar_banco():
    con = sqlite3.connect("banco_de_dados.db")
    return con

app = Flask(__name__) 

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    texto = "Vamos ver"
    return render_template('index.html', texto=texto)

@app.route('/pontos')
def pontos():
    con = sqlite3.connect("banco_de_dados.db")
    cursor = con.cursor()
    ponto = cursor.execute("SELECT * FROM teste").fetchall()
    tponto = len(ponto)
    
    
    descricao = "Igreja muito massa"
    return render_template('pontos.html', descricao=descricao, ponto=ponto, tponto=tponto)

@app.route('/cadastro')
def cadastro():
    return render_template('Popup_cadastro.html')


#@app.houre('hoteis')
#def style():
    #return render_template('')

if __name__=="__main__":
    app.run(debug=True)