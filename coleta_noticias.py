import requests
import json

def obter_noticias():
    url = 'http://api.octopustax.com.br/informative/v1/news'
    url_base_octopus = 'http://informativo.octopustax.com.br/news/'

    response = requests.get(url)

    if response.status_code == 200:
        data_response = response.json()

        if isinstance(data_response, list):
                noticias = []

                # Loop para processar cada item na resposta
                for i in data_response:
                    json_noticias = {
                        'titulo': i['titulo'],
                        'conteudo': i['conteudo'],
                        'data': i['criado'].split(' ')[0],
                        'imagem': i['urllinkimg'],
                        'link': url_base_octopus + i['codigo']
                    }
                    noticias.append(json_noticias)  # Adiciona a notícia à lista

                # Grava a lista completa de notícias em um único arquivo JSON
                with open(r'jsons\noticias.json', 'w', encoding='utf-8') as arquivo:
                    json.dump(noticias, arquivo, indent=4, ensure_ascii=False)
                return noticias
