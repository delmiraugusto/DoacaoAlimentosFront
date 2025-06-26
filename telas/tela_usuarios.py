import tkinter as tk
import requests
from tkinter import messagebox, simpledialog
from servicos import api

def abrir_tela():
    janela = tk.Toplevel()
    janela.title("Usuários")
    janela.geometry("400x350")

    campos = ["nome", "email", "telefone", "documento"]
    entradas = {}

    id_usuario_atual = None

    tk.Label(janela, text="Usuários", font=("Arial", 16, "bold")).pack(pady=10)

    for campo in campos:
        tk.Label(janela, text=campo.capitalize()).pack()
        entry = tk.Entry(janela, width=40)
        entry.pack()
        entradas[campo] = entry

    def buscar():
        global id_usuario_atual
        try:
            id_ = simpledialog.askstring("Buscar Usuário", "Informe o ID:")
            if not id_:
                return
            dados = api.get_por_id("usuarios", id_)
            id_usuario_atual = id_

            for campo in campos:
                entradas[campo].delete(0, tk.END)
                entradas[campo].insert(0, dados.get(campo, ""))
        except requests.exceptions.HTTPError as e:
            erro = e.response.text
            messagebox.showerror("Erro: ", str(erro))


    def abrir_tela_cadastro():
        cadastro = tk.Toplevel()
        cadastro.title("Cadastrar Usuário")
        cadastro.geometry("400x500")

        tk.Label(cadastro, text="Cadastro de Usuário", font=("Arial", 14, "bold")).pack(pady=10)

        campos_cadastro = {
            "nome": None,
            "email": None,
            "senha": None,
            "telefone": None,
            "documento": None,
            "perfil_id": None,
            "cep": None,
            "numero": None,
            "complemento": None
        }

        entradas_cadastro = {}

        for campo in campos_cadastro:
            label_text = campo.upper() if campo == "cep" else campo.capitalize()
            tk.Label(cadastro, text=label_text).pack()
            entrada = tk.Entry(cadastro, width=40)
            entrada.pack()
            entradas_cadastro[campo] = entrada

        def enviar_cadastro():
            try:
                perfil_id_str = entradas_cadastro["perfil_id"].get()
                numero_str = entradas_cadastro["numero"].get()
                complemento_str = entradas_cadastro["complemento"].get()

                dados = {
                    "nome": entradas_cadastro["nome"].get(),
                    "email": entradas_cadastro["email"].get(),
                    "senha": entradas_cadastro["senha"].get(),
                    "telefone": entradas_cadastro["telefone"].get(),
                    "documento": entradas_cadastro["documento"].get(),
                    "perfil_id": int(perfil_id_str) if perfil_id_str else None,
                    "numero": int(numero_str) if numero_str else None,
                    "complemento": int(complemento_str) if complemento_str else None,
                    "endereco": {
                        "cep": entradas_cadastro["cep"].get()
                    }
                }
                res = api.post("usuarios", dados)
                messagebox.showinfo("Resposta da API", res["msg"])
                cadastro.destroy()
            except requests.exceptions.HTTPError as e:
                erro = e.response.text
                messagebox.showerror("Erro: ", str(erro))


        tk.Button(cadastro, text="Cadastrar", width=20, command=enviar_cadastro).pack(pady=10)

    def editar():
        global id_usuario_atual
        try:
            if not id_usuario_atual:
                id_usuario_atual = simpledialog.askstring("Editar Usuário", "Informe o ID:")
                if not id_usuario_atual:
                    return

            id_ = id_usuario_atual
            dados = {k: entradas[k].get() for k in campos}
            res = api.put("usuarios", id_, dados)
            messagebox.showinfo("Resposta da API", res["msg"])
        except requests.exceptions.HTTPError as e:
            erro = e.response.text
            messagebox.showerror("Erro: ", str(erro))

    def excluir():
        try:
            id_ = simpledialog.askstring("Excluir Usuário", "Informe o ID:")
            if not id_:
                return
            res = api.delete("usuarios", id_)
            messagebox.showinfo("Sucesso", res["message"])
        except requests.exceptions.HTTPError as e:
            erro = e.response.text
            messagebox.showerror("Erro: ", str(erro))

    def limpar():
        for entrada in entradas.values():
            entrada.delete(0, tk.END)

    botoes_frame = tk.Frame(janela)
    botoes_frame.pack(pady=10)

    for texto, comando in [
        ("Buscar", buscar),
        ("Cadastrar", abrir_tela_cadastro),
        ("Editar", editar),
        ("Excluir", excluir)
    ]:
        tk.Button(botoes_frame, text=texto, width=10, command=comando).pack(side=tk.LEFT, padx=5)

    tk.Button(janela, text="Limpar", width=15, command=limpar).pack(pady=10)
