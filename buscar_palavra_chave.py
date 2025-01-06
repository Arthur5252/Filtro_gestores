import json
from coleta_noticias import *
from datetime import datetime

def filtra_noticias(palavras_chave, data_inicio, data_fim):
    # Lista para armazenar as notícias que contêm as palavras-chave e estão dentro do intervalo de datas
    noticias_filtradas = []

    # Converte as datas de início e fim para objetos datetime
    data_inicio_obj = datetime.strptime(data_inicio, "%Y/%m/%d")
    data_fim_obj = datetime.strptime(data_fim, "%Y/%m/%d")

    noticias = obter_noticias()

    # Percorre a lista de notícias
    for noticia in noticias:
        # Junta o título e o conteúdo para facilitar a busca
        texto = f"{noticia['titulo']} {noticia['conteudo']}".lower().replace('‘','')
        
        # Verifica se a palavra-chave está no texto
        if any(palavra.lower() in texto for palavra in palavras_chave):
            # Converte a data da notícia para objeto datetime
            data_noticia_obj = datetime.strptime(noticia['data'], "%d/%m/%Y")
            
            # Verifica se a data da notícia está dentro do intervalo
            if data_inicio_obj <= data_noticia_obj <= data_fim_obj:
                noticias_filtradas.append(noticia)
    # Exibe ou salva as notícias filtradas
    with open(r'jsons\noticias_filtradas.json', 'w', encoding='utf-8') as arquivo:
        json.dump(noticias_filtradas, arquivo, indent=4, ensure_ascii=False)
    return noticias_filtradas
