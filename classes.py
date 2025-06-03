import sqlite3

con = sqlite3.connect("SITE.db")                          
cursor = con.cursor()

class Usuarios:
    def __init__(self,id_usuario,nome,email,senha,cpf,imagem):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cpf = cpf
        self.imagem = imagem

id_usuario = int(input("Id_usuário: "))
cursor.execute('SELECT * FROM usuarios WHERE id = ?', (id_usuario, ))
tupla = cursor.fetchone()
if tupla:
    usuario = Usuarios(*tupla)
    print(usuario.nome, usuario.email)
    print(vars(usuario))

else:
    print("Usuário não encontrado.")