from flask import Flask

import sqlite3

con = sqlite3.connect("SITE.db")
                               
cursor = con.cursor()



'''
Sistema

'''


    
def cadastrar_hotel():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    nome = str(input('Nome do hotel a cadastrar: '))
    cidade = str(input('Cidade do hotel a cadastrar: '))
    bairro = str(input('Bairro do hotel a cadastrar: '))
    rua = str(input('Rua do hotel a cadastrar: '))
    numero = str(input('Número do hotel a cadastrar: '))
    cnpj = int(input('CNPJ somente com números: '))

    cursor.execute('''INSERT INTO hoteis(nome, cidade, bairro, rua, numero, cnpj)
                   VALUES(?, ?, ?, ?, ?, ?)''',
                   (nome, cidade, bairro, rua, numero, cnpj))
    con.commit()
    con.close()

    arquivo_hoteis = open('hoteis.txt', 'a')
    arquivo_hoteis.write(f'{nome}, {cidade}, {bairro}, {rua}, {numero}, {cnpj}\n')
    arquivo_hoteis.close()
    
def ver_hotel():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    acao = int(input('Ver todos os hoteis(1), ver um hotel(2): '))
    
    if acao == 1:
        cursor.execute('SELECT * FROM hoteis')
        
        todos_os_hoteis = cursor.fetchall()
        
        for hotel in todos_os_hoteis:
            print(hotel)
        
    elif acao == 2:
        nome_hotel = str(input('Nome do hotel cadastrado: '))
        
        cursor.execute('SELECT * FROM hoteis WHERE nome = ?', (nome_hotel,))
        
        dados_hotel = cursor.fetchone()
        
        print(dados_hotel)

    con.commit()
    con.close()


        
def atualizar_hotel():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    id_hotel = int(input('Id do hotel para atualização: '))
    nome = str(input('Nome do hotel a cadastrar: '))
    cidade = str(input('Cidade do hotel a cadastrar: '))
    bairro = str(input('Bairro do hotel a cadastrar: '))
    rua = str(input('Rua do hotel a cadastrar: '))
    numero = str(input('Número do hotel a cadastrar: '))
    cnpj = int(input('CNPJ somente com números: '))

    cursor.execute('''UPDATE hoteis 
                   SET nome = ?,cidade = ?,bairro = ?,rua = ?, numero = ?, cnpj = ?
                   WHERE id = ?''', (nome, cidade, bairro, rua, numero, cnpj, id_hotel))
    con.commit()
    con.close()


def deletar_hotel():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    id_hotel = int(input('Id do hotel que deseja deletar: '))
    acao = str(input(f'Tem certeza que deseja deletar o cadastro do hotel de id = {id_hotel}?')).lower()
    if acao == 'sim' or acao == 's':
        cursor.execute('DELETE FROM hoteis WHERE id = ?',(id_hotel,))

    con.commit()
    con.close()


def main():

    acao = int(input('Cadastrar(1), ver hoteis(2), atualizar cadastro(3), deletar hotel(4): '))
    if acao == 1:
        cadastrar_hotel()
    elif acao == 2:
        ver_hotel()
    elif acao == 3:
        atualizar_hotel()
    elif acao == 4:
        deletar_hotel()
    else:
        print('Erro')
        return
    
main()
con.close()