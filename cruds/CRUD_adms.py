from flask import Flask
import sqlite3

con = sqlite3.connect("SITE.db")
                               
cursor = con.cursor()



'''
Sistema

'''


    
def cadastrar_administrador():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    nome = str(input('Nome do administrador a cadastrar: ')).lower()
    email = str(input('E-mail do administrador a cadastrar: '))
    senha = str(input('Senha do administrador a cadastrar: '))
    cpf = str(input('CPF somentecom números: '))

    cursor.execute('''INSERT INTO administradores(nome, email, senha, cpf)
                   VALUES(?, ?, ?, ?)''',
                   (nome, email, senha, cpf))
    con.commit()
    con.close()

    arquivo_adms = open('registros/adms.txt', 'a')
    arquivo_adms.write(f'{nome}, {email}, {senha}, {cpf}\n')
    arquivo_adms.close()
    
def ver_administrador():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    acao = int(input('Ver todos os administradores(1), ver um só(2): '))
    
    if acao == 1:
        cursor.execute('SELECT * FROM administradores')
        
        todos_os_administradores = cursor.fetchall()
        
        for administrador in todos_os_administradores:
            print(administrador)
        
    elif acao == 2:
        nome_administrador = str(input('Nome do administrador cadastrado: '))
        
        cursor.execute('SELECT * FROM administradores WHERE nome = ?', (nome_administrador,))
        
        dados_administrador = cursor.fetchone()
        
        print(dados_administrador)

    con.commit()
    con.close()


        
def atualizar_administrador():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    id_administrador = int(input('Id do administrador para atualização: '))
    nome = str(input('Novo nome do administrador a atualizar: ')).lower()
    email = str(input('Novo e-mail do administrador a atualizar: '))
    senha = str(input('Nova senha do administrador a atualizar: '))
    cpf = str(input('Novo CPF somente com números: '))

    cursor.execute('''UPDATE administradores 
                   SET nome = ?,email = ?,senha = ?,cpf = ?
                   WHERE id = ?''', (nome, email, senha, cpf, id_administrador))
    con.commit()
    con.close()


def deletar_administrador():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    id_administrador = int(input('Id do administrador que deseja deletar: '))
    acao = str(input(f'Tem certeza que deseja deletar o cadastro do administrador de id = {id_administrador}?')).lower()
    if acao == 'sim' or acao == 's':
        cursor.execute('DELETE FROM administradores WHERE id = ?',(id_administrador,))

    con.commit()
    con.close()


def main():

    acao = int(input('Cadastrar(1)\n Ver administradores(2)\n Atualizar cadastro(3)\n Deletar administrador(4) '))
    if acao == 1:
        cadastrar_administrador()
    elif acao == 2:
        ver_administrador()
    elif acao == 3:
        atualizar_administrador()
    elif acao == 4:
        deletar_administrador()
    else:
        print('Erro')
        return
    
main()
con.close()