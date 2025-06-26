# pip install PyPDF2

import os
from tkinter import Tk, filedialog
from PyPDF2 import PdfMerger

def unificar_pdfs(caminhos_pdfs, caminho_saida):
    try:
        # Instancia o objeto PdfMerger
        merger = PdfMerger()

        # Adiciona cada arquivo PDF ao PdfMerger
        for caminho_pdf in caminhos_pdfs:
            merger.append(caminho_pdf)
        
        # Salva o arquivo PDF unificado
        merger.write(caminho_saida)
        merger.close()

        print(f"Arquivo PDF unificado salvo em: {caminho_saida}")
    except Exception as e:
        print(f"Erro ao unificar os arquivos PDF: {e}")

def selecionar_arquivos():
    # Oculta a janela raiz do Tkinter
    root = Tk()
    root.withdraw()

    # Abre a janela para selecionar múltiplos arquivos PDF
    caminhos_pdfs = filedialog.askopenfilenames(
        title="Selecione arquivos PDF para unificar",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    return caminhos_pdfs

if __name__ == "__main__":
    # Seleciona os arquivos PDF
    caminhos_pdfs = selecionar_arquivos()
    if caminhos_pdfs:  # Verifica se o usuário selecionou pelo menos um arquivo
        # Define o caminho do arquivo de saída
        pasta_saida = os.path.dirname(caminhos_pdfs[0])
        caminho_saida = os.path.join(pasta_saida, "PDF_Unificado.pdf")

        # Unifica os arquivos PDF
        unificar_pdfs(caminhos_pdfs, caminho_saida)
    else:
        print("Nenhum arquivo foi selecionado.")