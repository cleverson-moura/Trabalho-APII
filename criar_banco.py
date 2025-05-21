import sqlite3
con = sqlite3.connect("banco_de_dados.db")
cursor = con.cursor()
sql = "INSERT INTO teste(id, titulo, descricao) VALUES(2, 'Ota Igreja2', 'Muito massa2')"
cursor.execute(sql,)
con.commit()
con.close()
