import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Caminho do arquivo Excel
file_path = r'C:\Users\Multivercidades T.I\Documents\resultados_scraping\noticias.xlsx'

# Carregar o arquivo Excel
df = pd.read_excel(file_path)

# Converter a coluna 'Ano' para numérico, ignorando valores não numéricos (erros)
df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce')

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

# Filtrar o DataFrame para o período de 2010 a 2021
df_periodo = df[(df['Ano'] >= 2010) & (df['Ano'] <= 2021)]

# Concatenar todos os textos do período em uma única string
textos_periodo = " ".join(df_periodo['Texto Completo'].dropna().astype(str))

# Gerar a nuvem de palavras para o período
nuvem_palavras = WordCloud(width=800, height=400, background_color='white',
                           max_words=100, stopwords=stopwords).generate(textos_periodo)

# Configurar a figura e adicionar título
plt.figure(figsize=(12, 6))
plt.imshow(nuvem_palavras, interpolation='bilinear')
plt.axis('off')
plt.title("Nuvem de Palavras - Período 2010 a 2021", fontsize=24, weight='bold')

# Salvar a nuvem de palavras como PNG
output_path = r'C:\Users\Multivercidades T.I\Documents\resultados_scraping\nuvem_palavras_2010_2021.png'
plt.savefig(output_path, format='png', bbox_inches='tight')
plt.close()