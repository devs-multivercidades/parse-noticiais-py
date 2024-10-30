from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
from tabulate import tabulate  # Biblioteca para exibir tabelas no terminal

# Configuração do diretório de saída
DIRETORIO_SAIDA = r'C:\Users\Multivercidades T.I\Documents\resultados_scraping\noticias.xlsx'


# Configurar o navegador do Selenium
def configurar_navegador():
    try:
        options = Options()
        options.add_argument("--headless")  # Executa sem abrir janela
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Erro ao inicializar o navegador: {e}")
        return None


# Extrair detalhes da notícia: título, origem e texto completo
def extrair_detalhes_pagina(url, driver):
    try:
        driver.get(url)
        driver.implicitly_wait(10)  # Espera implícita para carregar a página
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extrair título
        titulo = soup.find('title').get_text() if soup.find('title') else 'Sem título'

        # Extrair a origem (domínio do site)
        origem = url.split('/')[2]

        # Extrair o texto completo da notícia
        texto = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2'])])

        return titulo.strip(), origem, texto.strip()
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return "Sem título", "Origem desconhecida", ""


# URLs para scraping (adicione suas URLs aqui)
urls = [
    'https://www.biodieselbr.com/blog/vedana/2010/situacao-da-agropalma-causa-estranheza/',
    'https://reporterbrasil.org.br/2012/12/denuncias-de-violencia-e-trabalho-escravo-envolvem-cultura-do-dende-no-para/',
    'https://reporterbrasil.org.br/2013/07/plantio-de-dende-entra-na-lista-de-atividades-com-trabalho-escravo/',
    'https://portaltailandia.com/tailandia-pa/tailandia-trabalhadores-da-agropalma-interditam-a-rodovia-pa-150/',
    'https://portaltailandia.com/para/comunidade-quilombola-de-moju-recebe-titulo-de-terra-do-governo/',
    'https://racismoambiental.net.br/2016/01/14/povo-tembe-lanca-nota-de-repudio-as-violencias-cometidas-contra-indigenas-e-quilombolas-nos-municipios-de-acara-e-tome-acu-pa/',
    'https://portaltailandia.com/para/corpo-de-lider-quilombola-e-encontrado-enterrado-as-margens-do-rio-moju/',
    'https://portaltailandia.com/para/tiraram-sua-vida-da-forma-mais-cruel-possivel-lamenta-sobrinha-de-lider-quilombola-morta-em-moju/',
    'https://www.zedudu.com.br/dia-do-indio-sem-muito-comemorar-com-as-terras-indigenas-ameacadas-pela-pec-215/',
    'https://www.brasildefato.com.br/2017/05/17/monocultura-do-dende-traz-impactos-ambientais-para-comunidades-no-nordeste-paraense/',
    'https://g1.globo.com/pa/para/noticia/operacao-da-pf-investiga-fraudes-em-documentos-de-regularizacao-fundiaria-no-para.ghtml/',
    'https://portaltailandia.com/tailandia-pa/justica-garante-posse-de-terras-no-baixo-tocantins-a-agropalma/',
    'https://amazoniareal.com.br/morte-de-nazildo-permanece-na-impunidade-no-para/',
    'https://ver-o-fato.com.br/bomba-acordo-da-vale-e-hydro-com-quilombolas-e-anulado-por-irregularidades/',
    'https://summitagro.estadao.com.br/colunistas/arvores-marcadas-para-morrer/',
    'https://portaltailandia.com/para/para-arvores-marcadas-para-morrer/',
    'https://ver-o-fato.com.br/exclusivo-agropalma-despeja-dende-e-contamina-rio-acara/',
    'https://ver-o-fato.com.br/justica-nega-pedido-da-agropalma-e-mantem-postagens-de-criticas-ao-iterpa-na-internet/',
    'https://brasildefatorj.com.br/2021/07/07/quilombolas-lutam-pela-terra-contra-gigante-do-agronegocio-e-pedem-o-fim-da-violencia-no-para/',
    'https://www.brasildefato.com.br/2021/07/09/gigante-do-agronegocio-ocupa-e-viola-tres-cemiterios-quilombolas-e-um-indigena-no-para/',
    'https://dol.com.br/noticias/para/666598/agropalma-cancelamento-de-titulo-e-seguranca-juridica-no-pa?d=1/',
    'https://www.oliberal.com/politica/suspeitos-de-crimes-de-grilagem-de-terras-da-agropalma-sao-intimados-pela-justica-1.430092/',
    'https://ver-o-fato.com.br/comunidades-do-acara-denunciam-agropalma-contaminou-rio-com-tibornia-e-matou-peixes-video/',
    'https://colunaolavodutra.com.br/podres-poderes/',
    'https://www.oliberal.com/politica/tribunal-de-justica-cancela-propriedades-da-agropalma-1.443641/',
    'https://ver-o-fato.com.br/exclusivo-agropalma-planta-dende-com-licenca-ambiental-vencida-desde-2020-na-semas/',
    'https://www.ihu.unisinos.br/categorias/625023-exportadora-de-oleo-de-palma-acusada-de-fraude-grilagem-de-terras-em-cemiterios-quilombolas/',
    'https://ojoioeotrigo.com.br/2022/02/quilombolas-encurralados-por-segurancas-armados-e-encapuzados-da-agropalma-fornecedora-de-oleo-de-palma-para-nestle/',
    'https://g1.globo.com/pa/para/noticia/2022/02/08/quilombolas-relatam-que-estao-encurralados-por-segurancas-encapuzados-de-empresa-fornecedora-de-dende-no-para.ghtml/',
    'https://dol.com.br/noticias/para/696684/agropalma-esclarecimento-a-sociedade?d=1/',
    'https://g1.globo.com/pa/para/noticia/2022/02/12/agropalma-cava-buraco-com-2-metros-de-profundidade-e-acirra-bloqueio-do-acesso-de-quilombolas-a-fazenda-no-pa-video.ghtml/',
    'https://g1.globo.com/pa/para/noticia/2022/02/12/juiz-acata-pedido-da-agropalma-e-determina-que-pm-atue-na-retirada-de-quilombolas-no-acara.ghtml/',
    'https://dol.com.br/comercial/697280/invasao-em-area-da-agropalma-chega-ao-10-dia?d=1/',
    'https://g1.globo.com/pa/para/noticia/2022/02/16/conflito-no-acara-representante-da-agropalma-assume-problemas-em-registros-de-terras-e-diz-que-empresa-aguarda-regularizacao.ghtml/',
    'https://g1.globo.com/pa/para/noticia/2022/02/17/em-audiencia-quilombolas-e-agropalma-entram-em-acordo-sobre-ocupacao-de-area-no-acara.ghtml/',
    'https://portalrdn.com.br/2022/02/18/quilombolas-devem-deixar-area-de-reserva-da-agropalma/',
    'https://ojoioeotrigo.com.br/2022/02/nestle-compra-oleo-de-palma-de-empresas-envolvidas-em-violacoes-de-direitos-humanos-na-amazonia-paraense/',
    'https://dol.com.br/comercial/697280/invasao-em-area-da-agropalma-chega-ao-10-dia?d=1/',
    'https://ojoioeotrigo.com.br/2022/02/quilombolas-encurralados-por-segurancas-armados-e-encapuzados-da-agropalma-fornecedora-de-oleo-de-palma-para-nestle/',
    'https://www.oliberal.com/para/mp-e-tjpa-discutem-conflitos-entre-empresas-de-dende-e-comunidades-tradicionais-no-para-1.516303/',
    'https://ver-o-fato.com.br/bomba-acusada-de-grilagem-e-com-58-mil-hectares-cancelados-pela-justica-agropalma-esta-a-venda/',
    'https://www.brasildefato.com.br/2022/02/28/nestle-por-que-te-calas-diante-da-violencia-que-patrocinas/',
    'https://portaltailandia.com/tailandia-pa/em-audiencia-agropalma-e-quilombolas-firmam-acordo-sobre-terra-invadida/',
    'https://g1.globo.com/pa/para/noticia/2022/03/11/justica-condena-agropalma-a-pagar-r960-mil-por-condicoes-degradantes-de-trabalho-ainda-cabe-recurso.ghtml/',
    'https://www.oliberal.com/politica/agropalma-e-condenada-a-pagar-quase-r-1milhao-por-dano-moral-coletivo-1.508587/',
    'https://www.oliberal.com/para/encontro-de-quilombolas-e-ribeirinhos-em-belem-traz-desafios-das-comunidades-ouca-1.497371/',
    'https://ver-o-fato.com.br/video-ribeirinhos-acusam-agropalma-por-despejo-de-produto-quimico-e-morte-de-peixes/',
    'https://g1.globo.com/pa/para/noticia/2022/04/06/indigenas-tembe-ocupam-empresa-cultivadora-de-dende-no-para-apos-reuniao-da-justica-para-mediacao-de-conflito-territorial.ghtml/',
    'https://ver-o-fato.com.br/exclusivo-com-venda-de-carbono-dende-e-minerio-agropalma-vale-r-5-bilhoes-e-problemas/',
    'https://amazoniareal.com.br/indigenas-turiwara-sao-alvos-de-dois-ataques-no-para/',
    'https://dol.com.br/noticias/para/710483/agropalma-e-alvo-de-nova-invasao-de-terras-no-estado?d=1/',
    'https://ver-o-fato.com.br/acara-agropalma-volta-a-impedir-acesso-de-comunidades-a-rio-e-cemiterio-diz-associacao-video/',
    'https://www.paraterraboa.com/agricultura/industria-do-dende-no-para-esta-em-conflito-de-terra-com-indigenas-e-quilombolas/',
    'https://g1.globo.com/pa/para/noticia/2022/07/03/vitimas-da-guerra-do-dende-quem-sao-as-liderancas-quilombolas-mortas-no-conflito-por-terras-no-pa.ghtml/',
    'https://g1.globo.com/pa/para/noticia/2022/07/03/guerra-do-dende-no-para-acusacao-de-grilagem-cartorio-fantasma-e-conflitos-entre-empresas-indigenas-e-quilombolas-entenda.ghtml/',
    'https://www.metropoles.com/materias-especiais/ouro-liquido-producao-de-dende-explora-populacoes-negras-e-indigenas-no-brasil-2/',
    'https://g1.globo.com/pa/para/noticia/2022/07/03/guerra-do-dende-no-para-acusacao-de-grilagem-cartorio-fantasma-e-conflitos-entre-empresas-indigenas-e-quilombolas-entenda.ghtml/',
    'https://g1.globo.com/pa/para/noticia/2022/07/04/guerra-do-dende-no-para-comunidade-denuncia-que-empresa-impede-quilombolas-e-ribeirinhos-de-pescar-e-visitar-cemiterio.ghtml/',
    'https://portaltailandia.com/tailandia-pa/em-audiencia-agropalma-e-quilombolas-firmam-acordo-sobre-terra-invadida/',
    'https://www.oliberal.com/para/agropalma-isola-e-intimida-quilombolas-em-tailandia-no-para-1.495789/',
    'https://ver-o-fato.com.br/urgente-mp-do-para-na-justica-contra-crueldade-da-agropalma-sobre-quilombolas-do-acara-video/',
    'https://www.brasildefato.com.br/2022/08/08/cercados-pelo-dende-povos-tradicionais-vivem-terror-em-disputa-com-produtora-de-biodiesel/',
    'https://ver-o-fato.com.br/exclusivo-agropalma-ignora-mp-e-intimida-quilombolas-do-acara-fechando-acesso-a-rio-video/',
    'https://amazoniareal.com.br/tembe-ocupam-bbf/',
    'https://ver-o-fato.com.br/agropalma-quer-saida-de-quilombolas-proibe-caca-e-pesca-acordo-quebrado-diz-lideranca/',
    'https://www.metropoles.com/brasil/homem-e-baleado-e-tem-corpo-incendiado-em-conflito-no-para-video/',
    'https://www.ihu.unisinos.br/categorias/621435-com-inercia-do-governo-empresas-do-dende-avancam-sobre-terras-publicas-da-amazonia/',
    'https://ver-o-fato.com.br/acara-tembes-tem-dende-apreendido-queimam-tres-onibus-e-invadem-empresa-bbf/',
    'https://reporterbrasil.org.br/2022/08/cercados-pelo-dende-povos-tradicionais-vivem-terror-em-disputa-fundiaria-com-produtora-de-biodiesel/',
    'https://www.paraterraboa.com/agricultura/industria-do-dende-no-para-esta-em-conflito-de-terra-com-indigenas-e-quilombolas/',
    'https://www.correiobraziliense.com.br/brasil/2022/09/5039626-guerra-do-dende-indigenas-sao-assassinados-no-interior-do-para.html/',
    'https://www.oliberal.com/para/indigenas-e-quilombolas-denunciam-empresa-bbf-de-bloquear-acesso-as-comunidades-1.510725/',
    'https://cimi.org.br/2022/09/ataque-armado-turiwara-acara/',
    'https://www.oliberal.com/para/com-discurso-de-sustentabilidade-producao-de-dende-na-amazonia-ataca-quilombolas-e-indigenas-1.511828/',
    'https://www.paraterraboa.com/meio-ambiente/apos-ocupacao-povo-tembe-relata-presenca-de-milicianos-a-mando-da-bbf/',
    'https://www.oliberal.com/para/mp-e-tjpa-discutem-conflitos-entre-empresas-de-dende-e-comunidades-tradicionais-no-para-1.516303/',
    'https://www.paraterraboa.com/gente-da-terra/gigantes-do-dende-avancaram-sobre-terras-publicas-no-para/',
    'https://www.ihu.unisinos.br/categorias/621435-com-inercia-do-governo-empresas-do-dende-avancam-sobre-terras-publicas-da-amazonia/',
    'https://www.oliberal.com/para/mp-e-tjpa-discutem-conflitos-entre-empresas-de-dende-e-comunidades-tradicionais-no-para-1.516303/',
    'https://vermelho.org.br/2022/09/25/pistoleiros-matam-um-indigena-e-ferem-tres-em-emboscada-no-para/',
    'https://btmais.com.br/nice-tupinamba-povo-tembe-teme-assassinato-de-liderancas-em-tome-acu/',
    'https://www.globalwitness.org/pt/amazonpalm-pt/',
    'https://cimi.org.br/2022/09/ataque-armado-turiwara-acara/',
    'https://amazoniareal.com.br/indigenas-turiwara-sao-alvos-de-dois-ataques-no-para/',
    'https://portaltailandia.com/tailandia-pa/quilombolas-deixam-area-da-agropalma-apos-acordo-de-conciliacao/',
    'https://webstories.metropoles.com/producao-de-dende-explora-populacao-negras-e-indigenas-no-brasil/',
    'https://g1.globo.com/pa/para/noticia/2023/02/08/indigenas-e-quilombolas-protestam-na-delegacia-do-acara-no-pa-apos-acao-do-bope-com-prisoes-e-apontam-presenca-de-segurancas-privados.ghtml/',
    'https://g1.globo.com/pa/para/noticia/2023/02/16/empresa-que-explora-oleo-de-dende-no-para-tem-certificacao-internacional-suspensa.ghtml/',
    'https://g1.globo.com/pa/para/noticia/2023/02/18/familiar-de-ex-lideranca-quilombola-e-assassinado-a-tiros-em-cidade-no-interior-do-para.ghtml/',
    'https://www.terra.com.br/nos/multinacional-e-governo-do-para-sao-denunciados-por-violacoes-em-terras-quilombolas,b30428c5a1871af8ffe85cb64902fc32co24pb97.html#google_vignette/',
    'https://g1.globo.com/pa/para/noticia/2023/04/17/policia-desmonta-ocupacao-de-quilombolas-em-area-de-conflito-no-acara-no-para.ghtml/',
    'https://midianinja.org/indigenas-quilombolas-e-ribeirinhos-revelam-sofrer-ameacas-e-invasoes-vindas-da-mineradora-hydro/',
    'https://www.terra.com.br/nos/quilombos-do-para-estao-na-mira-do-comando-vermelho,5ab8c3ea09ac4df305742a2794108cc00m473vq8.html/',
    'https://www.brasildefato.com.br/2023/04/28/governo-lula-anuncia-demarcacao-de-seis-terras-indigenas/',
    'https://www.brasildefato.com.br/2023/08/07/tres-indigenas-sao-baleados-durante-missao-em-defesa-dos-direitos-humanos-no-para/',
    'https://www.paraterraboa.com/gente-da-terra/apos-atentado-contra-cacique-em-tome-acu-reuniao-define-comite-para-atuar-no-direito-a-terra/',
    'https://cimi.org.br/2023/08/liderancas-tembe-sao-alvejadas-por-segurancas-de-empresa-produtora-de-oleo-de-palma/',
    'https://g1.globo.com/pa/para/noticia/2023/08/23/conflito-do-dende-indigenas-denunciam-grande-buraco-cavado-por-empresa-no-para.ghtml/',
    'https://www.brasildefato.com.br/2023/08/30/qual-a-origem-da-guerra-do-dende-no-para-e-por-que-os-indigenas-tembe-querem-expulsar-a-brasil-biofuels-bbf/',
    'https://www.brasildefato.com.br/2023/08/30/validacao-do-marco-temporal-deve-agravar-guerra-do-dende-no-para/',
    'https://www.cartacapital.com.br/sociedade/lider-indigena-tembe-e-alvo-de-pistoleiros-no-para/',
    'https://amazoniareal.com.br/segurancas-da-bbf/',
    'https://colunaolavodutra.com.br/invasores-e-liderancas-indigenas-vao-as-vias-de-fato-em-tome-acu-e-concorrente-do-crime-acaba-no-hospital/',
    'https://almapreta.com.br/sessao/cotidiano/multinacional-hydro-governo-para-violacoes-terras-quilombolas/',
    'https://oeco.org.br/reportagens/conflito-entre-quilombolas-e-agroindustria-do-dende-no-para-impede-a-livre-circulacao-de-moradores-dentro-de-comunidade/',
    'https://g1.globo.com/pa/para/noticia/2023/10/12/acao-quer-suspender-obras-de-mineroduto-dentro-de-area-quilombola-no-para.ghtml/',
    'https://ver-o-fato.com.br/e-mentira-da-agropalma-os-quilombolas-nao-invadiram-terras-afirma-lider-da-arqva/',
    'https://g1.globo.com/pa/para/noticia/2023/11/12/pf-abre-inquerito-para-investigar-morte-de-indigena-em-area-de-producao-de-oleo-de-palma-no-para.ghtml/',
    'https://racismoambiental.net.br/2023/11/12/liderancas-denunciam-segurancas-da-agropalma-matam-um-indigena-e-ferem-outro-no-vale-do-acara/',
    'https://redepara.com.br/Noticia/238263/agropalma-e-invadida-no-para/',
    'https://btmais.com.br/indigena-morre-baleado-por-segurancas-de-empresa-em-tailandia-denuncia-etnia-turiwara/',
    'https://dol.com.br/noticias/para/835712/terras-da-agropalma-no-para-sao-invadidas-pela-terceira-vez?d=1/',
    'https://diariodopara.com.br/para/terras-da-agropalma-sao-invadidas-novamente-no-para/',
    'https://ver-o-fato.com.br/exclusivo-com-problemas-de-grilagem-e-quilombolas-agropalma-e-vendida-por-mais-de-r-1-bilhao/',
    'https://ver-o-fato.com.br/urgente-segurancas-da-agropalma-matam-um-indigena-e-ferem-outro-no-vale-do-acara/',
    'https://ver-o-fato.com.br/exclusivo-segurancas-da-agropalma-que-mataram-indigena-estao-soltos-governador-calado/',
    'https://ver-o-fato.com.br/exclusivo-indigena-e-sepultado-sob-tensao-e-medo-turiwara-querem-pf-no-caso/',
    'https://ver-o-fato.com.br/urgente-exclusivo-certificacao-internacional-das-plantacoes-da-agropalma-no-para-esta-suspensa/',
    'https://ver-o-fato.com.br/agropalma-semas-arquiva-licenciamento-ambiental-e-suspende-cadastro-rural/',
    'https://btmais.com.br/indigena-morre-baleado-por-segurancas-de-empresa-em-tailandia-denuncia-etnia-turiwara/',
    'https://racismoambiental.net.br/2023/11/12/liderancas-denunciam-segurancas-da-agropalma-matam-um-indigena-e-ferem-outro-no-vale-do-acara/',
    'https://g1.globo.com/pa/para/noticia/2023/11/12/pf-abre-inquerito-para-investigar-morte-de-indigena-em-area-de-producao-de-oleo-de-palma-no-para.ghtml/',
    'https://averdade.org.br/2023/12/agronegocio-no-para-e-responsavel-por-ataques-a-comunidades-indigenas-e-quilombolas/',
    'https://g1.globo.com/pa/para/noticia/2024/01/05/guerra-do-dende-pistoleiros-deixam-tres-indigenas-feridos-em-2a-invasao-a-aldeia-de-pa-em-menos-de-uma-semana.ghtml/',
    'https://g1.globo.com/pa/para/noticia/2024/01/30/quilombolas-denunciam-que-obras-em-mineroduto-impedem-circulacao-de-moradores-no-pa-empresa-nega.ghtml/',
    'https://oglobo.globo.com/brasil/noticia/2024/01/31/milicia-conflitos-armados-guerra-do-dende-entenda-a-acao-da-pf-que-prendeu-liderancas-indigenas-no-para.ghtml/',
    'https://oglobo.globo.com/brasil/noticia/2024/02/01/triste-chegar-a-esse-ponto-secretaria-de-povos-indigenas-do-pa-reage-a-prisao-de-lideres-tembe-por-suspeita-de-milicia.ghtml/',
    'https://revistacenarium.com.br/mpf-e-dpu-pedem-suspensao-de-licencas-para-mineroduto-em-terras-indigenas-no-para/',
    'https://www.mpf.mp.br/pa/sala-de-imprensa/noticias-pa/mpf-busca-garantir-direito-a-saude-dos-indigenas-da-etnia-turiwara-no-municipio-de-tome-acu-pa/',
    'https://www.metropoles.com/distrito-federal/na-mira/pf-prende-pm-acusado-de-integrar-milicia-que-invade-terras-indigenas/',
    'https://g1.globo.com/pa/para/noticia/2024/03/19/guerra-do-dende-pf-prende-policial-militar-da-reserva-que-atuava-em-milicia-invasora-de-terras-em-disputa-por-indigenas-no-pa.ghtml/',
    'https://g1.globo.com/pa/para/noticia/2024/06/27/justica-determina-liberacao-de-tres-pessoas-levadas-em-acao-da-pm-sem-mandado-em-comunidade-quilombola-no-para.ghtml/',
    'https://www.terra.com.br/nos/prisao-de-indigenas-em-operacao-da-policia-federal-no-para-e-retaliacao-diz-lideranca,baabd0ceec3b8621701c9fbf80cace5awclu2cvk.html/',
    'https://g1.globo.com/pa/para/noticia/2024/08/22/area-disputada-por-indigenas-e-empresa-agropalma-e-palco-de-conflito-violento-no-para.ghtml/',
    'https://revistacenarium.com.br/indigenas-turiwara-denunciam-ataques-armados-por-segurancas-da-empresa-agropalma-no-para/',
    'https://oantagonico.net.br/a-agropalma-a-nova-invasao-os-quilombolas-indigenas-o-tj-e-a-reintegracao-imediata/',
    'https://g1.globo.com/pa/para/noticia/2024/08/23/mpf-apura-denuncia-de-carcere-privado-de-segurancas-de-empresa-contra-indigenas-no-para.ghtml/',
    'https://oantagonico.net.br/a-agropalma-a-associacao-vale-do-acara-a-nova-invasao-o-tj-e-a-reintegracao-de-posse/',
    'https://www.belemnegocios.com/post/area-monitorada-por-projeto-da-agropalma-e-berco-de-especie-ameacado-de-extincao/',
    'https://btmais.com.br/segurancas-da-agropalma-conflito-com-indigenas-para/#google_vignette/',
    'https://oantagonico.net.br/o-oleo-de-palma-o-para-a-agroplama-a-biovale-a-taua-brasil-a-belem-bioenergia-as-1-697-acoes-trabalhistas/',
    'https://portaltailandia.com/tailandia-pa/agropalma-afirma-que-fazenda-da-empresa-sofreu-uma-nova-invasao-no-para/',
    'https://ver-o-fato.com.br/urgente-mpf-recorre-contra-reintegracao-de-posse-a-agropalma-conflito-com-indigenas/',
    'https://ver-o-fato.com.br/videos-acusacoes-tirose-cercas-aprofundam-tensoes-entre-agropalma-e-indigenas/',
    'https://ver-o-fato.com.br/embuste-por-tras-da-certificacao-do-oleo-de-palma-da-agropalma-denuncia-site/',
    'https://ver-o-fato.com.br/exclusivo-quebra-de-sigilo-comprova-corrupcao-da-agropalma-e-cartorario-mpf-pede-condenacao/',
    'https://ver-o-fato.com.br/exclusivo-tabarana-minha-familia-quer-das-5-herdeiras-da-agropalma-nossas-terras-volta/',
    'https://www.brasildefato.com.br/2024/08/30/indigenas-retomam-area-no-para-sob-dominio-da-agropalma-e-sao-agredidos-por-segurancas/',
    'https://www.brasildefato.com.br/2024/08/30/indigenas-retomam-area-no-para-sob-dominio-da-agropalma-e-sao-agredidos-por-segurancas/',
    'https://www.theagribiz.com/empresas/bioenergia/do-dende-ao-ataque-a-indigenas-o-que-detonou-a-crise-financeira-da-bbf/',
    'https://www.brasildefato.com.br/2024/09/05/ministerio-da-justica-autoriza-tres-novas-terras-indigenas-apos-seis-anos-sem-demarcacao/',
    'https://revistacenarium.com.br/indigenas-turiwara-denunciam-ataques-armados-por-segurancas-da-empresa-agropalma-no-para/',
    'https://www.brasildefato.com.br/2024/09/08/banco-da-noruega-retira-investimento-em-empresa-de-seguranca-da-agropalma-por-violar-direitos-de-indigenas-do-para/',
    'https://g1.globo.com/pa/para/noticia/2024/09/17/comunidades-tradicionais-protestam-contra-instalacao-de-mineroduto-no-para.ghtml/',
    'https://g1.globo.com/pa/para/noticia/2024/09/24/indigenas-e-quilombolas-do-acara-protestam-contra-obra-de-mineradora-em-comunidades-tradicionais.ghtml/',
    'https://btmais.com.br/comunidades-do-vale-do-acara-protestam-em-belem/',
    'https://btmais.com.br/bbf-enfrenta-crise-financeira-diz-jornalista/',
    'https://oantagonico.net.br/a-agropalma-a-nova-invasao-os-quilombolas-indigenas-o-tj-e-a-reintegracao-imediata/',
    'https://btmais.com.br/segurancas-da-agropalma-conflito-com-indigenas-para/',
    'https://btmais.com.br/bbf-enfrenta-crise-financeira-diz-jornalista/',
    'https://ver-o-fato.com.br/manifesto-denuncia-hydro-e-uso-de-policia-contra-indigenas-e-quilombolas-no-vale-do-acara/',
    'https://ver-o-fato.com.br/urgente-pf-prende-parate-e-marques-tembe-investigados-por-crimes-no-vale-do-acara/',
    'https://almapreta.com.br/sessao/cotidiano/mobilizacao-indigena-impede-policia-de-impor-obra-de-multinacional-em-territorio-quilombola/',
    'https://www.agenciapara.com.br/noticia/53066/adepara-apresenta-politica-de-rastreabilidade-da-cadeia-do-dende-para-cooperativa-de-quilombolas-e-povos-originarios/',
    'https://ver-o-fato.com.br/exclusivo-tabarana-minha-familia-quer-das-5-herdeiras-da-agropalma-nossas-terras-volta/',
    'https://www.folhadoprogresso.com.br/exclusivo-herdeiro-de-terras-acusa-governador-e-irmao-de-favorecer-agropalma-1/',
    'https://www.theagribiz.com/empresas/a-venda-agropalma-traz-ex-monsanto-para-tirar-o-atraso/',
    'https://ver-o-fato.com.br/exclusivo-agropalma-perde-acao-contra-tabarana-e-justica-extingue-processo/',
    'https://dol.com.br/noticias/para/529208/decisao-judicial-garante-terras-a-agropalma?d=1/',
    'https://malungu.org/agropalma-e-seus-crimes-ambientais-contra-a-comunidade-quilombola-balsa/',
    'https://g1.globo.com/pa/para/noticia/2024/08/22/area-disputada-por-indigenas-e-empresa-agropalma-e-palco-de-conflito-violento-no-para.ghtml/',
    'https://anaind.org.br/noticias/area-disputada-por-indigenas-e-empresa-agropalma-e-palco-de-conflito-violento-no-para/',
    'https://g1.globo.com/pa/para/noticia/2023/08/23/conflito-do-dende-indigenas-denunciam-grande-buraco-cavado-por-empresa-no-para.ghtml/',
    'https://revistacenarium.com.br/indigenas-turiwara-denunciam-ataques-armados-por-segurancas-da-empresa-agropalma-no-para/',
    'https://www.salveafloresta.org/atualizacoes/11819/brasil-segurancas-da-agropalma-baleiam-indigenas/',
]

# Inicializa o navegador
driver = configurar_navegador()

# Lista para armazenar os dados e o status
dados = []
status_execucao = []  # Armazena o status de cada URLs

if driver:
    for i, url in enumerate(urls, start=1):
        print(f"Acessando {url}...")

        titulo, origem, conteudo = extrair_detalhes_pagina(url, driver)

        if conteudo:
            # Adiciona os dados extraídos na lista
            dados.append({
                'Número': i,
                'Título': titulo,
                'Origem': origem,
                'Texto Completo': conteudo
            })
            status_execucao.append([i, 'Sucesso'])
        else:
            status_execucao.append([i, 'Falha'])

        # Exibir a tabela atualizada no terminal
        print(tabulate(status_execucao, headers=["Nº da Notícia", "Status"], tablefmt="grid"))

        time.sleep(5)  # Espera 5 segundos entre requisições

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