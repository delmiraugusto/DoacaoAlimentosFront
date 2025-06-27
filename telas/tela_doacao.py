import tkinter as tk
import requests
from datetime import datetime
from tkinter import messagebox, simpledialog
from servicos import api

def abrir_tela():
    janela = tk.Toplevel()
    janela.title("Doação")
    janela.geometry("400x350")

    id_doacao_atual = None

    campos = ["doador_nome", "solicitante_nome", "descricao", "status", "dataDoacao", "data_recebimento"]
    entradas = {}

    tk.Label(janela, text="Doação", font=("Arial", 16, "bold")).pack(pady=10)

    for campo in campos:
        tk.Label(janela, text=campo).pack()
        entry = tk.Entry(janela, width=40)
        entry.pack()
        entradas[campo] = entry

    def buscar():
        global id_doacao_atual
        try:
            id_ = simpledialog.askstring("Buscar Doacao", "Informe o ID:")
            if not id_:
                return
            dados = api.get_por_id("doacoes", id_)
            id_doacao_atual = id_

            for campo in campos:
                entradas[campo].delete(0, tk.END)
                valor = dados.get(campo, "")
                entradas[campo].insert(0, "" if valor is None else str(valor))
        except requests.exceptions.HTTPError as e:
            erro = e.response.text
            messagebox.showerror("Erro: ", str(erro))

    def abrir_tela_cadastro():
        cadastro = tk.Toplevel()
        cadastro.title("Cadastrar Doacao")
        cadastro.geometry("400x500")

        tk.Label(cadastro, text="Cadastro de Doacao", font=("Arial", 14, "bold")).pack(pady=10)

        campos_cadastro = {
            "descricao": None,
            "status_id": None,
            "doador_id": None,
            "solicitante_id": None,
            "data_recebimento": None
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
                status_id = entradas_cadastro["status_id"].get()
                doador_id = entradas_cadastro["doador_id"].get()
                solicitante_id = entradas_cadastro["solicitante_id"].get()
                data_recebimento = entradas_cadastro["data_recebimento"].get()

                dados = {
                    "descricao": entradas_cadastro["descricao"].get(),
                    "status_id": int(status_id) if status_id else None,
                    "doador_id": int(doador_id) if doador_id else None,
                    "solicitante_id": int(solicitante_id) if solicitante_id else None
                }

                if data_recebimento.strip():
                    try:
                        datetime.strptime(data_recebimento, "%Y-%m-%d %H:%M:%S")
                        dados["data_recebimento"] = data_recebimento
                    except ValueError:
                        messagebox.showerror("Erro", "Data inválida. Use o formato: YYYY-MM-DD HH:MM:SS")
                        return

                res = api.post("doacoes", dados)
                messagebox.showinfo("Resposta da API", f'Id: {res["id"]}, {res["msg"]}')
                cadastro.destroy()

            except requests.exceptions.HTTPError as e:
                erro = e.response.text
                messagebox.showerror("Erro", str(erro))


        tk.Button(cadastro, text="Cadastrar", width=20, command=enviar_cadastro).pack(pady=10)

    def editar():
        global id_doacao_atual
        try:
            if not id_doacao_atual:
                id_doacao_atual = simpledialog.askstring("Editar Doacao", "Informe o ID:")
                if not id_doacao_atual:
                    return

            id_ = id_doacao_atual
            dados = {}

            for campo in campos:
                valor = entradas[campo].get().strip()

                if not valor:
                    continue

                if campo == "data_recebimento":
                    try:
                        datetime.strptime(valor, "%Y-%m-%d %H:%M:%S")
                        dados[campo] = valor
                    except ValueError:
                        messagebox.showerror("Erro", "Data inválida. Use o formato: YYYY-MM-DD HH:MM:SS")
                        return
                else:
                    dados[campo] = valor

            res = api.put("doacoes", id_, dados)
            messagebox.showinfo("Resposta da API", res["msg"])

        except requests.exceptions.HTTPError as e:
            erro = e.response.text
            messagebox.showerror("Erro: ", str(erro))

    def excluir():
        try:
            id_ = simpledialog.askstring("Excluir Doacao", "Informe o ID:")
            if not id_:
                return
            res = api.delete("doacoes", id_)
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
