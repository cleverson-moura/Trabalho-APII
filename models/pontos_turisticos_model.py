from models.connect import Database

class PontoTuristicoModel:
    def __init__(self, id=None, nome=None, descricao=None, cidade=None, bairro=None, rua=None):
        self.id = id
        self.nome = nome
        # Mapeia 'descricao' do form para 'info_ponto_turistico' no banco
        self.info_ponto_turistico = descricao 
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua

    def inserir(self):
        """
        Insere os dados básicos do ponto turístico e retorna o ID do novo registro.
        """
        db = Database()
        db.connect()
        sql = """
            INSERT INTO pontos_turisticos (nome, info_ponto_turistico, cidade, bairro, rua)
            VALUES (?, ?, ?, ?, ?)
        """
        db.execute(sql, (self.nome, self.info_ponto_turistico, self.cidade, self.bairro, self.rua))
        novo_id = db.cursor.lastrowid  # Pega o ID do ponto que acabamos de criar
        db.commit()
        db.close()
        return novo_id

    def inserir_imagens(self, id_ponto, imagens_paths):
        """
        Insere os caminhos das imagens na tabela IMG_PT.
        'imagens_paths' é um dicionário como {'imagem_capa': 'path/1.jpg', 'imagem_extra_1': 'path/2.jpg'}
        """
        if not imagens_paths:
            return

        db = Database()
        db.connect()

        colunas = ['id_ponto_turistico'] + list(imagens_paths.keys())
        placeholders = ['?'] * len(colunas)
        valores = [id_ponto] + list(imagens_paths.values())

        sql = f"""
            INSERT INTO IMG_PT ({', '.join(colunas)})
            VALUES ({', '.join(placeholders)})
        """
        
        db.execute(sql, tuple(valores))
        db.commit()
        db.close()

    def buscar_todos(self):
        """
        Busca todos os pontos turísticos juntando com a imagem de capa da tabela IMG_PT.
        """
        db = Database()
        db.connect()
        # LEFT JOIN garante que pontos sem imagem ainda apareçam
        sql = """
            SELECT pt.*, img.imagem_capa 
            FROM pontos_turisticos pt
            LEFT JOIN IMG_PT img ON pt.id_ponto_turistico = img.id_ponto_turistico
        """
        db.execute(sql)
        pontos = db.fetchall()
        db.close()
        return pontos

    def buscar_por_id(self, id_ponto):
        """
        Busca um ponto turístico específico e todas as suas imagens.
        """
        db = Database()
        db.connect()
        sql = """
            SELECT pt.*, img.*
            FROM pontos_turisticos pt
            LEFT JOIN IMG_PT img ON pt.id_ponto_turistico = img.id_ponto_turistico
            WHERE pt.id_ponto_turistico = ?
        """
        db.execute(sql, (id_ponto,))
        ponto = db.fetchone()
        db.close()
        return ponto
