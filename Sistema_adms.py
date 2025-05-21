import sqlite3
from flask import Flask

def cadastrar_admin():
    nome = str(input("Nome: "))
    cpf = int(input("CPF: "))
    email = str(input("Email: "))
    senha = str(input("Senha: "))
    con = sqlite3.connect("administradores.db")
    cursor = con.cursor()
    sql = "INSERT INTO administradores (nome, cnpj, email, senha) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(sql, (nome, cpf, email, senha))
    con.commit()
    con.close()

def deletar_admin():
    x = int(input("ID: "))
    con = sqlite3.connect("administradores.db")
    cursor = con.cursor()
    sql = "DELETE FROM administradores WHERE id = ? "
    cursor.execute(sql, (x,))
    con.commit()
    con.close()

def editar_admin():
    x = int(input("ID: "))
    nome = str(input("Nome: "))
    cpf = int(input("CPF: "))
    email = str(input("Email: "))
    senha = str(input("Senha: "))
    con = sqlite3.connect("administradores.db")
    cursor = con.cursor()
    sql = "UPDATE administradores SET nome=?, cnpj=?, email=?, senha=? WHERE id=?"
    cursor.execute(sql, (nome, cpf, email, senha, x))
    con.commit()
    con.close()

escolha = int(input("Escolha: "))
if escolha == 1:
    cadastrar_admin()
if escolha == 2:
    editar_admin()
if escolha == 3:
    deletar_admin()
