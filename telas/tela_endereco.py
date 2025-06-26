import tkinter as tk
import requests
from tkinter import messagebox, simpledialog
from servicos import api

def abrir_tela():
    janela = tk.Toplevel()
    janela.title("Endereço")
    janela.geometry("400x400")

    campos = ["cep", "logradouro", "bairro", "uf", "cidade"]
    entradas = {}

    id_endereco_atual = None

    tk.Label(janela, text="Endereço", font=("Arial", 16, "bold")).pack(pady=10)

    for campo in campos:
        tk.Label(janela, text=campo.capitalize()).pack()
        entry = tk.Entry(janela, width=40)
        entry.pack()
        entradas[campo] = entry

    def buscar():
        global id_endereco_atual
        try:
            id_ = simpledialog.askstring("Buscar Endereco", "Informe o ID:")
            if not id_:
                return
                        
            dados = api.get_por_id("enderecos", id_)
            id_endereco_atual = id_

            for campo in campos:
                entradas[campo].delete(0, tk.END)
                entradas[campo].insert(0, dados.get(campo, ""))
        except requests.exceptions.HTTPError as e:
            erro = e.response.text
            messagebox.showerror("Erro: ", str(erro))

    def abrir_tela_cadastro():
        cadastro = tk.Toplevel()
        cadastro.title("Cadastrar Endereco")
        cadastro.geometry("400x500")

        tk.Label(cadastro, text="Cadastro de Endereco", font=("Arial", 14, "bold")).pack(pady=10)

        campos_cadastro = {
            "cep": None,
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
                    "cep": entradas_cadastro["cep"].get()
                }
                res = api.post("enderecos", dados)
                messagebox.showinfo("Resposta da API", f'Id: {res["id"]}, {res["msg"]}')
                cadastro.destroy()
            except requests.exceptions.HTTPError as e:
                erro = e.response.text
                messagebox.showerror("Erro: ", str(erro))

        tk.Button(cadastro, text="Cadastrar", width=20, command=enviar_cadastro).pack(pady=10)

    def editar():
        global id_endereco_atual
        try:
            if not id_endereco_atual:
                id_endereco_atual = simpledialog.askstring("Editar Endereco", "Informe o ID:")
                if not id_endereco_atual:
                    return
                
            id_ = id_endereco_atual
            dados = {
                "cep": entradas["cep"].get()
            }
            res = api.put("enderecos", id_, dados)
            messagebox.showinfo("Resposta da API", res["msg"])
        except requests.exceptions.HTTPError as e:
            erro = e.response.text
            messagebox.showerror("Erro: ", str(erro))

    def excluir():
        try:
            id_ = simpledialog.askstring("Excluir Endereco", "Informe o ID:")
            if not id_:
                return
            res = api.delete("enderecos", id_)
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
        
        
        tk.Button(botoes_frame, text=texto, width=10, command=comando).pack(side=tk.LEFT, padx=5, pady=2)

    tk.Button(janela, text="Limpar", width=15, command=limpar).pack(pady=10)
