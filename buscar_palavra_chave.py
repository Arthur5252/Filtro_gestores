from coleta_noticias import *
from datetime import datetime
import logging
import json

# Log configuration (assumindo que você já tenha configurado o logging no app principal)
logger = logging.getLogger(__name__)

def filtra_noticias(palavras_chave, data_fixa):
    # Lista para armazenar as notícias que contêm as palavras-chave e são a partir da data fixa
    noticias_filtradas = []
    data_atual = datetime.now().strftime('%d/%m/%Y')

    try:
        logger.info(f"Iniciando o processo de filtragem de notícias para a data {data_atual}.")

        noticias = obter_noticias()  # Função que obtém as notícias
        logger.info(f"Obtidas {len(noticias)} notícias para o filtro.")

        # Percorre a lista de notícias
        for noticia in noticias:
            try:
                # Junta o título e o conteúdo para facilitar a busca
                texto = f"{noticia['titulo']} {noticia['conteudo']}".lower().replace('‘', '')
                
                # Verifica se a palavra-chave está no texto
                if any(palavra.lower() in texto for palavra in palavras_chave):
                    # Converte a data da notícia para objeto datetime
                    data_noticia_obj = datetime.strptime(noticia['data'], "%d/%m/%Y")
                    
                    # Verifica se a data da notícia é a partir da data fixa
                    if data_noticia_obj == data_atual:
                        noticias_filtradas.append(noticia)
            
            except KeyError as e:
                logger.error(f"Erro ao processar notícia. Chave ausente: {e}")
            except Exception as e:
                logger.error(f"Erro inesperado ao processar a notícia: {str(e)}")

        # Exibe ou salva as notícias filtradas em um arquivo JSON
        if noticias_filtradas:
            with open(r'jsons\noticias_filtradas.json', 'w', encoding='utf-8') as arquivo:
                json.dump(noticias_filtradas, arquivo, indent=4, ensure_ascii=False)
            logger.info(f"{len(noticias_filtradas)} notícias filtradas e salvas no arquivo 'noticias_filtradas.json'.")
        else:
            logger.warning("Nenhuma notícia filtrada correspondente aos critérios fornecidos.")

        return noticias_filtradas

    except Exception as e:
        logger.error(f"Erro ao tentar filtrar as notícias: {str(e)}")
        return []

