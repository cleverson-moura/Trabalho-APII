import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from connect import Database

db = Database()

db.connect()

def criar_reserva(id_usuario, id_quarto, tempo_estadia):
    sql = '''INSERT INTO reservas (id_usuario, id_quarto, tempo_estadia)
             VALUES (?, ?, ?, ?)'''
    db.execute(sql, (id_usuario, id_quarto, tempo_estadia))
    db.commit()

    arquivo_quartos = open('registros/reservas.txt', 'a')
    arquivo_quartos.write(f'{id_usuario}, {id_quarto}, {tempo_estadia}\n')
    arquivo_quartos.close()

usuario_id = int(input('Digite o ID do usuário: '))
quarto_id = int(input('Digite o ID do quarto: '))
tempo_estadia = int(input('Digite o tempo de estadia (em dias): '))

criar_reserva(usuario_id, quarto_id, tempo_estadia)
db.close()