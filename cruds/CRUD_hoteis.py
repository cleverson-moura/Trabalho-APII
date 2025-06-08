import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.connect import Database  # ou from database import Database

def cadastrar_hotel():
    db = Database()
    db.connect()

    nome = input('Nome do hotel a cadastrar: ')
    cidade = input('Cidade do hotel a cadastrar: ')
    bairro = input('Bairro do hotel a cadastrar: ')
    rua = input('Rua do hotel a cadastrar: ')
    numero = input('Número do hotel a cadastrar: ')
    cnpj = int(input('CNPJ somente com números: '))

    sql = '''
        INSERT INTO hoteis (nome, cidade, bairro, rua, numero, cnpj)
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    db.execute(sql, (nome, cidade, bairro, rua, numero, cnpj))
    db.commit()
    db.close()

    with open('registros/hoteis.txt', 'a') as arquivo:
        arquivo.write(f'{nome}, {cidade}, {bairro}, {rua}, {numero}, {cnpj}\n')


def ver_hotel():
    db = Database()
    db.connect()

    acao = int(input('Ver todos os hotéis (1), ver um hotel (2): '))

    if acao == 1:
        resultado = db.execute("SELECT * FROM hoteis").fetchall()
        for hotel in resultado:
            print(dict(hotel))
    elif acao == 2:
        nome_hotel = input('Nome do hotel cadastrado: ')
        resultado = db.execute("SELECT * FROM hoteis WHERE nome = ?", (nome_hotel,)).fetchone()
        print(dict(resultado) if resultado else "Hotel não encontrado.")

    db.close()


def atualizar_hotel():
    db = Database()
    db.connect()

    id_hotel = int(input('ID do hotel para atualização: '))
    nome = input('Novo nome: ')
    cidade = input('Nova cidade: ')
    bairro = input('Novo bairro: ')
    rua = input('Nova rua: ')
    numero = input('Novo número: ')
    cnpj = int(input('Novo CNPJ: '))

    sql = '''
        UPDATE hoteis 
        SET nome = ?, cidade = ?, bairro = ?, rua = ?, numero = ?, cnpj = ?
        WHERE id = ?
    '''
    db.execute(sql, (nome, cidade, bairro, rua, numero, cnpj, id_hotel))
    db.commit()
    db.close()


def deletar_hotel():
    db = Database()
    db.connect()

    id_hotel = int(input('ID do hotel que deseja deletar: '))
    confirm = input(f'Deseja realmente deletar o hotel de ID = {id_hotel}? (s/n): ').lower()

    if confirm in ['s', 'sim']:
        db.execute('DELETE FROM hoteis WHERE id = ?', (id_hotel,))
        db.commit()

    db.close()


def main():
    op = int(input('Cadastrar (1), Ver (2), Atualizar (3), Deletar (4): '))
    if op == 1:
        cadastrar_hotel()
    elif op == 2:
        ver_hotel()
    elif op == 3:
        atualizar_hotel()
    elif op == 4:
        deletar_hotel()
    else:
        print('Opção inválida.')

if __name__ == "__main__":
    main()
