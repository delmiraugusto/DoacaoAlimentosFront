import tkinter as tk
import requests
from tkinter import messagebox, simpledialog
from servicos import api
from tkinter import ttk

def abrir_tela():
    janela = tk.Toplevel()
    janela.title("Endereço")
    janela.geometry("950x450")

    colunas = ["id", "cep", "logradouro", "bairro", "uf", "cidade"]

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
            enderecos = api.get("enderecos")
            for end in enderecos:
                tree.insert("", tk.END, values=(end["id"], end["cep"], end["logradouro"], end["bairro"], end["uf"], end["cidade"]))
        except requests.exceptions.HTTPError as e:
            messagebox.showerror("Erro", e.response.text)

    def buscar_por_id():
        try:
            id_ = simpledialog.askstring("Buscar Endereco", "Informe o ID:")
            if not id_:
                return

            for i in tree.get_children():
                tree.delete(i)

            dados = api.get_por_id("endereco", id_)
            tree.insert("", tk.END, values=(id_, dados["cep"], dados["logradouro"], dados["bairro"], dados["uf"], dados["cidade"]))

        except requests.exceptions.HTTPError as e:
            messagebox.showerror("Erro", e.response.text)

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
        if entry_edicao["widget"] is not None:
            entry_edicao["widget"].event_generate("<FocusOut>")

        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um endereco para editar.")
            return

        item_id = selecionado[0]
        valores = tree.item(item_id, "values")
        id_ = valores[0]
        cep = valores[1]

        try:
            dados = {"cep": cep}
            res = api.put("enderecos", id_, dados)
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
            id_ = simpledialog.askstring("Excluir Endereco", "Informe o ID:")
            if not id_:
                return
            res = api.delete("enderecos", id_)
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
        ("Cadastrar", abrir_tela_cadastro),
        ("Editar", editar),
        ("Excluir", excluir)
    ]:
        
        
        tk.Button(botoes_frame, text=texto, width=10, command=comando).pack(side=tk.LEFT, padx=5, pady=2)

    tk.Button(janela, text="Limpar", width=15, command=limpar).pack(pady=10)
