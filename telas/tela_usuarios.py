import tkinter as tk
import requests
from tkinter import messagebox, simpledialog
from servicos import api
from tkinter import ttk

def abrir_tela():
    janela = tk.Toplevel()
    janela.title("Usuários")
    janela.geometry("950x450")

    colunas = ["nome", "email", "telefone", "documento"]

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
            usuarios = api.get("usuarios")
            for usuario in usuarios:
                tree.insert("", tk.END, values=(usuario["id"], usuario["nome"], usuario["email"], usuario["telefone"], usuario["documento"],))
        except requests.exceptions.HTTPError as e:
            messagebox.showerror("Erro", e.response.text)

    def buscar_por_id():
        try:
            id_ = simpledialog.askstring("Buscar Usuario", "Informe o ID:")
            if not id_:
                return

            for i in tree.get_children():
                tree.delete(i)

            dados = api.get_por_id("usuarios", id_)
            tree.insert("", tk.END, values=(id_, dados["nome"], dados["email"], dados["telefone"], dados["documento"]))

        except requests.exceptions.HTTPError as e:
            messagebox.showerror("Erro", e.response.text)


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
            messagebox.showwarning("Aviso", "Selecione um usuario para editar.")
            return

        item_id = selecionado[0]
        valores = tree.item(item_id, "values")
        id_ = valores[0]
        nome = valores[1]
        email = valores[2]
        telefone = valores[2]
        documento = valores[2]

        try:
            dados = {"nome": nome, "email": email, "telefone": telefone, "documento": documento}
            res = api.put("usuarios", id_, dados)
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
            id_ = simpledialog.askstring("Excluir Usuário", "Informe o ID:")
            if not id_:
                return
            res = api.delete("usuarios", id_)
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
        tk.Button(botoes_frame, text=texto, width=10, command=comando).pack(side=tk.LEFT, padx=5)

    tk.Button(janela, text="Limpar", width=15, command=limpar).pack(pady=10)
