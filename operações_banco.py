import sqlite3
def deletar_usuario():
    i = 1
    while i != 0:
        i = int(input("Digite o ID:"))
        connect = sqlite3.connect("SITE.db")
        cursor = connect.cursor()
        sql = "DELETE FROM usuarios WHERE id=?"
        cursor.execute(sql, (i,))
        connect.commit()
        connect.close()

def checar_senha():
    email = str(input("Email: "))
    senha = int(input("Senha"))
    connect = sqlite3.connect("SITE.db")
    cursor = connect.cursor()
    sql = "SELECT * FROM usuarios WHERE email=? AND senha=?"
    cursor.execute(sql, (email, senha))
    usuario = cursor.fetchone()
    connect.close()
    if usuario:
        print(usuario[1])
    else:
        print("Erro")

def inserir_hotel():
    primeiro = str(input("Primeiro: "))
    segundo = str(input("Segundo: "))
    connect = sqlite3.connect("banco_de_dados.db")
    cursor = connect.cursor()
    sql = "INSERT INTO teste (titulo, descricao) VALUES (?, ?)"
    cursor.execute(sql, (primeiro, segundo))
    connect.commit()
    connect.close() 
