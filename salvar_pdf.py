from buscar_palavra_chave import *
from datetime import datetime
from io import BytesIO
from fpdf import FPDF
import PyPDF2 as pdf
import requests
import logging


from buscar_palavra_chave import *
from datetime import datetime
from fpdf import FPDF
import requests
import logging
import os
from io import BytesIO

# Configuração do log
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('app.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

def gera_pdf(noticias):
    data = datetime.now().strftime('%d/%m/%Y').replace('/', '-')

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)  # Usando a fonte Arial em negrito
            self.cell(0, 10, "Relatório de Notícias", 0, 1, "C")

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)  # Usando a fonte Arial em itálico
            self.cell(0, 10, f'Página {self.page_no()}', align='C')

    try:
        # Criação do PDF
        pdf = PDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Usar a fonte Arial
        pdf.add_font("Arial_TTF", "", r"Arial.ttf", uni=True)
        pdf.set_font("Arial_TTF", size=12)

        # Configura a página de rosto
        pdf.image(r'imagens\logoOctopus.png', x=30, y=80, w=150)
        pdf.cell(0, 50, "", ln=True)
        pdf.image(r'imagens\infos.png', x=5, y=120, w=200)
        pdf.add_page()

        logger.info("Página de rosto criada com sucesso.")
        
        # Lista para armazenar caminhos de imagens baixadas
        imagens_baixadas = []

        # Baixar imagens e salvar localmente
        for noticia in noticias:
            try:
                image_url = noticia['imagem']
                response = requests.get(image_url)
                response.raise_for_status()

                # Salvar a imagem temporariamente em um arquivo
                temp_image_path = f"temp_images/{noticia['titulo'].replace(' ', '_').replace('/','-')}.jpg"
                with open(temp_image_path, 'wb') as f:
                    f.write(response.content)

                imagens_baixadas.append((temp_image_path, noticia))  # Armazena o caminho e a notícia

            except Exception as e:
                logger.error(f"Erro ao baixar a imagem para a notícia '{noticia['titulo']}': {str(e)}")

        # Adiciona notícias ao PDF
        for image_path, noticia in imagens_baixadas:
            try:
                # Título e data
                pdf.cell(0, 10, f'Título: {noticia["titulo"]}', ln=True)
                pdf.cell(0, 10, f'Data: {noticia["data"]}', ln=True)
                pdf.cell(0, 10, "", ln=True)

                # Inserir Imagem
                y_before_image = pdf.get_y()  # Salvar a posição Y atual
                pdf.image(image_path, x=30, y=y_before_image, w=150, h=80)
                pdf.set_y(y_before_image + 70)  # Ajustar altura conforme necessário

                logger.info(f"Imagem inserida para a notícia: {noticia['titulo']}")

            except Exception as e:
                pdf.cell(0, 10, f'Erro ao inserir a imagem: {str(e)}', ln=True)
                logger.error(f"Erro ao inserir a imagem para a notícia '{noticia['titulo']}': {str(e)}")

            # Conteúdo e separação
            pdf.cell(0, 10, "", ln=True)
            pdf.multi_cell(0, 10, f'Conteúdo: {noticia["conteudo"]}')
            pdf.cell(0, 10, "-"*120, ln=True)
            pdf.add_page()

        # Salva o PDF
        pdf.output('relatorio_noticias.pdf')
        logger.info("PDF gerado e salvo com sucesso como 'relatorio_noticias.pdf'.")

    except Exception as e:
        logger.error(f"Erro ao gerar o PDF: {str(e)}")
    finally:
        # Remove imagens temporárias
        for image_path, _ in imagens_baixadas:
            if os.path.exists(image_path):
                os.remove(image_path)
                logger.info(f"Imagem temporária removida: {image_path}")
