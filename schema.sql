import sqlite3
con = sqlite3.connect("SITE.db")
cursor = con.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

criar_tabela_usuarios = '''CREATE TABLE IF NOT EXISTS
usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT, 
      nome TEXT,
        email TEXT,
          senha TEXT,
            cpf INTEGER(11), 
              imagem BLOB)'''


criar_tabela_administradores = '''CREATE TABLE
administradores (
    id_adm INTEGER PRIMARY KEY AUTOINCREMENT,
      nome VARCHAR(100),
        cpf INTEGER,
          email VARCHAR(70),
            senha VARCHAR(100),'''


criar_tabela_quartos = '''CREATE TABLE IF NOT EXISTS
quartos (
    id_quarto INTEGER PRIMARY KEY AUTOINCREMENT,
      andar,
        numero,
          numero_reserva,
            chave_quarto,
              id_usuario,
                id_hotel,
                  FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario),
                  FOREIGN KEY (id_hotel) REFERENCES hoteis(id_hotel))'''


criar_tabela_hoteis = '''CREATE TABLE IF NOT EXISTS
hoteis(
  id_hotel INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
      cidade TEXT,
        bairro TEXT,
          rua TEXT,
            numero INTEGER,
              cnpj INTEGER,
                id_adm,
                  FOREIGN KEY (id_adm) REFERENCES administradores(id_adm))'''


criar_tabela_usuarios = '''CREATE TABLE IF NOT EXISTS
reservas (
    id_quarto, 
      id_usuario,
        tempo_estadia INTEGER,
          FOREIGN KEY (id_quarto) REFERENCES quartos(id_quarto),
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)'''
            # O tempo de estadia é dado em dias.

con.commit()
con.close()