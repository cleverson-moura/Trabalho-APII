from connect import Database

class AdministradorModel:
    @staticmethod
    def buscar_por_email_senha(email, senha):
        db = Database()
        db.connect()
        sql = "SELECT * FROM administradores WHERE email=? AND senha=?"
        db.execute(sql, (email, senha))
        adm = db.fetchone()
        db.close()
        return adm

    @staticmethod
    def inserir(nome, cpf, email, senha, imagem):
        db = Database()
        db.connect()
        sql = "INSERT INTO administradores (nome, cpf, email, senha, imagem) VALUES (?, ?, ?, ?, ?)"
        db.execute(sql, (nome, cpf, email, senha, imagem))
        db.commit()
        db.close()
