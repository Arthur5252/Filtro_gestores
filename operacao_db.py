from flask import Flask
import sqlite3
import logging

app = Flask(__name__)

# Log configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('app.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Inicializar banco de dados
def init_db():
    try:
        conn = sqlite3.connect('newsletter.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                keywords TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        logger.info("Banco de dados inicializado com sucesso.")
    
    except sqlite3.Error as e:
        logger.error(f"Erro ao inicializar o banco de dados: {str(e)}")

# Registrar assinantes no banco de dados
def register_subscribers(json_data):
    try:
        conn = sqlite3.connect('newsletter.db')
        c = conn.cursor()
        
        for subscriber in json_data["emails"]:
            email = subscriber["email"]
            keywords = ','.join(subscriber["palavra_chave"])  # Convertendo lista para string
            
            c.execute('''
                INSERT INTO subscribers (email, keywords) 
                VALUES (?, ?)
            ''', (email, keywords))
        
        conn.commit()
        conn.close()
        logger.info(f"Registros adicionados com sucesso: {json_data['emails']}")
        return {"message": "Registros adicionados com sucesso!"}, 200
    
    except sqlite3.Error as e:
        logger.error(f"Erro ao registrar assinantes: {str(e)}")
        return {"error": str(e)}, 500

def get_emails_and_keywords():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('newsletter.db')
        c = conn.cursor()

        # Consultar todos os emails e palavras-chave
        c.execute('SELECT email, keywords FROM subscribers')
        rows = c.fetchall()

        # Formatar os dados em um dicionário
        result = {}
        for email, keywords in rows:
            result[email] = keywords.split(',')  # Transformar a string em lista de palavras-chave
        
        # Fechar a conexão
        conn.close()

        logger.info("Emails e palavras-chave recuperados com sucesso.")
        return result

    except sqlite3.Error as e:
        logger.error(f"Erro ao acessar o banco de dados: {e}")
        return {}

# Função para excluir email e palavra chave
def delete_subscriber(email):
    try:
        conn = sqlite3.connect('newsletter.db')
        c = conn.cursor()
        
        # Deletando o registro com o e-mail fornecido
        c.execute('''
            DELETE FROM subscribers
            WHERE email = ?
        ''', (email,))
        
        conn.commit()
        conn.close()

        # Verificando se algum registro foi apagado
        if c.rowcount > 0:
            logger.info(f"Registro deletado com sucesso: {email}")
            return {"message": "Registro apagado com sucesso!"}, 200
        else:
            logger.warning(f"Não foi encontrado nenhum registro com o e-mail: {email}")
            return {"error": "Nenhum registro encontrado com esse e-mail."}, 404

    except sqlite3.Error as e:
        logger.error(f"Erro ao deletar registro: {str(e)}")
        return {"error": str(e)}, 500

# Função para alterar os registros
def update_subscriber(email, new_keywords):
    try:
        conn = sqlite3.connect('newsletter.db')
        c = conn.cursor()
        
        # Convertendo a lista de novas palavras-chave em string para armazenar no banco
        new_keywords_str = ','.join(new_keywords)
        
        # Atualizando as palavras-chave para o assinante com o e-mail fornecido
        c.execute('''
            UPDATE subscribers
            SET keywords = ?
            WHERE email = ?
        ''', (new_keywords_str, email))
        
        conn.commit()
        conn.close()

        # Verificando se algum registro foi atualizado
        if c.rowcount > 0:
            logger.info(f"Registro atualizado com sucesso para o e-mail: {email}")
            return {"message": "Registro atualizado com sucesso!"}, 200
        else:
            logger.warning(f"Não foi encontrado nenhum registro com o e-mail: {email}")
            return {"error": "Nenhum registro encontrado com esse e-mail."}, 404

    except sqlite3.Error as e:
        logger.error(f"Erro ao atualizar registro: {str(e)}")
        return {"error": str(e)}, 500
