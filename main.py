import tkinter as tk
from telas import (
    tela_usuarios, tela_alimentos, tela_endereco,
    tela_status, tela_doacao, tela_doacao_item, tela_perfil
)

def iniciar():
    root = tk.Tk()
    root.title("Doação de Alimentos")
    root.geometry("950x450")

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

    frame_botoes = tk.Frame(root)
    frame_botoes.pack()

    for i, (texto, comando) in enumerate(botoes):
        linha = 0 if i < 4 else 1
        coluna = i if i < 4 else i - 4
        btn = tk.Button(frame_botoes, text=texto, width=15, command=comando)
        btn.grid(row=linha, column=coluna, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    iniciar()

# Para Ativar a venv: .\venv\Scripts\Activate.ps1  

# Para rodar: python main.py