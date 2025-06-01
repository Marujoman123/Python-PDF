import os
import re
from PyPDF2 import PdfReader, PdfWriter
from tkinter import Tk, filedialog

# Oculta a janela principal do Tkinter
Tk().withdraw()

# Abre uma janela para o usuário selecionar um arquivo PDF
caminho_pdf_entrada = filedialog.askopenfilename(
    title="Selecione o arquivo PDF",
    filetypes=[("Arquivos PDF", "*.pdf")]
)

# Verifica se o usuário selecionou um arquivo
if caminho_pdf_entrada:
    leitor = PdfReader(caminho_pdf_entrada)

    # Cria a subpasta "A Cobrar" para salvar os novos PDFs
    pasta_origem = os.path.dirname(caminho_pdf_entrada)
    pasta_destino = os.path.join(pasta_origem, "A Cobrar")
    os.makedirs(pasta_destino, exist_ok=True)

    escritor_atual = None
    nome_arquivo_atual = None
    contador_pdfs = 0  # Contador de arquivos exportados

    for i, pagina in enumerate(leitor.pages):
        texto_pagina = pagina.extract_text() or ""

        # Procura o nome da empresa entre "Razão Social" e "CNPJ"
        match = re.search(r"Raz[aã]o Social\s*[:\-]?\s*(.*?)\s*CNPJ", texto_pagina, re.IGNORECASE | re.DOTALL)
        nova_empresa = False

        if match:
            nome_empresa = match.group(1)
            nome_empresa = re.sub(r'\s+', ' ', nome_empresa).strip()
            nome_empresa = re.sub(r'[\\/*?:"<>|]', "_", nome_empresa)
            nome_arquivo_atual = os.path.join(pasta_destino, f"{nome_empresa}.pdf")
            escritor_atual = PdfWriter()
            nova_empresa = True

        if escritor_atual:
            escritor_atual.add_page(pagina)

        if nova_empresa:
            print(f"Página {i+1} iniciando novo arquivo: {os.path.basename(nome_arquivo_atual)}")
        else:
            print(f"Página {i+1} anexada a: {os.path.basename(nome_arquivo_atual) if nome_arquivo_atual else 'NENHUM'}")

        # Verifica se estamos na última página do arquivo
        proxima_pagina_existe = (i + 1) < len(leitor.pages)

        # Se for a última página, salva o arquivo atual
        if not proxima_pagina_existe:
            if nome_arquivo_atual and escritor_atual:
                with open(nome_arquivo_atual, "wb") as saida_pdf:
                    escritor_atual.write(saida_pdf)
                    contador_pdfs += 1  # Incrementa o contador

        # Se a próxima página for de uma nova empresa, salva o arquivo atual
        elif proxima_pagina_existe:
            texto_proxima = leitor.pages[i + 1].extract_text() or ""
            match_proxima = re.search(r"Raz[aã]o Social\s*[:\-]?\s*(.*?)\s*CNPJ", texto_proxima, re.IGNORECASE | re.DOTALL)

            if match_proxima and nome_arquivo_atual and escritor_atual:
                with open(nome_arquivo_atual, "wb") as saida_pdf:
                    escritor_atual.write(saida_pdf)
                    contador_pdfs += 1  # Incrementa o contador

    # Mostra o total de arquivos gerados
    print(f"\n✅ {contador_pdfs} arquivos PDF exportados com sucesso para: {pasta_destino}")
else:
    print("Nenhum arquivo selecionado.")
