from models.connect import Database

class QuartoModel:
    def __init__(self, id_quarto=None, andar=None, numero=None, preco=None, imagem=None, id_hotel=None, id_usuario=None):
        self.id_quarto = id_quarto
        self.andar = andar
        self.numero = numero
        self.preco = preco
        self.imagem = imagem
        self.id_hotel = id_hotel
        self.id_usuario = id_usuario

    def buscar_por_quarto(self):
        db = Database()
        db.connect()
        sql = "SELECT * FROM quartos WHERE id_quarto=?"
        db.execute(sql, (self.id_quarto,))
        quarto = db.fetchone()
        db.close()
        return quarto

    def buscar_todos_quartos(self):
        db = Database()
        db.connect()
        sql = "SELECT * FROM quartos"
        db.execute(sql)
        quartos = db.fetchall()
        db.close()
        return quartos

    def buscar_todos_quartos_do_hotel(self):
        db = Database()
        db.connect()
        sql = "SELECT * FROM quartos WHERE id_hotel=?"
        db.execute(sql, (self.id_hotel,))
        quartos = db.fetchall()
        db.close()
        return quartos

    def inserir(self):
        db = Database()
        db.connect()
        sql = "INSERT INTO quartos (andar, numero_quarto, preco, imagem, id_hotel) VALUES (?, ?, ?, ?, ?)"
        db.execute(sql, (self.andar, self.numero, self.preco, self.imagem, self.id_hotel))
        db.commit()
        db.close()

    def atualizar(self):
        db = Database()
        db.connect()
        sql = "UPDATE quartos SET andar=?, numero_quarto=?, preco=?, imagem=?, id_hotel=? WHERE id_quarto=?"
        db.execute(sql, (self.andar, self.numero, self.preco, self.imagem, self.id_hotel, self.id_quarto))
        db.commit()
        db.close()
