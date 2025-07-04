from models.connect import Database

class HotelModel:
    def __init__(self, id_hotel=None, nome=None, cidade=None, bairro=None,rua=None,numero=None,cnpj=None,email=None,senha=None,foto=None):
        self.id_hotel = id_hotel
        self.nome = nome
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.numero = numero
        self.cnpj = cnpj
        self.email = email
        self.senha = senha
        self.foto = foto

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
        sql = "INSERT INTO hoteis (nome, cidade, bairro, rua, numero, cnpj, email, senha, foto) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        db.execute(sql, (self.nome, self.cidade, self.bairro, self.rua, self.numero, self.cnpj, self.email, self.senha, self.foto))
        db.commit()
        db.close()

    def buscar_por_email_senha(self):
        db = Database()
        db.connect()
        sql = "SELECT * FROM hoteis WHERE email=? AND senha=?"
        db.execute(sql, (self.email, self.senha))
        hotel = db.fetchone()
        db.close()
        return hotel