from models.connect import Database

class AdministradorModel:
    def __init__(self, id_administrador=None, nome=None, cpf=None, email=None, senha=None, imagem=None, id_hotel=None):
        self.id_administrador = id_administrador
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.imagem = imagem
        self.id_hotel = id_hotel

    def buscar_por_id(self):
        db = Database()
        db.connect()
        sql = "SELECT * FROM administradores WHERE id_adm=?"
        db.execute(sql, (self.id_administrador,))
        adm = db.fetchone()
        db.close()
        return adm

    def buscar_por_email_senha(self):
        db = Database()
        db.connect()
        sql = "SELECT * FROM administradores WHERE email=? AND senha=?"
        db.execute(sql, (self.email, self.senha))
        adm = db.fetchone()
        db.close()
        return adm

    def inserir(self):
        db = Database()
        db.connect()
        sql = "INSERT INTO administradores (nome, cpf, email, senha, imagem) VALUES (?, ?, ?, ?, ?)"
        db.execute(sql, (self.nome, self.cpf, self.email, self.senha, self.imagem))
        db.commit()
        db.close()

    def atualizar(self):
        db = Database()
        db.connect()
        sql = "UPDATE administradores SET nome=?, senha=?, imagem=? WHERE id_adm=?"
        db.execute(sql, (self.nome, self.senha, self.imagem, self.id_administrador))
        db.commit()
        db.close()
