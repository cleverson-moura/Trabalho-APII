import sqlite3
con = sqlite3.connect("database/banco/SITE.db")
cursor = con.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

criar_tabela_usuarios = '''CREATE TABLE IF NOT EXISTS
usuarios 
(
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT,
    email TEXT,
    senha TEXT,
    cpf INTEGER, 
    imagem TEXT
)'''
cursor.execute(criar_tabela_usuarios)

criar_tabela_pontos_turisticos = '''CREATE TABLE IF NOT EXISTS 
pontos_turisticos 
(
    id_ponto_turistico INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    cidade TEXT,
    bairro TEXT,
    rua TEXT,
    numero TEXT,
    info_ponto_turistico TEXT
)'''
cursor.execute(criar_tabela_pontos_turisticos)

criar_tabela_hoteis = '''CREATE TABLE IF NOT EXISTS
hoteis
(
    id_hotel INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    cidade TEXT,
    bairro TEXT,
    rua TEXT,
    numero INTEGER,
    cnpj INTEGER,
    email TEXT,
    senha TEXT,
    foto TEXT
)'''
cursor.execute(criar_tabela_hoteis)

criar_tabela_quartos = '''CREATE TABLE IF NOT EXISTS
quartos 
(
    id_quarto INTEGER PRIMARY KEY AUTOINCREMENT,
    andar TEXT,
    numero_quarto TEXT,
    preco TEXT,
    imagem TEXT,
    mes_disponivel TEXT,
    id_hotel INTEGER,   
    id_usuario INTEGER,
    FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_hotel) REFERENCES hoteis(id_hotel)
)'''
cursor.execute(criar_tabela_quartos)

criar_tabela_reservas = '''CREATE TABLE IF NOT EXISTS
reservas 
(
    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER, 
    id_quarto INTEGER,
    tempo_estadia INTEGER,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_quarto) REFERENCES quartos(id_quarto)
)'''
cursor.execute(criar_tabela_reservas)
    # O tempo de estadia é dado em dias.

criar_tabela_IMG_PT = '''CREATE TABLE IF NOT EXISTS
IMG_PT 
(
    id_img_PT INTEGER PRIMARY KEY AUTOINCREMENT,
    imagem_PT TEXT,
    info TEXT,
    id_ponto_turistico INTEGER,
    FOREIGN KEY (id_ponto_turistico) REFERENCES pontos_turisticos(id_ponto_turistico)
)'''
cursor.execute(criar_tabela_IMG_PT)

criar_tabela_IMG_HOTEIS = ''' CREATE TABLE IF NOT EXISTS
IMG_HOTEIS 
(
    id_img_hotel INTEGER PRIMARY KEY AUTOINCREMENT,
    imagem_hotel TEXT,
    info TEXT,
    id_ponto_turistico INTEGER,
    FOREIGN KEY (id_ponto_turistico) REFERENCES pontos_turisticos(id_ponto_turistico)
)'''
cursor.execute(criar_tabela_IMG_HOTEIS)

con.commit()
con.close()