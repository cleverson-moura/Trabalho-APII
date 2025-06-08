from models.connect import Database

class QuartoModel:
    def __init__(self,id_quarto=None, andar=None, numero=None, preco=None, imagem=None, mes_disponivel=None, id_hotel=None, id_usuario=None):
        self.id_quarto = id_quarto
        self.andar = andar
        self.numero = numero
        self.preco = preco
        self.imagem = imagem
        self.mes_disponivel = mes_disponivel
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