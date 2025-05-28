#Formatos suportados para seleção estão definidos no parâmetro filetypes, como .png, .jpg, .jpeg.
#pip install pillow

from PIL import Image
import os
from tkinter import Tk, filedialog

def imagem_para_pdf(caminho_imagem):
    try:
        # Abre a imagem
        imagem = Image.open(caminho_imagem)
        
        # Converte a imagem para modo RGB (caso seja necessário, como no caso de PNG com transparência)
        if imagem.mode in ("RGBA", "P"):  # Verifica se não está em RGB
            imagem = imagem.convert("RGB")
        
        # Extrai o caminho, nome base e extensão do arquivo
        caminho, nome_arquivo = os.path.split(caminho_imagem)
        nome_base, _ = os.path.splitext(nome_arquivo)
        
        # Define o nome do arquivo PDF de saída
        caminho_pdf = os.path.join(caminho, f"{nome_base}-PDF.pdf")
        
        # Salva a imagem no formato PDF
        imagem.save(caminho_pdf, "PDF", resolution=100.0)
        
        print(f"Arquivo PDF salvo em: {caminho_pdf}")
    except Exception as e:
        print(f"Erro ao converter a imagem para PDF: {e}")

def selecionar_arquivo():
    # Oculta a janela raiz do Tkinter
    root = Tk()
    root.withdraw()
    
    # Abre a janela para selecionar o arquivo de imagem
    caminho_imagem = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.gif")]
    )
    
    return caminho_imagem

if __name__ == "__main__":
    # Seleciona o arquivo de imagem
    caminho_imagem = selecionar_arquivo()
    
    if caminho_imagem:  # Verifica se o usuário selecionou um arquivo
        imagem_para_pdf(caminho_imagem)
    else:
        print("Nenhum arquivo foi selecionado.")



