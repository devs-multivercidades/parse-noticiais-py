from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from tabulate import tabulate

# Configuração do diretório de saída
DIRETORIO_SAIDA = r'C:\Users\Multivercidades T.I\Documents\resultados_scraping\noticias.xlsx'


# Configurar o navegador do Selenium
def configurar_navegador():
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Erro ao inicializar o navegador: {e}")
        return None


# Função para extrair o ano da publicação
def extrair_ano(url, soup):
    # Primeiro, tentar encontrar o ano na URL
    ano_match = re.search(r'/(\d{4})/', url)
    if ano_match:
        return ano_match.group(1)

    # Verificar se há uma tag <time> com o atributo datetime contendo o ano
    time_tag = soup.find('time')
    if time_tag and time_tag.has_attr('datetime'):
        ano_match = re.search(r'(\d{4})', time_tag['datetime'])
        if ano_match:
            return ano_match.group(1)

    # Procurar em <meta> tags comuns
    meta_tags = soup.find_all('meta')
    for meta in meta_tags:
        if meta.has_attr('content'):
            ano_match = re.search(r'(\d{4})', meta['content'])
            if ano_match:
                return ano_match.group(1)

    # Procurar por padrões de data no texto da página
    body_text = soup.get_text()
    ano_match = re.search(r'\b(20\d{2}|19\d{2})\b', body_text)
    if ano_match:
        return ano_match.group(1)

    # Retorna "Ano desconhecido" se nenhuma correspondência for encontrada
    return "Ano desconhecido"


# Extrair detalhes da notícia
def extrair_detalhes_pagina(url, driver):
    try:
        driver.get(url)
        driver.implicitly_wait(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extrair título
        titulo = soup.find('title').get_text() if soup.find('title') else 'Sem título'

        # Extrair a origem (domínio do site)
        origem = url.split('/')[2]

        # Extrair o texto completo da notícia
        texto = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2'])])

        # Extrair o ano da publicação usando a função aprimorada
        ano = extrair_ano(url, soup)

        return titulo.strip(), origem, texto.strip(), ano
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return "Sem título", "Origem desconhecida", "", "Ano desconhecido"


# URLs para scraping
urls = [
    'https://g1.globo.com/pa/para/noticia/operacao-da-pf-investiga-fraudes-em-documentos-de-regularizacao-fundiaria-no-para.ghtml',
    'https://g1.globo.com/pa/para/noticia/2022/02/08/quilombolas-relatam-que-estao-encurralados-por-segurancas-encapuzados-de-empresa-fornecedora-de-dende-no-para.ghtml',
    'https://g1.globo.com/pa/para/noticia/2022/02/12/agropalma-cava-buraco-com-2-metros-de-profundidade-e-acirra-bloqueio-do-acesso-de-quilombolas-a-fazenda-no-pa-video.ghtml',
    'https://g1.globo.com/pa/para/noticia/2022/02/12/juiz-acata-pedido-da-agropalma-e-determina-que-pm-atue-na-retirada-de-quilombolas-no-acara.ghtml',
    'https://g1.globo.com/pa/para/noticia/2022/02/16/conflito-no-acara-representante-da-agropalma-assume-problemas-em-registros-de-terras-e-diz-que-empresa-aguarda-regularizacao.ghtml',
    'https://g1.globo.com/pa/para/noticia/2022/02/17/em-audiencia-quilombolas-e-agropalma-entram-em-acordo-sobre-ocupacao-de-area-no-acara.ghtml',
    'https://g1.globo.com/pa/para/noticia/2022/03/11/justica-condena-agropalma-a-pagar-r960-mil-por-condicoes-degradantes-de-trabalho-ainda-cabe-recurso.ghtml',
    'https://g1.globo.com/pa/para/noticia/2022/04/06/indigenas-tembe-ocupam-empresa-cultivadora-de-dende-no-para-apos-reuniao-da-justica-para-mediacao-de-conflito-territorial.ghtml',
    'https://g1.globo.com/pa/para/noticia/2022/07/03/vitimas-da-guerra-do-dende-quem-sao-as-liderancas-quilombolas-mortas-no-conflito-por-terras-no-pa.ghtml',
    'https://g1.globo.com/pa/para/noticia/2022/07/03/guerra-do-dende-no-para-acusacao-de-grilagem-cartorio-fantasma-e-conflitos-entre-empresas-indigenas-e-quilombolas-entenda.ghtml',
    'https://g1.globo.com/pa/para/noticia/2022/07/04/guerra-do-dende-no-para-comunidade-denuncia-que-empresa-impede-quilombolas-e-ribeirinhos-de-pescar-e-visitar-cemiterio.ghtml',
    'https://g1.globo.com/pa/para/noticia/2023/02/08/indigenas-e-quilombolas-protestam-na-delegacia-do-acara-no-pa-apos-acao-do-bope-com-prisoes-e-apontam-presenca-de-segurancas-privados.ghtml',
    'https://g1.globo.com/pa/para/noticia/2023/02/16/empresa-que-explora-oleo-de-dende-no-para-tem-certificacao-internacional-suspensa.ghtml',
    'https://g1.globo.com/pa/para/noticia/2023/02/18/familiar-de-ex-lideranca-quilombola-e-assassinado-a-tiros-em-cidade-no-interior-do-para.ghtml',
    'https://g1.globo.com/pa/para/noticia/2023/04/17/policia-desmonta-ocupacao-de-quilombolas-em-area-de-conflito-no-acara-no-para.ghtml',
    'https://g1.globo.com/pa/para/noticia/2023/08/23/conflito-do-dende-indigenas-denunciam-grande-buraco-cavado-por-empresa-no-para.ghtml',
    'https://g1.globo.com/pa/para/noticia/2023/10/12/acao-quer-suspender-obras-de-mineroduto-dentro-de-area-quilombola-no-para.ghtml',
    'https://g1.globo.com/pa/para/noticia/2023/11/12/pf-abre-inquerito-para-investigar-morte-de-indigena-em-area-de-producao-de-oleo-de-palma-no-para.ghtml',
    'https://g1.globo.com/pa/para/noticia/2023/11/12/pf-abre-inquerito-para-investigar-morte-de-indigena-em-area-de-producao-de-oleo-de-palma-no-para.ghtml',
    'https://g1.globo.com/pa/para/noticia/2023/08/23/conflito-do-dende-indigenas-denunciam-grande-buraco-cavado-por-empresa-no-para.ghtml',
    'https://g1.globo.com/pa/para/noticia/2024/01/05/guerra-do-dende-pistoleiros-deixam-tres-indigenas-feridos-em-2a-invasao-a-aldeia-de-pa-em-menos-de-uma-semana.ghtml',
    'https://g1.globo.com/pa/para/noticia/2024/01/30/quilombolas-denunciam-que-obras-em-mineroduto-impedem-circulacao-de-moradores-no-pa-empresa-nega.ghtml',
    'https://oglobo.globo.com/brasil/noticia/2024/01/31/milicia-conflitos-armados-guerra-do-dende-entenda-a-acao-da-pf-que-prendeu-liderancas-indigenas-no-para.ghtml',
    'https://oglobo.globo.com/brasil/noticia/2024/02/01/triste-chegar-a-esse-ponto-secretaria-de-povos-indigenas-do-pa-reage-a-prisao-de-lideres-tembe-por-suspeita-de-milicia.ghtml',
    'https://g1.globo.com/pa/para/noticia/2024/03/19/guerra-do-dende-pf-prende-policial-militar-da-reserva-que-atuava-em-milicia-invasora-de-terras-em-disputa-por-indigenas-no-pa.ghtml',
    'https://g1.globo.com/pa/para/noticia/2024/06/27/justica-determina-liberacao-de-tres-pessoas-levadas-em-acao-da-pm-sem-mandado-em-comunidade-quilombola-no-para.ghtml',
    'https://g1.globo.com/pa/para/noticia/2024/08/22/area-disputada-por-indigenas-e-empresa-agropalma-e-palco-de-conflito-violento-no-para.ghtml',
    'https://g1.globo.com/pa/para/noticia/2024/08/23/mpf-apura-denuncia-de-carcere-privado-de-segurancas-de-empresa-contra-indigenas-no-para.ghtml',
    'https://g1.globo.com/pa/para/noticia/2024/09/17/comunidades-tradicionais-protestam-contra-instalacao-de-mineroduto-no-para.ghtml',
    'https://g1.globo.com/pa/para/noticia/2024/09/24/indigenas-e-quilombolas-do-acara-protestam-contra-obra-de-mineradora-em-comunidades-tradicionais.ghtml',
    'https://g1.globo.com/pa/para/noticia/2024/08/22/area-disputada-por-indigenas-e-empresa-agropalma-e-palco-de-conflito-violento-no-para.ghtml',
    'https://www.mpf.mp.br/pa/sala-de-imprensa/noticias-pa/mpf-busca-garantir-direito-a-saude-dos-indigenas-da-etnia-turiwara-no-municipio-de-tome-acu-pa',
    ''
]

# Inicializa o navegador
driver = configurar_navegador()

# Lista para armazenar os dados e o status
dados = []
status_execucao = []

if driver:
    for i, url in enumerate(urls, start=1):
        print(f"Acessando {url}...")

        titulo, origem, conteudo, ano = extrair_detalhes_pagina(url, driver)

        if conteudo:
            # Adiciona os dados extraídos na lista
            dados.append({
                'Número': i,
                'Ano': ano,
                'Título': titulo,
                'Origem': origem,
                'Texto Completo': conteudo
            })
            status_execucao.append([i, 'Sucesso'])
        else:
            status_execucao.append([i, 'Falha'])

        # Exibir a tabela atualizada no terminal
        print(tabulate(status_execucao, headers=["Nº da Notícia", "Status"], tablefmt="grid"))

        time.sleep(5)  # Espera entre requisições

    driver.quit()  # Fecha o navegador
else:
    print("Não foi possível iniciar o navegador.")

# Salvar os dados no Excel
if dados:
    # Converter a lista de dicionários em um DataFrame do pandas
    df = pd.DataFrame(dados)

    # Salvar no arquivo Excel
    df.to_excel(DIRETORIO_SAIDA, index=False)
    print(f"Dados salvos em: {DIRETORIO_SAIDA}")
else:
    print("Nenhuma notícia foi extraída.")
