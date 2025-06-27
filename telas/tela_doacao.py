import tkinter as tk
import requests
from datetime import datetime
from tkinter import messagebox, simpledialog
from servicos import api
from tkinter import ttk

def abrir_tela():
    janela = tk.Toplevel()
    janela.title("Doação")
    janela.geometry("950x450")

    colunas = ["id", "doador_nome", "solicitante_nome", "descricao", "status", "dataDoacao", "data_recebimento"]

    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150)

    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    entry_edicao = {"widget": None}


    def listar_todos():
        try:
            for i in tree.get_children():
                tree.delete(i)
            doacoes = api.get("doacoes")
            for d in doacoes:
                tree.insert("", tk.END, values=(d["id"], d["doador_nome"], d["solicitante_nome"], d["descricao"], d["status_id"], d["dataDoacao"], d["data_recebimento"],))
        except requests.exceptions.HTTPError as e:
            messagebox.showerror("Erro", e.response.text)

    def buscar_por_id():
        try:
            id_ = simpledialog.askstring("Buscar Doacao", "Informe o ID:")
            if not id_:
                return

            for i in tree.get_children():
                tree.delete(i)

            dados = api.get_por_id("doacoes", id_)
            tree.insert("", tk.END, values=(id_, dados["doador_nome"], dados["solicitante_nome"], dados["descricao"], dados["status_id"], dados["dataDoacao"], dados["data_recebimento"]))

        except requests.exceptions.HTTPError as e:
            messagebox.showerror("Erro", e.response.text)

    def buscar_por_doador_id():
        try:
            id_ = simpledialog.askstring("Buscar Pelo Doador", "Informe o ID:")
            if not id_:
                return

            for i in tree.get_children():
                tree.delete(i)

            dados = api.get_por_id("doacoes/doador", id_)
            tree.insert("", tk.END, values=(id_, dados["descricao"], dados["status_id"], dados["dataDoacao"], dados["solicitante_nome"], dados["data_recebimento"]))

        except requests.exceptions.HTTPError as e:
            messagebox.showerror("Erro", e.response.text)

    def buscar_por_solicitante_id():
        try:
            id_ = simpledialog.askstring("Buscar Pelo Solicitante", "Informe o ID:")
            if not id_:
                return

            for i in tree.get_children():
                tree.delete(i)

            dados = api.get_por_id("doacoes/solicitante", id_)
            tree.insert("", tk.END, values=(id_, dados["descricao"], dados["status_id"], dados["dataDoacao"], dados["doador_nome"], dados["data_recebimento"]))

        except requests.exceptions.HTTPError as e:
            messagebox.showerror("Erro", e.response.text)

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
        if entry_edicao["widget"] is not None:
            entry_edicao["widget"].event_generate("<FocusOut>")

        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma doacao para editar.")
            return

        item_id = selecionado[0]
        valores = tree.item(item_id, "values")
        id_ = valores[0]
        doador_nome = valores[1]
        solicitante_nome = valores[2]
        status = valores[3]
        dataDoacao = valores[4]
        data_recebimento = valores[5]


        try:
            dados = {"doador_nome": doador_nome, "solicitante_nome": solicitante_nome, "status": status, "dataDoacao": dataDoacao, "data_recebimento": data_recebimento}
            res = api.put("doacoes", id_, dados)
            messagebox.showinfo("Sucesso", res["msg"])
        except requests.exceptions.HTTPError as e:
            messagebox.showerror("Erro", e.response.text)

        def editar_celula(event):
            item = tree.identify_row(event.y)
            coluna = tree.identify_column(event.x)
            if not item or coluna == "#1":
                return

            col_index = int(coluna[1:]) - 1
            x, y, largura, altura = tree.bbox(item, column=coluna)
            valor_atual = tree.item(item, "values")[col_index]

            tree.selection_set(item)

            entry = tk.Entry(janela)
            entry.place(x=x + tree.winfo_rootx() - janela.winfo_rootx(),
                        y=y + tree.winfo_rooty() - janela.winfo_rooty(),
                        width=largura, height=altura)
            entry.insert(0, valor_atual)
            entry.focus()

            entry_edicao["widget"] = entry

            def salvar_edicao(e=None):
                novo_valor = entry.get()
                valores = list(tree.item(item, "values"))
                valores[col_index] = novo_valor
                tree.item(item, values=valores)
                entry.destroy()
                entry_edicao["widget"] = None  

            entry.bind("<Return>", salvar_edicao)
            entry.bind("<FocusOut>", salvar_edicao)
        
        tree.bind("<Double-1>", editar_celula)


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
        for item in tree.get_children():
            tree.delete(item)

    botoes_frame = tk.Frame(janela)
    botoes_frame.pack(pady=10)

    for texto, comando in [
        ("Listar Todos", listar_todos),
        ("Buscar", buscar_por_id),
        ("Buscar por Doacoes doador", buscar_por_doador_id),
        ("Buscar por Doacoes solicitante", buscar_por_solicitante_id),
        ("Cadastrar", abrir_tela_cadastro),
        ("Editar", editar), 
        ("Excluir", excluir)
    ]:
        tk.Button(botoes_frame, text=texto, width=10, command=comando).pack(side=tk.LEFT, padx=5)

    tk.Button(janela, text="Limpar", width=15, command=limpar).pack(pady=10)
