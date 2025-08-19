import sqlite3
import os

# --- ATENÇÃO ---
# Certifique-se de que o caminho para o banco de dados está correto.
DB_PATH = os.path.join("database", "banco", "SITE.db")

def executar_migracao():
    """
    Adiciona as novas colunas de imagem na tabela IMG_PT sem apagar dados.
    Este script é seguro para ser executado múltiplas vezes.
    """
    if not os.path.exists(DB_PATH):
        print(f"Erro: O arquivo do banco de dados não foi encontrado em '{DB_PATH}'")
        return

    try:
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()

        print("Conectado ao banco de dados. Verificando a tabela IMG_PT...")

        # Pega as informações das colunas existentes na tabela
        cursor.execute("PRAGMA table_info(IMG_PT)")
        colunas_existentes = [coluna[1] for coluna in cursor.fetchall()]
        
        # 1. Renomeia a coluna antiga 'imagem_PT' para 'imagem_capa' se ela existir
        if 'imagem_PT' in colunas_existentes and 'imagem_capa' not in colunas_existentes:
            print("Renomeando 'imagem_PT' para 'imagem_capa'...")
            cursor.execute("ALTER TABLE IMG_PT RENAME COLUMN imagem_PT TO imagem_capa")
            print("Coluna renomeada com sucesso.")
        
        # 2. Define as novas colunas que queremos adicionar
        novas_colunas = {
            "imagem_extra_1": "TEXT",
            "imagem_extra_2": "TEXT",
            "imagem_extra_3": "TEXT",
            "imagem_extra_4": "TEXT"
        }

        # 3. Adiciona cada nova coluna, APENAS se ela não existir ainda
        for nome_coluna, tipo_coluna in novas_colunas.items():
            if nome_coluna not in colunas_existentes:
                print(f"Adicionando coluna '{nome_coluna}'...")
                cursor.execute(f"ALTER TABLE IMG_PT ADD COLUMN {nome_coluna} {tipo_coluna}")
                print(f"Coluna '{nome_coluna}' adicionada.")
            else:
                print(f"Coluna '{nome_coluna}' já existe. Nenhuma ação necessária.")

        # Salva (commita) as alterações
        con.commit()
        print("\nMigração concluída com sucesso!")

    except sqlite3.Error as e:
        print(f"\nOcorreu um erro durante a migração: {e}")
        if con:
            con.rollback()
    finally:
        # Garante que a conexão seja fechada
        if con:
            con.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    # É uma boa prática fazer um backup antes de migrações
    print("--- INICIANDO MIGRAÇÃO DA TABELA IMG_PT ---")
    print("ATENÇÃO: É recomendado fazer um backup do seu arquivo 'SITE.db' antes de continuar.")
    
    resposta = input("Deseja executar a migração agora? (s/n): ").lower()
    if resposta == 's':
        executar_migracao()
    else:
        print("Operação cancelada.")

