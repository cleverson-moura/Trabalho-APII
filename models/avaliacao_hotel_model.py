import sqlite3

class AvaliacaoHotelModel:
    @staticmethod
    def inserir_avaliacao(id_usuario, id_hotel, estrelas, comentario):
        try:
            con = sqlite3.connect("database/banco/SITE.db")
            cursor = con.cursor()
            cursor.execute('''INSERT INTO avaliacoes_hoteis(id_usuario, id_hotel, estrelas, comentario)
                           VALUES(?,?,?,?)''', (id_usuario, id_hotel, estrelas, comentario))
            con.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            con.close()

    @staticmethod
    def buscar_avaliacoes_hotel(id_hotel):
        con = sqlite3.connect("database/banco/SITE.db")
        cursor = con.cursor()
        cursor.execute('''SELECT u.nome, a.estrelas, a.comentario, a.data_avaliacao
                       FROM avaliacoes_hoteis a
                       JOIN usuarios u ON a.id_usuario = u.id_usuario
                       WHERE a.id_hotel = ?
                       ORDER BY a.data_avaliacao DESC
                       ''', (id_hotel,))
        avaliacoes = cursor.fetchall()
        con.close()
        return avaliacoes
    

    @staticmethod
    def calcular_media_estrelas(id_hotel):
        con = sqlite3.connect("database/banco/SITE.db")
        cursor = con.cursor()
        cursor.execute('''SELECT AVG(estrelas), COUNT(*) FROM avaliacoes_hoteis 
                        WHERE id_hotel = ?
                        ''', (id_hotel,))
        media, total = cursor.fetchone()
        con.close()
        return (round(media, 1) if media else 0, total)