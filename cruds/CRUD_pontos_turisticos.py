import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.connect import Database  # ajusta o caminho conforme sua estrutura

def cadastrar_ponto_turistico():
    db = Database()
    db.connect()

    nome = input('Nome do ponto turístico a cadastrar: ')
    cidade = input('Cidade do ponto turístico a cadastrar: ')
    bairro = input('Bairro do ponto turístico a cadastrar: ')
    rua = input('Rua do ponto turístico a cadastrar: ')
    numero = input('Número do ponto turístico a cadastrar: ')
    info = input('Informações extras: ')

    sql = '''
        INSERT INTO pontos_turisticos (nome, cidade, bairro, rua, numero, info_ponto_turistico)
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    db.execute(sql, (nome, cidade, bairro, rua, numero, info))
    db.commit()
    db.close()

    with open('registros/pontos_turisticos.txt', 'a') as arquivo:
        arquivo.write(f'{nome}, {cidade}, {bairro}, {rua}, {numero}, {info}\n')


def ver_ponto_turistico():
    db = Database()
    db.connect()

    acao = int(input('Ver todos os pontos turísticos (1), ver um ponto turístico (2): '))
    
    if acao == 1:
        resultado = db.execute('SELECT * FROM pontos_turisticos').fetchall()
        for ponto in resultado:
            print(dict(ponto))
    elif acao == 2:
        nome = input('Nome do ponto turístico: ')
        resultado = db.execute('SELECT * FROM pontos_turisticos WHERE nome = ?', (nome,)).fetchone()
        print(dict(resultado) if resultado else "Ponto turístico não encontrado.")
    
    db.close()


def atualizar_ponto_turistico():
    db = Database()
    db.connect()

    id_ponto = int(input('ID do ponto turístico para atualização: '))
    nome = input('Novo nome: ')
    cidade = input('Nova cidade: ')
    bairro = input('Novo bairro: ')
    rua = input('Nova rua: ')
    numero = input('Novo número: ')
    info = input('Novas informações extras: ')

    sql = '''
        UPDATE pontos_turisticos
        SET nome = ?, cidade = ?, bairro = ?, rua = ?, numero = ?, info_ponto_turistico = ?
        WHERE id = ?
    '''
    db.execute(sql, (nome, cidade, bairro, rua, numero, info, id_ponto))
    db.commit()
    db.close()


def deletar_ponto_turistico():
    db = Database()
    db.connect()

    id_ponto = int(input('ID do ponto turístico a deletar: '))
    confirm = input(f'Deseja realmente deletar o ponto turístico ID={id_ponto}? (s/n): ').lower()

    if confirm in ['s', 'sim']:
        db.execute('DELETE FROM pontos_turisticos WHERE id = ?', (id_ponto,))
        db.commit()

    db.close()


def main():
    acao = int(input('Cadastrar (1), Ver (2), Atualizar (3), Deletar (4): '))
    if acao == 1:
        cadastrar_ponto_turistico()
    elif acao == 2:
        ver_ponto_turistico()
    elif acao == 3:
        atualizar_ponto_turistico()
    elif acao == 4:
        deletar_ponto_turistico()
    else:
        print('Opção inválida.')

if __name__ == "__main__":
    main()
