from models.connect import Database

class ReservaModel:
    #futuramente adicionar data_entrada e data_saida
    def __init__(self, id_reserva=None, id_usuario=None, id_quarto=None, tempo_estadia=None):
        self.id_reserva = id_reserva
        self.id_usuario = id_usuario
        self.id_quarto = id_quarto
        self.tempo_estadia = tempo_estadia

    def buscar_por_reservas(self):
        db = Database()
        db.connect()
        sql = "SELECT * FROM reservas WHERE id_usuario=?"
        db.execute(sql, (self.id_usuario,))
        reservas = db.fetchall()
        db.close()
        return reservas
    
    def cancelar_reserva(self):
        db = Database()
        db.connect()
        sql = "DELETE FROM reservas WHERE id_reserva=?"
        db.execute(sql, (self.id_reserva,))
        db.commit()
        db.close()

    def fazer_reserva(self):
        db = Database()
        db.connect()
        sql = "INSERT INTO reservas (id_usuario, id_quarto, tempo_estadia) VALUES (?, ?, ?)"
        db.execute(sql, (self.id_usuario, self.id_quarto, self.tempo_estadia))
        db.commit()
        db.close()
