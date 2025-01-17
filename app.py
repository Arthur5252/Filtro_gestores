from flask import Flask, request, jsonify, render_template
from buscar_palavra_chave import *
from datetime import datetime
from coleta_noticias import *
from enviar_email import *
from operacao_db import *
from salvar_pdf import *
import logging
import os

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", mode="w"),  # Salvar logs em arquivo
    ]
)

@app.route('/')
def index():
    app.logger.info("Acessando a página inicial.")
    return render_template('index.html')

# Rota de teste
@app.route('/frutas', methods=['GET'])
def get_frutas():
    frutas = ['Maçã', 'Banana', 'Laranja', 'Manga', 'Uva']
    app.logger.info("Rota de frutas acessada.")
    return jsonify(frutas)

# Rota para Enviar os emails
@app.route('/process', methods=['GET'])
def processar():
    app.logger.info("Iniciando o processamento de envio de emails.")
    local_pdf = 'relatorio_noticias.pdf'
    emails_palavras = get_emails_and_keywords()
    data_atual = datetime.now().strftime('%Y-%m-%d')
    
    for email, palavra_chave in emails_palavras.items():
        try:
            app.logger.info(f"Filtrando notícias para o email: {email} com palavras-chave: {palavra_chave}")
            noticias_filtradas = filtra_noticias(palavra_chave, data_atual)
            gera_pdf(noticias=noticias_filtradas)
            envia_email(email, local_pdf)
            os.remove(local_pdf)
            app.logger.info(f"Email enviado para {email} com o PDF gerado.")
        except Exception as e:
            app.logger.error(f"Erro ao processar para o email {email}: {str(e)}")
    
    return 'Email enviado'

# Adicionar endpoint para remover usuário do banco
@app.route('/delete', methods=['POST'])
def deletar():
    try:
        del_email = request.get_json()['emails']
        app.logger.info(f"Solicitação de exclusão de usuário com o e-mail: {del_email}")
        delete_subscriber(del_email)
        app.logger.info(f"Registro com o e-mail {del_email} deletado com sucesso.")
        return 'Registro deletado'
    except Exception as e:
        app.logger.error(f"Erro ao tentar excluir o registro: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Adicionar endpoint para alterar registro do banco
@app.route('/update', methods=['POST'])
def alterar():
    try:
        up_email = request.get_json()['email']
        up_keywords = request.get_json()['novas_keywords']
        app.logger.info(f"Solicitação de atualização do registro para o e-mail: {up_email} com novas palavras-chave: {up_keywords}")
        update_subscriber(up_email, up_keywords)
        app.logger.info(f"Registro com o e-mail {up_email} atualizado com as novas palavras-chave.")
        return 'Registro alterado'
    except Exception as e:
        app.logger.error(f"Erro ao tentar alterar o registro: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Rota para receber JSON e registrar no banco
@app.route('/register', methods=['POST'])
def register():
    try:
        json_data = request.get_json()  # Obter o JSON enviado pelo frontend
        if not json_data or "emails" not in json_data:
            app.logger.warning("Dados inválidos recebidos na rota /register.")
            return jsonify({"error": "Dados inválidos"}), 400
        
        app.logger.info("Iniciando o registro de assinantes no banco de dados.")
        response, status_code = register_subscribers(json_data)
        app.logger.info(f"{status_code} - Resposta: {response}")
        return jsonify(response), status_code
    
    except Exception as e:
        app.logger.error(f"Erro ao tentar registrar assinantes: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()  # Garantir que o banco está inicializado
    app.logger.info("Banco de dados inicializado com sucesso.")
    app.run(debug=True)
