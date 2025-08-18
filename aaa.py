import sqlite3

con = sqlite3.connect('database/banco/SITE.db')
cursor = con.cursor()

cursor.execute('DELETE FROM avaliacoes_hoteis WHERE id_avaliacao=?',(2,))

con.commit()
con.close()