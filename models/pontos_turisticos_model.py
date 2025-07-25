from models.connect import Database

class PontoTuristicoModel:
    def __init__(self, id=None, nome=None, descricao=None, imagem=None, cidade=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.imagem = imagem
        self.cidade = cidade

    def inserir(self):
        db = Database()
        db.connect()
        sql = """
            INSERT INTO pontos_turisticos (nome, info_ponto_turistico, cidade)
            VALUES (?, ?, ?)
        """
        db.execute(sql, (self.nome, self.descricao, self.cidade))
        db.commit()
        db.close()

    def buscar_todos(self):
        db = Database()
        db.connect()
        sql = "SELECT * FROM pontos_turisticos"
        db.execute(sql)
        pontos = db.fetchall()
        db.close()
        return pontos

    def buscar_por_id(self):
        db = Database()
        db.connect()
        sql = "SELECT * FROM pontos_turisticos WHERE id = ?"
        db.execute(sql, (self.id,))
        ponto = db.fetchone()
        db.close()
        return ponto