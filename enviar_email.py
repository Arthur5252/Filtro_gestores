from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from buscar_palavra_chave import *
from coleta_noticias import *
import smtplib
import logging

# Log configuration (assumindo que você já tenha configurado o logging no app principal)
logger = logging.getLogger(__name__)

def envia_email(destinatario_email, local_pdf):
    # Configurações do e-mail
    smtp_server = 'smtp.hostinger.com'
    port = 587
    sender_email = 'OctopusTAX <noreply@octopustax.com.br>'
    username= 'noreply@octopustax.com.br'
    password = '#Sdn7and7slv5'

    # Criação do e-mail
    subject = 'Relatório de noticias'
    body = 'Segue em anexo os artigos escolhidos pelo seu gestor!'

    try:
        logger.info(f"Iniciando o processo de envio de e-mail para {destinatario_email}.")
        
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
        logger.info(f"Arquivo PDF {local_pdf} anexado ao e-mail.")

        # Envio do e-mail
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(sender_email, destinatario_email, message.as_string())
            logger.info(f"E-mail enviado com sucesso para {destinatario_email}.")
    
    except smtplib.SMTPException as e:
        logger.error(f"Erro no envio de e-mail: {str(e)}")
    except Exception as e:
        logger.error(f"Erro inesperado ao tentar enviar o e-mail: {str(e)}")
