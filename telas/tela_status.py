import tkinter as tk
import requests
from tkinter import messagebox, simpledialog
from servicos import api

def abrir_tela():
    janela = tk.Toplevel()
    janela.title("Status")
    janela.geometry("400x350")

    campos = ["nome"]
    entradas = {}

    id_status_atual = None

    tk.Label(janela, text="Status", font=("Arial", 16, "bold")).pack(pady=10)

    for campo in campos:
        tk.Label(janela, text=campo.capitalize()).pack()
        entry = tk.Entry(janela, width=40)
        entry.pack()
        entradas[campo] = entry

    def buscar():
        global id_status_atual
        try:
            id_ = simpledialog.askstring("Buscar Status", "Informe o ID:")
            dados = api.get_por_id("status", id_)
            id_status_atual = id_
            entradas["nome"].delete(0, tk.END)
            entradas["nome"].insert(0, dados.get("nome", ""))
        except requests.exceptions.HTTPError as e:
            erro = e.response.text
            messagebox.showerror("Erro: ", str(erro))

    def abrir_tela_cadastro():
        cadastro = tk.Toplevel()
        cadastro.title("Cadastrar Status")
        cadastro.geometry("400x500")

        tk.Label(cadastro, text="Cadastro de Status", font=("Arial", 14, "bold")).pack(pady=10)

        campos_cadastro = {
            "nome": None,
        }

        entradas_cadastro = {}

        for campo in campos_cadastro:
            label_text = campo.capitalize()
            tk.Label(cadastro, text=label_text).pack()
            entrada = tk.Entry(cadastro, width=40)
            entrada.pack()
            entradas_cadastro[campo] = entrada

        def enviar_cadastro():
            try:
                dados = {
                    "nome": entradas_cadastro["nome"].get(),
                }
                res = api.post("status", dados)
                messagebox.showinfo("Resposta da API", res["msg"])
                cadastro.destroy()
            except requests.exceptions.HTTPError as e:
                erro = e.response.text
                messagebox.showerror("Erro: ", str(erro))

        tk.Button(cadastro, text="Cadastrar", width=20, command=enviar_cadastro).pack(pady=10)


    def editar():
        global id_status_atual
        try:
            if not id_status_atual:
                id_status_atual = simpledialog.askstring("Editar Status", "Informe o ID:")
                if not id_status_atual:
                    return
                
            id_ = id_status_atual
            dados = {k: entradas[k].get() for k in campos}
            res = api.put("status", id_, dados)
            messagebox.showinfo("Resposta da API", res["msg"])
        except requests.exceptions.HTTPError as e:
            erro = e.response.text
            messagebox.showerror("Erro: ", str(erro))

    def excluir():
        try:
            id_ = simpledialog.askstring("Excluir Status", "Informe o ID:")
            if not id_:
                return
            res = api.delete("status", id_)
            messagebox.showinfo("Sucesso", res["message"])
        except requests.exceptions.HTTPError as e:
            erro = e.response.text
            messagebox.showerror("Erro: ", str(erro))

    def limpar():
        entradas["nome"].delete(0, tk.END)

    botoes_frame = tk.Frame(janela)
    botoes_frame.pack(pady=10)


    for texto, comando in [
        ("Buscar", buscar),
        ("Cadastrar", abrir_tela_cadastro),
        ("Editar", editar),
        ("Excluir", excluir)
    ]:
        tk.Button(botoes_frame, text=texto, width=10, command=comando).pack(side=tk.LEFT, padx=5, pady=2)

    tk.Button(janela, text="Limpar", width=15, command=limpar).pack(pady=10)
