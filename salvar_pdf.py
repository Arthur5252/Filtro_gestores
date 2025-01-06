from fpdf import FPDF
import PyPDF2 as pdf
from buscar_palavra_chave import *
from io import BytesIO
from datetime import datetime

def gera_pdf(noticias):
    data = datetime.now().strftime('%d/%m/%Y').replace('/','-')
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)  # Usando a fonte Arial em negrito
            self.cell(0, 10, "Relatório de Notícias", 0, 1, "C")

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)  # Usando a fonte Arial em itálico
            self.cell(0, 10, f'Página {self.page_no()}', align='C')

    # Criação do PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Usar a fonte Arial
    pdf.add_font("Arial_TTF", "", r"C:\Windows\Fonts\Arial.ttf")
    pdf.set_font("Arial_TTF", size=12)

    # Configura a pagina de rosto
    y_before_image = pdf.get_y()
    pdf.image(r'imagens\logoOctopus.png', x=30, y=80, w=150 )
    pdf.cell(0, 50, "", ln=True)
    pdf.image(r'imagens\infos.png', x=5, y=120, w=200 )
    pdf.add_page()
    noticias =''
    # Adiciona notícias ao PDF 
    for noticia in noticias:
        # Requisição da imagem
        image_url = noticia['imagem']
        response = requests.get(image_url)
        image = BytesIO(response.content)
        # Titulo e data
        pdf.cell(0, 10, f'Título: {noticia["titulo"]}', ln=True)
        pdf.cell(0, 10, f'Data: {noticia["data"]}', ln=True)
        pdf.cell(0, 10, "", ln=True)

        # Inserir Imagem
        try:
            response = requests.get(noticia['imagem'])
            image = BytesIO(response.content)
            y_before_image = pdf.get_y()  # Salvar a posição Y atual
            pdf.image(image, x=30, y=y_before_image, w=150, h=80)  # Ajustar conforme necessário
            
            # Atualizar a posição Y após a imagem
            pdf.set_y(y_before_image + 70)  # Ajustar altura conforme a dimensão da imagem
        except Exception as e:
            pdf.cell(0, 10, f'Erro ao carregar a imagem: {str(e)}', ln=True)
        # conteudo e link
        pdf.cell(0, 10, "", ln=True) 
        pdf.cell(0, 10, "", ln=True)
        pdf.multi_cell(0, 10, f'Conteúdo: {noticia["conteudo"]}')
        pdf.cell(0, 10, "", ln=True) 
        pdf.cell(0, 10, "-"*120, ln=True) 
        pdf.cell(0, 10, "", ln=True)  # Linha em branco para espaçamento
        pdf.add_page()

    # Salva o PDF
    pdf.output('relatorio_noticias.pdf')