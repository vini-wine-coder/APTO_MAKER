import customtkinter as ctk
from tkinter import filedialog
import os
import subprocess
import core


def abrir_pasta(caminho_arquivo):
    """
    Abre a pasta que contem o arquivo gerado, no gerenciador de arquivos
    padrao do sistema.

    LINUX (atual): usa xdg-open na pasta.
    WINDOWS (quando trocar): troque o corpo desta funcao por
        os.startfile(pasta)
    """
    pasta = os.path.dirname(os.path.abspath(caminho_arquivo))
    try:
        subprocess.Popen(["xdg-open", pasta])
    except FileNotFoundError:
        pass


def iniciar():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    janela = ctk.CTk()
    janela.title("APTO Maker")
    janela.geometry("600x450")

    label_texto = ctk.CTkLabel(janela, text="Sequência APTO (uma por linha):")
    label_texto.pack(padx=20, pady=(20, 5), anchor="w")

    caixa_texto = ctk.CTkTextbox(janela, width=560, height=250)
    caixa_texto.pack(padx=20, pady=5, fill="both", expand=True)

    label_caminho = ctk.CTkLabel(janela, text="Nenhum arquivo selecionado ainda.")
    label_caminho.pack(padx=20, pady=(10, 0), anchor="w")

    estado = {"caminho_saida": None}

    def escolher_caminho():
        caminho = filedialog.asksaveasfilename(
            defaultextension=".dxf",
            filetypes=[("Arquivo DXF", "*.dxf")],
            title="Salvar DXF como...",
        )
        if caminho:
            estado["caminho_saida"] = caminho
            label_caminho.configure(text=caminho)

    frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
    frame_botoes.pack(padx=20, pady=15, fill="x")

    botao_salvar_como = ctk.CTkButton(frame_botoes, text="Salvar como...", command=escolher_caminho)
    botao_salvar_como.pack(side="left", padx=(0, 10))

    label_status = ctk.CTkLabel(janela, text="")

    def gerar():
        texto = caixa_texto.get("1.0", "end").strip()

        if not texto:
            label_status.configure(text="Digite a sequência de APTOs primeiro.", text_color="orange")
            return

        if not estado["caminho_saida"]:
            label_status.configure(text="Escolha onde salvar antes de gerar.", text_color="orange")
            return

        try:
            resultado = core.gerar_dxf(texto, estado["caminho_saida"])
        except Exception as e:
            label_status.configure(text=f"Erro: {e}", text_color="red")
            return

        label_status.configure(
            text=(
                f"OK: {resultado['total']} apartamentos, "
                f"{resultado['folhas']} folha(s) -> {resultado['caminho']}"
            ),
            text_color="green",
        )
        abrir_pasta(resultado["caminho"])

    botao_gerar = ctk.CTkButton(frame_botoes, text="Gerar DXF", command=gerar)
    botao_gerar.pack(side="left")

    label_status.pack(padx=20, pady=(0, 15), anchor="w")

    janela.mainloop()


if __name__ == "__main__":
    iniciar()
