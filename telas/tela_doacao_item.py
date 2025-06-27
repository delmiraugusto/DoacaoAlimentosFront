import tkinter as tk
import requests
from datetime import datetime
from tkinter import messagebox, simpledialog
from servicos import api

def abrir_tela():
    janela = tk.Toplevel()
    janela.title("Doação Item")
    janela.geometry("400x350")

    id_doacaoItem_atual = None

    campos = ["doacao_id", "alimento_id", "quantidade", "data_vencimento"]
    entradas = {}

    tk.Label(janela, text="Doação Item", font=("Arial", 16, "bold")).pack(pady=10)

    for campo in campos:
        tk.Label(janela, text=campo).pack()
        entry = tk.Entry(janela, width=40)
        entry.pack()
        entradas[campo] = entry

    def buscar():
        global id_doacaoItem_atual
        try:
            id_ = simpledialog.askstring("Buscar Doacao Item", "Informe o ID:")
            if not id_:
                return
            dados = api.get_por_id("doacoesItens", id_)
            id_doacaoItem_atual = id_

            for campo in campos:
                entradas[campo].delete(0, tk.END)
                valor = dados.get(campo, "")
                entradas[campo].insert(0, "" if valor is None else str(valor))
        except requests.exceptions.HTTPError as e:
            erro = e.response.text
            messagebox.showerror("Erro: ", str(erro))


    def abrir_tela_cadastro():
        cadastro = tk.Toplevel()
        cadastro.title("Cadastrar Doacao Item")
        cadastro.geometry("400x500")

        tk.Label(cadastro, text="Cadastro de Doacao Item", font=("Arial", 14, "bold")).pack(pady=10)

        campos_cadastro = {
            "doacao_id": None,
            "alimento_id": None,
            "quantidade": None,
            "data_vencimento": None
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
                doacao_id = entradas_cadastro["doacao_id"].get()
                alimento_id = entradas_cadastro["alimento_id"].get()
                data_vencimento = entradas_cadastro["data_vencimento"].get()
                quantidade = entradas_cadastro["quantidade"].get().strip()


                dados = {
                    "doacao_id": int(doacao_id) if doacao_id else None,
                    "alimento_id": int(alimento_id) if alimento_id else None,
                    "quantidade": int(quantidade),
                }

                if data_vencimento.strip():
                    try:
                        datetime.strptime(data_vencimento, "%Y-%m-%d")
                        dados["data_vencimento"] = data_vencimento
                    except ValueError:
                        messagebox.showerror("Erro", "Data inválida. Use o formato: YYYY-MM-DD")
                        return

                res = api.post("doacoesItens", dados)
                messagebox.showinfo("Resposta da API", f'Id: {res["id"]}, {res["msg"]}')
                cadastro.destroy()

            except requests.exceptions.HTTPError as e:
                erro = e.response.text
                messagebox.showerror("Erro", str(erro))


        tk.Button(cadastro, text="Cadastrar", width=20, command=enviar_cadastro).pack(pady=10)

    def editar():
        global id_doacaoItem_atual
        try:
            if not id_doacaoItem_atual:
                id_doacaoItem_atual = simpledialog.askstring("Editar Doacao Item", "Informe o ID:")
                if not id_doacaoItem_atual:
                    return

            id_ = id_doacaoItem_atual
            dados = {}

            for campo in campos:
                valor = entradas[campo].get().strip()

                if not valor:
                    continue

                if campo == "data_vencimento":
                    try:
                        datetime.strptime(valor, "%Y-%m-%d")
                        dados[campo] = valor
                    except ValueError:
                        messagebox.showerror("Erro", "Data inválida. Use o formato: YYYY-MM-DD")
                        return
                else:
                    dados[campo] = valor

            res = api.put("doacoesItens", id_, dados)
            messagebox.showinfo("Resposta da API", res["msg"])

        except requests.exceptions.HTTPError as e:
            erro = e.response.text
            messagebox.showerror("Erro: ", str(erro))

    def excluir():
        try:
            id_ = simpledialog.askstring("Excluir Doacao Item", "Informe o ID:")
            if not id_:
                return
            res = api.delete("doacoesItens", id_)
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
