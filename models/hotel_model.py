from models.connect import Database

class HotelModel:
    def __init__(self, id_hotel=None, nome=None, cidade=None, bairro=None,rua=None,numero=None,cnpj=None,id_ponto=None):
        self.id_hotel = id_hotel
        self.nome = nome
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.numero = numero
        self.cnpj = cnpj
        self.id_ponto = id_ponto

    def buscar_por_hotel(self):
        db = Database()
        db.connect()
        sql = "SELECT * FROM hoteis WHERE id_hotel=?"
        db.execute(sql, (self.id_hotel,))
        hotel = db.fetchone()
        db.close()
        return hotel
    
    def buscar_todos_hoteis(self):
        db = Database()
        db.connect()
        sql = "SELECT * FROM hoteis"
        db.execute(sql)
        hoteis = db.fetchall()
        db.close()
        return hoteis


    def inserir(self):
        db = Database()
        db.connect()
        sql = "INSERT INTO hoteis (nome, cidade, bairro, rua, numero, cnpj, id_ponto_turistico) VALUES (?, ?, ?, ?, ?, ?, ?)"
        db.execute(sql, (self.nome, self.cidade, self.bairro, self.rua, self.numero, self.cnpj, self.id_ponto))
        db.commit()
        db.close()