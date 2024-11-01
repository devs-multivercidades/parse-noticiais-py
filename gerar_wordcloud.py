# Instale as bibliotecas necessárias (se ainda não tiver)
# !pip install pandas wordcloud matplotlib openpyxl

import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Caminho do arquivo Excel
file_path = r'C:\Users\Multivercidades T.I\Documents\resultados_scraping\noticias.xlsx'

# Carregar o arquivo Excel
df = pd.read_excel(file_path)

# Definir stopwords em português com adição de palavras específicas
stopwords = set(STOPWORDS)
stopwords.update([
    # Conectivos, advérbios, preposições, etc.
    "a", "o", "e", "de", "da", "do", "em", "para", "com", "não", "um", "uma",
    "os", "as", "ao", "dos", "das", "por", "na", "no", "que", "se", "mais",
    "já", "são", "também", "sua", "ou", "como", "mas", "há", "nos", "entre",
    "quando", "sobre", "muito", "ser", "foi", "pelo", "pela", "até", "após",
    "nosso", "sua", "esse", "essa", "aquele", "aquela", "está", "fazer",
    "tem", "ter", "estão", "vai", "vão", "será", "diz", "disse", "porque",
    "tinha", "têm", "sou", "era", "onde", "quem", "pode", "podem", "todas",
    "todos", "cada", "ele", "ela", "eles", "elas", "isso", "isto", "aquilo",
    "!", "?", "é", "era", "deve", "dever", "poder", "quero", "quere",
    "vamos", "vou", "sim", "não", "porém", "assim", "pois", "então", "deste",
    "destes", "desse", "desse", "destas", "neste", "nesta", "aquele", "aqueles",
    "daqueles", "daquele", "isso", "nisso", "dessas", "porém", "porquê",
    "aos", "aqui", "sendo", "qualquer", "ver", "sem", "nós", "além", "cerca",
    "mesmo", "seu", "só", "sómente", "tambem", "nela", "nele", "neles", "nelas",
    "você", "vocês", "algum", "alguma", "alguns", "algumas", "cada", "todo",
    "tudo", "aquela", "aqueles", "aquelas", "deles", "delas", "seus", "suas",
    "tal", "tais", "bem", "muito", "pouco", "menos", "mais", "nosso", "nossa",
    "meu", "minha", "teu", "tua", "dele", "dela",
    # Novas palavras identificadas e sinônimos
    "esses", "dar", "lançou", "este", "eram", "tinham", "foram", "ocorreu",
    "pelos", "estavam", "tornar", "nesse", "nessa", "nossas", "sejam", "poderia",
    "devem", "irá", "serão", "eram", "foram", "ocorrido", "fez", "após",
    "houve", "tornou", "houvesse", "colocado", "realizou", "realizados", "destes",
    "estas", "fizeram", "fará", "realizar", "tornar-se", "foram", "estiveram",
    "vem", "poder", "daria", "vai", "ainda", "irá", "mantêm", "levou", "colocar",
    "tendo", "deixou", "chegou", "aquelas", "nela", "haveria", "deixou", "tivesse"
])

# Obter os anos únicos na coluna "Ano"
anos_disponiveis = df['Ano'].dropna().unique()

# Filtrar e gerar nuvem de palavras para cada ano
for ano in anos_disponiveis:
    # Filtrar o DataFrame para o ano específico
    textos_ano = df[df['Ano'] == ano]['Texto Completo'].dropna()

    # Concatenar os textos do ano em uma única string
    textos = " ".join(textos_ano.astype(str))

    # Gerar a nuvem de palavras para o ano
    nuvem_palavras = WordCloud(width=800, height=400, background_color='white',
                               max_words=100, stopwords=stopwords).generate(textos)

    # Configurar a figura e adicionar título
    plt.figure(figsize=(12, 6))
    plt.imshow(nuvem_palavras, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"Nuvem de Palavras - Ano {ano}", fontsize=24, weight='bold')

    # Salvar a nuvem de palavras como PNG com o título no topo
    output_path = f'C:\\Users\\Multivercidades T.I\\Documents\\resultados_scraping\\nuvem_palavras_{ano}.png'
    plt.savefig(output_path, format='png', bbox_inches='tight')
    plt.close()