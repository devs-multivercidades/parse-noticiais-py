import pandas as pd
import os
from fpdf import FPDF

# Carregar a planilha
caminho_planilha = r"C:\Users\Multivercidades T.I\Documents\resultados_scraping\noticias.xlsx"
df = pd.read_excel(caminho_planilha)

# Criar diretório de saída, se não existir
caminho_saida = r"C:\Users\Multivercidades T.I\Documents\resultados_scraping\PDFs Noticias"
os.makedirs(caminho_saida, exist_ok=True)


# Função para gerar o PDF
def criar_pdf(numero, ano, titulo, origem, texto, arquivo_nome):
    pdf = FPDF()
    pdf.add_page()

    # Adiciona a fonte FreeSerif (compatível com Unicode)
    pdf.add_font("FreeSerif", "", "FreeSerif.ttf", uni=True)
    pdf.set_font("FreeSerif", "", 16)

    # Título e formatação
    pdf.cell(0, 10, f"Número: {numero}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Ano: {ano}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Título: {titulo}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Origem: {origem}", new_x="LMARGIN", new_y="NEXT")

    # Conteúdo
    pdf.set_font("FreeSerif", "", 12)
    pdf.multi_cell(0, 10, f"Texto Completo:\n{texto}")

    # Salvar PDF
    pdf.output(os.path.join(caminho_saida, arquivo_nome))


# Iterar pelas primeiras 5 linhas da planilha e gerar PDFs
for index, row in df.head(5).iterrows():  # Limita a leitura para as primeiras 5 linhas
    numero = row['Número']
    ano = row['Ano']
    titulo = row['Título']
    origem = row['Origem']
    texto = row['Texto Completo']

    arquivo_nome = f"noticia_{numero}.pdf"
    criar_pdf(numero, ano, titulo, origem, texto, arquivo_nome)

print("PDFs criados para as 5 primeiras notícias!")