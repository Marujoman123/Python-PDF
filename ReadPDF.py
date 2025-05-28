#pip install PyPDF2 pillow
#pip install PyPDF2 fpdf

from tkinter import Tk, filedialog
from PyPDF2 import PdfReader
from fpdf import FPDF
import os

def extrair_texto_pdf(caminho_pdf):
    """Extrai o texto de todas as páginas de um arquivo PDF."""
    try:
        leitor = PdfReader(caminho_pdf)
        texto = ""
        
        # Loop pelas páginas para extrair o texto
        for pagina in leitor.pages:
            texto += pagina.extract_text() + "\n"
        
        return texto
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {e}")
        return None

def criar_pdf_editavel(texto, caminho_saida):
    """Cria um novo PDF editável com o texto extraído."""
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Adiciona o texto ao PDF linha por linha
        linhas = texto.split("\n")
        for linha in linhas:
            pdf.multi_cell(0, 10, linha)  # Adiciona uma célula de texto com quebra automática
        
        # Salva o PDF no caminho de saída
        pdf.output(caminho_saida)
        print(f"PDF editável com texto transcrito salvo em: {caminho_saida}")
    except Exception as e:
        print(f"Erro ao criar PDF editável: {e}")

def selecionar_arquivo():
    """Abre uma janela para o usuário selecionar um arquivo PDF."""
    # Oculta a janela raiz do Tkinter
    root = Tk()
    root.withdraw()
    
    # Abre a janela de seleção de arquivo
    caminho_pdf = filedialog.askopenfilename(
        title="Selecione um arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    
    return caminho_pdf

if __name__ == "__main__":
    # Seleciona o arquivo PDF
    caminho_pdf = selecionar_arquivo()
    
    if caminho_pdf:  # Verifica se o usuário selecionou um arquivo
        texto_extraido = extrair_texto_pdf(caminho_pdf)
        
        if texto_extraido:
            # Define o caminho do novo PDF
            caminho, nome_arquivo = os.path.split(caminho_pdf)
            nome_base, _ = os.path.splitext(nome_arquivo)
            caminho_saida = os.path.join(caminho, f"{nome_base}-Transcrito.pdf")
            
            # Cria o PDF editável com o texto transcrito
            criar_pdf_editavel(texto_extraido, caminho_saida)
    else:
        print("Nenhum arquivo foi selecionado.")
