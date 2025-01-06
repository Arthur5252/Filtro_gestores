from flask import Flask, render_template, request
from buscar_palavra_chave import filtra_noticias
from salvar_pdf import gera_pdf
from enviar_email import envia_email
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processa', methods=['POST'])
def processa():
    # Captura dados do formulário
    destinatario_email = request.form['destinatario_email'].split(',')
    palavras_chave = request.form['palavras_chave'].split(',')
    
    # Converte data para o formato %Y/%m/%d
    data_inicio = datetime.strptime(request.form['data_inicio'], '%Y-%m-%d').strftime('%Y/%m/%d')
    data_fim = datetime.strptime(request.form['data_fim'], '%Y-%m-%d').strftime('%Y/%m/%d')

    # Processa as informações
    noticias = filtra_noticias(palavras_chave, data_inicio, data_fim)
    gera_pdf(noticias)
    local_pdf = 'relatorio_noticias.pdf'

    # Envia email para cada destinatário
    for destinatario in destinatario_email:
        envia_email(destinatario.strip(), local_pdf)

    return "Notícias filtradas, PDF gerado e e-mails enviados com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)
