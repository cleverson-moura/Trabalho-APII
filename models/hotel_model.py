from models.connect import Database
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash

class HotelModel:
    def __init__(self, id_hotel=None, nome=None, cidade=None, bairro=None,rua=None,numero=None,cnpj=None,email=None,senha=None,foto=None,chave_pix=None):
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
        self.chave_pix = chave_pix

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
        sql = "SELECT id_usuario FROM usuarios WHERE email=?"
        db.execute(sql,(self.email,))
        existe1 = db.fetchone()
        sql = "SELECT id_hotel FROM hoteis WHERE email=?"
        db.execute(sql,(self.email,))
        existe2 = db.fetchone()
        if existe1 or existe2:
            db.close()
            return True
        else:
            senha_hash = generate_password_hash(self.senha)
            sql = "INSERT INTO hoteis  (nome, cidade, bairro, rua, numero, cnpj, email, senha, foto, chave_pix) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            db.execute(sql, (self.nome, self.cidade, self.bairro, self.rua, self.numero, self.cnpj, self.email, senha_hash, self.foto, self.chave_pix))
            db.commit()
            db.close()
            return False

    def buscar_por_email_senha(self):
        db = Database()
        db.connect()
        sql = "SELECT * FROM hoteis WHERE email=?"
        db.execute(sql, (self.email,))
        hotel = db.fetchone()
        db.close()

        if hotel and check_password_hash(hotel['senha'], self.senha):
            return hotel
        else:
            return None
        
    def atualizar(self):
        db = Database()
        db.connect()
        if self.senha:
            senha_hash = generate_password_hash(self.senha)
            sql = """UPDATE hoteis SET chave_pix=?, nome=?, senha=?, foto=? WHERE id_hotel=?"""
            db.execute(sql, (self.chave_pix, self.nome, senha_hash, self.foto, self.id_hotel))
        else:
            sql = """UPDATE hoteis SET chave_pix=?, nome=?, foto=? WHERE id_hotel=?"""
            db.execute(sql, (self.chave_pix, self.nome, self.foto, self.id_hotel))
        db.commit()
        db.close()