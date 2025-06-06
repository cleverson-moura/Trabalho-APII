import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from connect import Database

db = Database()

def cadastrar_usuario():
    db.connect()
    
    nome = str(input('Nome do usuario a cadastrar: ')).lower()
    email = str(input('E-mail do usuario a cadastrar: '))
    senha = str(input('Senha do usuario a cadastrar: '))
    cpf = str(input('CPF somente com números: '))
    img_perfil = "imagens/foto_perfil.jpg"
    
    sql = '''INSERT INTO usuarios(nome, email, senha, cpf, imagem)
             VALUES (?, ?, ?, ?, ?)'''
    db.execute(sql, (nome, email, senha, cpf, img_perfil))
    db.commit()
    
    with open('usuarios.txt', 'a') as arquivo_usuarios:
        arquivo_usuarios.write(f'{nome}, {email}, {senha}, {cpf}\n')
    
    db.close()

def ver_usuario():
    db.connect()
    
    acao = int(input('Ver todos os usuarios(1), ver um usuario(2): '))
    
    if acao == 1:
        sql = 'SELECT * FROM usuarios'
        usuarios = db.query(sql)
        for usuario in usuarios:
            print(usuario)
    elif acao == 2:
        nome_usuario = str(input('Nome do usuario cadastrado: ')).lower()
        sql = 'SELECT * FROM usuarios WHERE nome = ?'
        usuario = db.query(sql, (nome_usuario,))
        if usuario:
            print(usuario[0])
        else:
            print('Usuário não encontrado.')
    else:
        print('Ação inválida.')
    
    db.close()

def atualizar_usuario():
    db.connect()
    
    id_usuario = int(input('Id do usuário para atualização: '))
    nome = str(input('Novo nome do usuario a atualizar: ')).lower()
    email = str(input('Novo e-mail do usuario a atualizar: '))
    senha = str(input('Nova senha do usuario a atualizar: '))
    cpf = str(input('Novo CPF somente com números: '))
    
    sql = '''UPDATE usuarios
             SET nome = ?, email = ?, senha = ?, cpf = ?
             WHERE id = ?'''
    db.execute(sql, (nome, email, senha, cpf, id_usuario))
    db.commit()
    db.close()

def deletar_usuario():
    db.connect()
    
    id_usuario = int(input('Id do usuário que deseja deletar: '))
    acao = input(f'Tem certeza que deseja deletar o cadastro do usuário id={id_usuario}? (s/n): ').lower()
    
    if acao in ['s', 'sim']:
        sql = 'DELETE FROM usuarios WHERE id = ?'
        db.execute(sql, (id_usuario,))
        db.commit()
    
    db.close()

def main():
    acao = int(input('Cadastrar(1), ver usuários(2), atualizar cadastro(3), deletar usuário(4): '))
    
    if acao == 1:
        cadastrar_usuario()
    elif acao == 2:
        ver_usuario()
    elif acao == 3:
        atualizar_usuario()
    elif acao == 4:
        deletar_usuario()
    else:
        print('Erro: ação inválida.')

if __name__ == '__main__':
    main()
