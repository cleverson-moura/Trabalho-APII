import sqlite3

class AvaliacaoHotelModel:
    def __init__(self,id_hotel=None, id_usuario=None,estrelas=None,comentario=None):
        self.id_hotel = id_hotel
        self.id_usuario = id_usuario
        self.estrelas = estrelas
        self.comentario = comentario
        self.con = sqlite3.connect("database/banco/SITE.db")
        self.cursor = self.con.cursor()

    def pode_avaliar_hotel(self, id_usuario, id_hotel):
        query = """
        SELECT 1
        FROM reservas r
        JOIN quartos q ON r.id_quarto = q.id_quarto
        WHERE r.id_usuario = ?
          AND q.id_hotel = ?
          AND r.data_checkout < DATE('now')
        LIMIT 1
        """
        self.cursor.execute(query, (id_usuario, id_hotel))
        return self.cursor.fetchone() is not None

    def inserir_avaliacao(self, id_usuario, id_hotel, estrelas, comentario):
        try:
            self.cursor.execute(
                '''INSERT INTO avaliacoes_hoteis(id_usuario, id_hotel, estrelas, comentario)
                   VALUES(?,?,?,?)''',
                (id_usuario, id_hotel, estrelas, comentario)
            )
            self.con.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def buscar_avaliacoes_hotel(self):
        self.cursor.execute(
            '''SELECT u.nome, a.estrelas, a.comentario, a.data_avaliacao
               FROM avaliacoes_hoteis a
               JOIN usuarios u ON a.id_usuario = u.id_usuario
               WHERE a.id_hotel = ?
               ORDER BY a.data_avaliacao DESC''',
            (self.id_hotel,)
        )
        return self.cursor.fetchall()

    def calcular_media_estrelas(self):
        self.cursor.execute(
            '''SELECT AVG(estrelas), COUNT(*) 
               FROM avaliacoes_hoteis 
               WHERE id_hotel = ?''',
            (self.id_hotel,)
        )
        media, total = self.cursor.fetchone()
        if media:
            media = round(media, 1)
            media = str(media).replace(".", ",")  # troca ponto por vírgula
        else:
            media = "0"
        return media
        
    def fechar(self):
        self.con.close()