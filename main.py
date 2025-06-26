import tkinter as tk
from telas import (
    tela_usuarios, tela_alimentos, tela_endereco,
    tela_status, tela_doacao, tela_doacao_item, tela_perfil
)

def iniciar():
    root = tk.Tk()
    root.title("Doação de Alimentos")
    root.geometry("500x400")

    tk.Label(root, text="Doação de Alimentos", font=("Arial", 20, "bold")).pack(pady=20)

    botoes = [
        ("Usuários", tela_usuarios.abrir_tela),
        ("Alimentos", tela_alimentos.abrir_tela),
        ("Endereço", tela_endereco.abrir_tela),
        ("Status", tela_status.abrir_tela),
        ("Perfil", tela_perfil.abrir_tela),
        ("Doação", tela_doacao.abrir_tela),
        ("DoacaoItem", tela_doacao_item.abrir_tela)
    ]

    for texto, comando in botoes:
        tk.Button(root, text=texto, width=20, command=comando).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    iniciar()
