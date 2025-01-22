from flask import Flask
import psycopg2
import logging

app = Flask(__name__)


def get_postgres_connection():
    return psycopg2.connect(
        dbname="base01",
        user="postgres",
        password="9238d680d2cc8a5f600df7262fe6a8f7",
        host="sql.octopustax.com.br",  # Ou endereço do servidor PostgreSQL
        port="5432"        # Porta padrão do PostgreSQL
    )

# Registrar assinantes no banco de dados
def register_subscribers(json_data):
    try:
        conn = get_postgres_connection()
        with conn.cursor() as c:
            for subscriber in json_data:
                email = subscriber["email"]
                keywords = subscriber["keywords"]
                
                # Verificar se o email já está registrado
                c.execute('SELECT 1 FROM ead.subscribers WHERE email = %s', (email,))
                if c.fetchone():
                    logging.warning(f"E-mail já registrado: {email}")
                    continue  # Pular para o próximo assinante
                
                # Inserir novo registro
                c.execute('''
                    INSERT INTO ead.subscribers (email, keywords) 
                    VALUES (%s, %s)
                ''', (email, keywords))
            
            conn.commit()
            c.close()
            conn.close()
        
        logging.info(f"Registros adicionados com sucesso (exceto duplicados): {json_data}")
        return {"message": "Registros adicionados com sucesso, exceto duplicados!"}, 200
    
    except psycopg2.Error as e:
        logging.error(f"Erro ao registrar assinantes: {str(e)}")
        return {"error": str(e)}, 500


def get_email_and_keywords():
    try:
        conn = get_postgres_connection()
        c = conn.cursor()
        
        c.execute('SELECT email, keywords FROM ead.subscribers')
        rows = c.fetchall()
        
        result = []
        for item in rows:
            result.append({"email": item[0], "keywords": item[1]})
        
        c.close()
        conn.close()
        
        logging.info("email e palavras-chave recuperados com sucesso.")
        return result
    except psycopg2.Error as e:
        logging.error(f"Erro ao acessar o banco de dados: {str(e)}")
        return []


# Função para excluir email e palavra chave
def delete_subscriber(email):
    try:
        conn = get_postgres_connection()
        c = conn.cursor()
        
        c.execute('DELETE FROM subscribers WHERE email = %s', (email,))
        conn.commit()
        c.close()
        conn.close()
        
        if c.rowcount > 0:
            logging.info(f"Registro deletado com sucesso: {email}")
            return {"message": "Registro apagado com sucesso!"}, 200
        else:
            logging.warning(f"Não foi encontrado nenhum registro com o e-mail: {email}")
            return {"error": "Nenhum registro encontrado com esse e-mail."}, 404
    except psycopg2.Error as e:
        logging.error(f"Erro ao deletar registro: {str(e)}")
        return {"error": str(e)}, 500


# Função para alterar os registros
def update_subscriber(email, new_keywords):
    try:
        conn = get_postgres_connection()
        c = conn.cursor()
        
        new_keywords_str = ','.join(new_keywords)
        
        c.execute('''
            UPDATE ead.subscribers
            SET keywords = %s
            WHERE email = %s
        ''', (new_keywords_str, email))
        
        conn.commit()
        c.close()
        conn.close()
        
        if c.rowcount > 0:
            logging.info(f"Registro atualizado com sucesso para o e-mail: {email}")
            return {"message": "Registro atualizado com sucesso!"}, 200
        else:
            logging.warning(f"Não foi encontrado nenhum registro com o e-mail: {email}")
            return {"error": "Nenhum registro encontrado com esse e-mail."}, 404
    except psycopg2.Error as e:
        logging.error(f"Erro ao atualizar registro: {str(e)}")
        return {"error": str(e)}, 500