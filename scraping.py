from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Importação correta
from bs4 import BeautifulSoup
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv
import time
import re  # Para sanitizar o nome do arquivo

# Configurar o navegador do Selenium
def configurar_navegador():
    try:
        options = Options()
        options.add_argument("--headless")  # Modo headless (sem abrir janela)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Erro ao inicializar o navegador: {e}")
        return None  # Retorna None se o driver falhar

# Extrair detalhes da página, incluindo título e data de publicação
def extrair_detalhes_pagina(url, driver):
    try:
        driver.get(url)
        driver.implicitly_wait(10)  # Espera implícita para carregamento
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extrair título da matéria
        titulo = soup.find('title').get_text() if soup.find('title') else 'Sem título'
        titulo_limpo = ' '.join(titulo.split()[:2])  # Pega os 2 primeiros termos do título

        # Extrair data de publicação (tenta encontrar em <time> ou <meta>)
        data = soup.find('time')
        if data and data.has_attr('datetime'):
            data_publicacao = data['datetime']
        else:
            meta_data = soup.find('meta', {'name': 'article:published_time'})
            data_publicacao = meta_data['content'] if meta_data else 'Data desconhecida'

        # Extrair textos principais da página
        textos = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2'])])
        return titulo_limpo, data_publicacao, textos.strip()
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return "Sem título", "Data desconhecida", ""

# Processar o texto e retornar as palavras mais frequentes
def processar_texto(texto):
    palavras = word_tokenize(texto.lower(), language='portuguese')
    stop_words = set(stopwords.words('portuguese'))
    palavras_filtradas = [palavra for palavra in palavras if palavra.isalnum() and palavra not in stop_words]
    frequencia = Counter(palavras_filtradas)
    return frequencia.most_common(10)

# Salvar os termos relevantes em um arquivo CSV
def salvar_termos_csv(termos, nome_arquivo='termos_relevantes.csv'):
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8-sig') as arquivo:
        escritor = csv.writer(arquivo, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        escritor.writerow(['Termo', 'Frequência'])
        escritor.writerows(termos)

# Sanitizar o nome do arquivo para evitar caracteres inválidos
def sanitizar_nome_arquivo(titulo, data):
    titulo_limpo = re.sub(r'[^\w\-_\. ]', '_', titulo)
    data_limpa = re.sub(r'[^\w\-_]', '_', data)
    return f"termos_{titulo_limpo}_{data_limpa}.csv"

# Lista de URLs para scraping
urls = [
    'https://reporterbrasil.org.br/2013/07/plantio-de-dende-entra-na-lista-de-atividades-com-trabalho-escravo/',
    'https://portaltailandia.com/tailandia-pa/tailandia-trabalhadores-da-agropalma-interditam-a-rodovia-pa-150/',
    'https://portaltailandia.com/para/comunidade-quilombola-de-moju-recebe-titulo-de-terra-do-governo/',
    'https://racismoambiental.net.br/2016/01/14/povo-tembe-lanca-nota-de-repudio-as-violencias-cometidas-contra-indigenas-e-quilombolas-nos-municipios-de-acara-e-tome-acu-pa/',
    'https://portaltailandia.com/para/corpo-de-lider-quilombola-e-encontrado-enterrado-as-margens-do-rio-moju/',
    'https://portaltailandia.com/para/tiraram-sua-vida-da-forma-mais-cruel-possivel-lamenta-sobrinha-de-lider-quilombola-morta-em-moju/',
    'https://www.zedudu.com.br/dia-do-indio-sem-muito-comemorar-com-as-terras-indigenas-ameacadas-pela-pec-215/',
    'https://www.brasildefato.com.br/2017/05/17/monocultura-do-dende-traz-impactos-ambientais-para-comunidades-no-nordeste-paraense',
    'https://g1.globo.com/pa/para/noticia/operacao-da-pf-investiga-fraudes-em-documentos-de-regularizacao-fundiaria-no-para.ghtml',
    'https://portaltailandia.com/tailandia-pa/justica-garante-posse-de-terras-no-baixo-tocantins-a-agropalma/'
]

# Inicializando o navegador
driver = configurar_navegador()

if driver:  # Verificar se o driver foi inicializado com sucesso
    for url in urls:
        print(f"Acessando {url}...")
        titulo, data, conteudo = extrair_detalhes_pagina(url, driver)

        if conteudo:
            termos_relevantes = processar_texto(conteudo)
            nome_arquivo = sanitizar_nome_arquivo(titulo, data)
            salvar_termos_csv(termos_relevantes, nome_arquivo)
            print(f"Termos salvos para {url} em {nome_arquivo}\n")
        else:
            print(f"Nenhum conteúdo extraído de {url}.")

        time.sleep(5)  # Esperar 5 segundos entre as requisições

    driver.quit()  # Fechar o navegador
else:
    print("Não foi possível iniciar o navegador. Verifique sua configuração.")