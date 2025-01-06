import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from coleta_noticias import *
from buscar_palavra_chave import *

def envia_email(destinatario_email,local_pdf):
    # Configurações do e-mail
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender_email = 'arthur.lima.araujoo@gmail.com'
    password = 'mfvjmfgsxrvjioha'

    # Criação do e-mail
    destinatario_email = 'arthur.lima.araujoo@gmail.com'
    subject = 'Relatório de noticias'

    # Converte a lista de notícias em uma string
    body = 'Segue em anexo os artigos escolhidos pelo seu gestor!'

    # Cria a mensagem do e-mail
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = destinatario_email
    message['Subject'] = subject

    # Anexa o corpo do e-mail
    message.attach(MIMEText(body, 'plain'))

    # Anexa o arquivo PDF
    with open(local_pdf, 'rb') as f:
        pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename=local_pdf)
        message.attach(pdf_attachment)

    # Envio do e-mail
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, destinatario_email, message.as_string())
    except Exception as e:
        print(f'Falha ao enviar e-mail: {e}')