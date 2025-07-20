from models.connect import Database
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioModel:
    def __init__(self, id_usuario=None, nome=None, cpf=None, email=None, senha=None, imagem=None):
        self.id_usuario = id_usuario
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.imagem = imagem
    
    def buscar_por_id(self):
        db = Database()
        db.connect()
        sql = "SELECT * FROM usuarios WHERE id_usuario=?"
        db.execute(sql, (self.id_usuario,))
        usuario = db.fetchone()
        db.close()
        return usuario
        
    def buscar_por_email_senha(self):
        db = Database()
        db.connect()
        sql = "SELECT * FROM usuarios WHERE email=?"
        db.execute(sql, (self.email,))
        usuario = db.fetchone()
        db.close()
        if usuario and check_password_hash(usuario['senha'], self.senha):
            return usuario
        else:
            return None

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
            sql = "INSERT INTO usuarios (nome, cpf, email, senha, imagem) VALUES (?, ?, ?, ?, ?)"
            db.execute(sql, (self.nome, self.cpf, self.email, senha_hash, self.imagem))
            db.commit()
            db.close()
            return False

    def atualizar(self):
        db = Database()
        db.connect()
        senha_hash = generate_password_hash(self.senha)
        sql = "UPDATE usuarios SET nome=?, senha=?, imagem=? WHERE id_usuario=?"
        db.execute(sql, (self.nome, senha_hash, self.imagem, self.id_usuario))
        db.commit()
        db.close()
