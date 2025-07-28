import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.connect import Database  # ou from database import Database

def cadastrar_quarto():
    db = Database()
    db.connect()

    andar = input('Andar do quarto a cadastrar: ')
    numero = input('Número do quarto a cadastrar: ')
    preco = input('Número da reserva do quarto a cadastrar: ')
    id_hotel = input('Chave do quarto a cadastrar: ')
    descricao = input('ID do hotel que o quarto pertence: ')

    sql = '''
        INSERT INTO quartos (andar, numero_quarto, preco, id_hotel, descricao)
        VALUES (?, ?, ?, ?, ?)
    '''
    db.execute(sql, (andar, numero, preco, id_hotel, descricao))
    db.commit()
    db.close()

    # with open('registros/quartos.txt', 'a') as arquivo:
    #     arquivo.write(f'{andar}, {numero}, {numero_reserva}, {chave_quarto}\n')


def ver_quarto():
    db = Database()
    db.connect()

    acao = int(input('Ver todos os quartos (1), ver um quarto (2): '))

    if acao == 1:
        resultado = db.execute("SELECT * FROM quartos").fetchall()
        for quarto in resultado:
            print(dict(quarto))
    elif acao == 2:
        numero_quarto = input('Número do quarto cadastrado: ')
        resultado = db.execute("SELECT * FROM quartos WHERE numero = ?", (numero_quarto,)).fetchone()
        print(dict(resultado) if resultado else "Quarto não encontrado.")

    db.close()


def atualizar_quarto():
    db = Database()
    db.connect()

    id_quarto = int(input('ID do quarto para atualização: '))
    andar = input('Novo andar: ')
    numero = input('Novo número: ')
    numero_reserva = input('Novo número de reserva: ')
    chave_quarto = input('Nova chave: ')

    sql = '''
        UPDATE quartos
        SET andar = ?, numero = ?, numero_reserva = ?, chave_quarto = ?
        WHERE id_quarto = ?
    '''
    db.execute(sql, (andar, numero, numero_reserva, chave_quarto, id_quarto))
    db.commit()
    db.close()


def deletar_quarto():
    db = Database()
    db.connect()

    id_quarto = int(input('ID do quarto a deletar: '))
    confirm = input(f'Deseja realmente deletar o quarto ID={id_quarto}? (s/n): ').lower()

    if confirm in ['s', 'sim']:
        db.execute('DELETE FROM quartos WHERE id_quarto = ?', (id_quarto,))
        db.commit()

    db.close()


def main():
    op = int(input('Cadastrar (1), Ver (2), Atualizar (3), Deletar (4): '))
    if op == 1:
        cadastrar_quarto()
    elif op == 2:
        ver_quarto()
    elif op == 3:
        atualizar_quarto()
    elif op == 4:
        deletar_quarto()
    else:
        print('Opção inválida.')

if __name__ == "__main__":
    main()
