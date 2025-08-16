import sqlite3

class AvaliacaoQuartoModel:
    
    def __init__(self):
        self.con = sqlite3.connect("database/banco/SITE.db")
        self.cursor = self.con.cursor()

    def inserir_avaliacao(id_usuario, id_hotel, id_quarto, estrelas, comentario):
        try:
            con = sqlite3.connect("database/banco/SITE.db")
            cursor = con.cursor()
            cursor.execute('''INSERT INTO avaliacoes_quartos(id_usuario, id_hotel, id_quarto, estrelas, comentario) VALUES(?,?,?,?,?)''', (id_usuario, id_hotel, id_quarto, estrelas, comentario))
            con.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            con.close()

    def buscar_avaliacoes_quarto(id_hotel, id_quarto):
        con = sqlite3.connect("database/banco/SITE.db")
        cursor = con.cursor()
        cursor.execute('''SELECT u.nome, a.estrelas, a.comentario, a.data_avaliacao
                       FROM avaliacoes_quartos a
                       JOIN usuarios u ON a.id_usuario = u.id_usuario
                       WHERE a.id_hotel = ? AND a.id_quarto = ?
                       ORDER BY a.data_avaliacao DESC
                       ''', (id_hotel, id_quarto))
        avaliacoes = cursor.fetchall()
        con.close()
        return avaliacoes

    def calcular_media_estrelas(id_hotel, id_quarto):
        con = sqlite3.connect("database/banco/SITE.db")
        cursor = con.cursor()
        cursor.execute('''SELECT AVG(estrelas), COUNT(*) FROM avaliacoes_quartos 
                        WHERE id_hotel = ? AND id_quarto = ?
                        ''', (id_hotel, id_quarto))
        media, total = cursor.fetchone()
        con.close()
        return (round(media, 1) if media else 0, total)