from flask import Flask

import sqlite3

con = sqlite3.connect("SITE.db")
                               
cursor = con.cursor()



'''
Sistema

'''


    
def cadastrar_quarto():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    andar = str(input('Andar do quarto a cadastrar: '))
    numero = str(input('Numero do quarto a cadastrar: '))
    numero_reserva = str(input('Número da reserva do quarto a cadastrar: '))
    chave_quarto = str(input('Chave do quarto a cadastrar: '))

    cursor.execute('''INSERT INTO quartos(andar, numero, numero_reserva, chave_quarto)
                   VALUES(?, ?, ?, ?)''',
                   (andar, numero, numero_reserva, chave_quarto))
    con.commit()
    con.close()

    arquivo_quartos = open('quartos.txt', 'a')
    arquivo_quartos.write(f'{andar}, {numero}, {numero_reserva}, {chave_quarto}\n')
    arquivo_quartos.close()
    
def ver_quarto():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    acao = int(input('Ver todos os quartos(1), ver um quarto(2): '))
    
    if acao == 1:
        cursor.execute('SELECT * FROM quartos')
        
        todos_os_quartos = cursor.fetchall()
        
        for quarto in todos_os_quartos:
            print(quarto)
        
    elif acao == 2:
        numero_quarto = str(input('Número do quarto cadastrado: '))
        
        cursor.execute('SELECT * FROM quartos WHERE numero = ?', (numero_quarto,))
        
        dados_quarto = cursor.fetchone()
        
        print(dados_quarto)

    con.commit()
    con.close()


        
def atualizar_quarto():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    id_quarto = int(input('Id do quarto para atualização: '))
    andar = str(input('Andar do quarto a cadastrar: '))
    numero = str(input('Numero do quarto a cadastrar: '))
    numero_reserva = str(input('Número da reserva do quarto a cadastrar: '))
    chave_quarto = str(input('Chave do quarto a cadastrar: '))

    cursor.execute('''UPDATE quartos 
                   SET andar = ?,numero = ?,numero_reserva = ?,chave_quarto = ?
                   WHERE id = ?''', (andar, numero, numero_reserva, chave_quarto, id_quarto))
    con.commit()
    con.close()


def deletar_quarto():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    id_quarto = int(input('Id do quarto que deseja deletar: '))
    acao = str(input(f'Tem certeza que deseja deletar o cadastro do quarto de id = {id_quarto}?')).lower()
    if acao == 'sim' or acao == 's':
        cursor.execute('DELETE FROM quartos WHERE id = ?',(id_quarto,))

    con.commit()
    con.close()


def main():

    acao = int(input('Cadastrar(1), ver quartos(2), atualizar cadastro(3), deletar quarto(4): '))
    if acao == 1:
        cadastrar_quarto()
    elif acao == 2:
        ver_quarto()
    elif acao == 3:
        atualizar_quarto()
    elif acao == 4:
        deletar_quarto()
    else:
        print('Erro')
        return
    
main()
con.close()