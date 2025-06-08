from connect import Database

class UsuarioModel:
    @staticmethod
    def buscar_por_email_senha(email, senha):
        db = Database()
        db.connect()
        sql = "SELECT * FROM usuarios WHERE email=? AND senha=?"
        db.execute(sql, (email, senha))
        usuario = db.fetchone()
        db.close()
        return usuario

    @staticmethod
    def inserir(nome, cpf, email, senha, imagem):
        db = Database()
        db.connect()
        sql = "INSERT INTO usuarios (nome, cpf, email, senha, imagem) VALUES (?, ?, ?, ?, ?)"
        db.execute(sql, (nome, cpf, email, senha, imagem))
        db.commit()
        db.close()
