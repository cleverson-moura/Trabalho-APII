from models.connect import Database

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
        sql = "SELECT * FROM usuarios WHERE email=? AND senha=?"
        db.execute(sql, (self.email, self.senha))
        usuario = db.fetchone()
        db.close()
        return usuario

    def inserir(self):
        db = Database()
        db.connect()
        sql = "INSERT INTO usuarios (nome, cpf, email, senha, imagem) VALUES (?, ?, ?, ?, ?)"
        db.execute(sql, (self.nome, self.cpf, self.email, self.senha, self.imagem))
        db.commit()
        db.close()

    def atualizar(self):
        db = Database()
        db.connect()
        sql = "UPDATE usuarios SET nome=?, cpf=?, email=?, senha=?, imagem=? WHERE id_usuario=?"
        db.execute(sql, (self.nome, self.cpf, self.email, self.senha, self.imagem, self.id_usuario))
        db.commit()
        db.close()
