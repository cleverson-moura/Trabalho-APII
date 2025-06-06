from flask import Flask

import sqlite3

con = sqlite3.connect("SITE.db")
                               
cursor = con.cursor()



'''
Sistema

'''


    
def cadastrar_ponto_turistico():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    nome = str(input('Nome do ponto turístico a cadastrar: '))
    cidade = str(input('Cidade do ponto turístico a cadastrar: '))
    bairro = str(input('Bairro do ponto turístico a cadastrar: '))
    rua = str(input('Rua do ponto turístico a cadastrar: '))
    numero = str(input('Número do ponto turístico a cadastrar: '))
    info = int(input('Informações extras: '))

    cursor.execute('''INSERT INTO pontos_turisticos(nome, cidade, bairro, rua, numero, info)
                   VALUES(?, ?, ?, ?, ?, ?)''',
                   (nome, cidade, bairro, rua, numero, info))
    con.commit()
    con.close()

    arquivo_pontos_turisticos = open('registros/pontos_turisticos.txt', 'a')
    arquivo_pontos_turisticos.write(f'{nome}, {cidade}, {bairro}, {rua}, {numero}, {info}\n')
    arquivo_pontos_turisticos.close()
    
def ver_ponto_turistico():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    acao = int(input('Ver todos os pontos turísticos(1), ver um ponto turístico(2): '))
    
    if acao == 1:
        cursor.execute('SELECT * FROM pontos_turisticos')
        
        todos_os_pontos_turisticos = cursor.fetchall()
        
        for ponto_turistico in todos_os_pontos_turisticos:
            print(ponto_turistico)
        
    elif acao == 2:
        nome_ponto_turistico = str(input('Nome do ponto turístico cadastrado: '))
        
        cursor.execute('SELECT * FROM pontos_turisticos WHERE nome = ?', (nome_ponto_turistico,))
        
        dados_ponto_turistico = cursor.fetchone()
        
        print(dados_ponto_turistico)

    con.commit()
    con.close()


        
def atualizar_ponto_turistico():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    id_ponto_turistico = int(input('Id do ponto turístico para atualização: '))
    nome = str(input('Nome do pontoturístico a cadastrar: '))
    cidade = str(input('Cidade do ponto turístico a cadastrar: '))
    bairro = str(input('Bairro do ponto turístico a cadastrar: '))
    rua = str(input('Rua do ponto turístico a cadastrar: '))
    numero = str(input('Número do ponto turístico a cadastrar: '))
    info = int(input('Informações extras: '))

    cursor.execute('''UPDATE pontos_turisticos 
                   SET nome = ?,cidade = ?,bairro = ?,rua = ?, numero = ?, info = ?
                   WHERE id = ?''', (nome, cidade, bairro, rua, numero, info, id_ponto_turistico))
    con.commit()
    con.close()


def deletar_ponto_turistico():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    id_ponto_turistico = int(input('Id do ponto turístico que deseja deletar: '))
    acao = str(input(f'Tem certeza que deseja deletar o cadastro do ponto turístico de id = {id_ponto_turistico}?')).lower()
    if acao == 'sim' or acao == 's':
        cursor.execute('DELETE FROM pontos_turisticos WHERE id = ?',(id_ponto_turistico,))

    con.commit()
    con.close()


def main():

    acao = int(input('Cadastrar(1), ver pontos turísticos(2), atualizar cadastro(3), deletar ponto turístico(4): '))
    if acao == 1:
        cadastrar_ponto_turistico()
    elif acao == 2:
        ver_ponto_turistico()
    elif acao == 3:
        atualizar_ponto_turistico()
    elif acao == 4:
        deletar_ponto_turistico()
    else:
        print('Erro')
        return
    
main()
con.close()