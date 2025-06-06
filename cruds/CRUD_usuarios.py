import pickle
import sqlite3


dicionario_usuarios = {
"Nome": 'digite',
"Email": 'digite',
"Senha": 'digite',
"CPF": 'digite'
}



'''
Sistema

'''

    
def cadastrar_usuario():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    nome = str(input('Nome do usuario a cadastrar: ')).lower()
    email = str(input('E-mail do usuario a cadastrar: '))
    senha = str(input('Senha do usuario a cadastrar: '))
    cpf = str(input('CPF somentecom números: '))
    img_perfil = "imagens/foto_perfil.jpg"

    dicionario_usuarios.update({
    "Nome": nome,
    "Email": email,
    "Senha": senha,
    "CPF": cpf
    })

    cursor.execute('''INSERT INTO usuarios(nome, email, senha, cpf, imagem)
                   VALUES(?, ?, ?, ?, ?)''',
                   (nome, email, senha, cpf, img_perfil))
    con.commit()
    con.close()
    a = ' '
    for chave, valor in dicionario_usuarios.items():
        a += (f'{chave}: {valor}, ')

    arquivo_users = open('users.txt', 'a')
    arquivo_users.write(f'{a}\n\n')
    arquivo_users.close()
    
def ver_usuario():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    acao = int(input('Ver todos os usuarios(1), ver um usuario(2): '))
    
    if acao == 1:
        cursor.execute('SELECT * FROM usuarios')
        
        todos_os_usuarios = cursor.fetchall()
        
        for usuario in todos_os_usuarios:
            print(usuario)
        
    elif acao == 2:
        nome_usuario = str(input('Nome do usuario cadastrado: '))
        
        cursor.execute('SELECT * FROM usuarios WHERE nome = ?', (nome_usuario,))
        
        dados_usuario = cursor.fetchone()
        
        print(dados_usuario)

    con.commit()
    con.close()


        
def atualizar_usuario():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    id_usuario = int(input('Id do usuário para atualização: '))
    nome = str(input('Novo nome do usuario a atualizar: ')).lower()
    email = str(input('Novo e-mail do usuario a atualizar: '))
    senha = str(input('Nova senha do usuario a atualizar: '))
    cpf = str(input('Novo CPF somente com números: '))

    cursor.execute('''UPDATE usuarios 
                   SET nome = ?,email = ?,senha = ?,cpf = ?
                   WHERE id = ?''', (nome, email, senha, cpf, id_usuario))
    con.commit()
    con.close()


def deletar_usuario():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")


    id_usuario = int(input('Id do usuário que deseja deletar: '))
    acao = str(input(f'Tem certeza que deseja deletar o cadastro do usuário de id = {id_usuario}?')).lower()
    if acao == 'sim' or acao == 's':
        cursor.execute('DELETE FROM usuarios WHERE id_usuario = ?',(id_usuario,))
        con.commit()
    con.commit()
    con.close()


def main():

    acao = int(input('Cadastrar(1), ver usuarios(2), atualizar cadastro(3), deletar usuario(4): '))
    if acao == 1:
        cadastrar_usuario()
    elif acao == 2:
        ver_usuario()
    elif acao == 3:
        atualizar_usuario()
    elif acao == 4:
        deletar_usuario()
    else:
        print('Erro')
        return
    
main()

def deletar_todos_usuarios():
    con = sqlite3.connect("SITE.db")                          
    cursor = con.cursor()
    cursor.execute('DELETE FROM usuarios')
    con.commit()
    con.close()