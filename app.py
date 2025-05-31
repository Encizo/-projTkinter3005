import os
import json
import regex as re
from tkinter import *
from tkinter import ttk, messagebox


# Validação de nome/sobrenome
def valida_campo(campo, tipo_campo):
    if not campo:
        messagebox.showwarning('Aviso', f'{tipo_campo} inválido.')
        return False
    if len(campo) > 50:
        messagebox.showwarning('Aviso', f'{tipo_campo} muito longo. Máximo 50 caracteres.')
        return False

    pattern = r'^[\p{L}\s]{1,50}$'
    if not re.match(pattern, campo):
        messagebox.showwarning('Aviso', f'{tipo_campo} inválido. Evite números e símbolos.')
        return False

    preposicoes = ['da', 'de', 'do', 'das', 'dos']
    campo = ' '.join([parte.capitalize() if parte not in preposicoes else parte for parte in re.sub(r'\s+', ' ', campo).strip().split()])
    return campo


def grava_dados_arquivo(pessoa):
    arquivo_json = "cadastro.json"
    dados = []
    if os.path.exists(arquivo_json) and os.path.getsize(arquivo_json) > 0:
        with open(arquivo_json, 'r') as arquivo:
            dados = json.load(arquivo)
    dados.append(pessoa)
    with open(arquivo_json, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)


def carregar_dados_arquivo():
    arquivo_json = "cadastro.json"
    if os.path.exists(arquivo_json) and os.path.getsize(arquivo_json) > 0:
        with open(arquivo_json, 'r') as arquivo:
            return [(linha['nome'], linha['sobrenome'], linha['genero']) for linha in json.load(arquivo)]
    return []


def configurar_app():
    app.title('Cadastro de Pessoas')
    app.geometry('1024x600')
    app.configure(background='#F8F8FF')

    # Permitir redimensionamento
    app.rowconfigure(1, weight=1)
    app.columnconfigure(0, weight=1)


def criar_frame():
    frame = LabelFrame(app, text=' Cadastro ', borderwidth=1, relief='solid')
    frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
    frame.columnconfigure(1, weight=1)
    return frame


def criar_labels(frame):
    Label(frame, text='Contatos:', fg='red', font=('Arial', 14, 'italic', 'bold')).grid(row=0, column=0, columnspan=3, sticky='w', padx=10, pady=(5, 0))
    Label(frame, text='Digite um nome:', font=('Arial', 14)).grid(row=1, column=0, sticky='e', padx=10, pady=5)
    Label(frame, text='Digite um sobrenome:', font=('Arial', 14)).grid(row=2, column=0, sticky='e', padx=10, pady=5)


def criar_entry(frame):
    global nome, sobrenome
    nome = Entry(frame, font=('Arial', 14))
    nome.grid(row=1, column=1, sticky='we', padx=10)
    sobrenome = Entry(frame, font=('Arial', 14))
    sobrenome.grid(row=2, column=1, sticky='we', padx=10)
    return nome, sobrenome


def criar_checkbutton(frame):
    global genero_var
    genero_var = StringVar()
    generos = ['Masculino', 'Feminino', 'Outros']
    for i, gen in enumerate(generos):
        Radiobutton(frame, text=gen, variable=genero_var, value=gen, font=('Arial', 14)).grid(row=i+1, column=2, sticky='w', padx=10)
    return genero_var


def criar_botao():
    btn_frame = Frame(app, bg='#F8F8FF')
    btn_frame.grid(row=2, column=0, pady=10)
    Button(btn_frame, text='Inserir dados', font=('Arial', 14, 'bold'), command=capturar).pack(side=LEFT, padx=10)
    Button(btn_frame, text='Pesquisar dados', font=('Arial', 14, 'bold'), command=abrir_janela_pesquisa).pack(side=LEFT, padx=10)
    Button(btn_frame, text='Sair', font=('Arial', 14, 'bold'), command=app.quit).pack(side=LEFT, padx=10)


def criar_treeview():
    global tree
    frame_tree = Frame(app)
    frame_tree.grid(row=4, column=0, sticky='nsew', padx=10, pady=10)
    app.rowconfigure(4, weight=1)

    colunas = ('nome', 'sobrenome', 'genero')
    tree = ttk.Treeview(frame_tree, columns=colunas, show='headings')
    tree.heading('nome', text='Nome')
    tree.heading('sobrenome', text='Sobrenome')
    tree.heading('genero', text='Gênero')
    tree.column('nome', width=250)
    tree.column('sobrenome', width=250)
    tree.column('genero', width=150)
    tree.pack(side=LEFT, fill=BOTH, expand=True)

    scroll_y = ttk.Scrollbar(frame_tree, orient='vertical', command=tree.yview)
    scroll_x = ttk.Scrollbar(frame_tree, orient='horizontal', command=tree.xview)
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)


def atualizar_treeview(dados):
    tree.delete(*tree.get_children())
    for pessoa in dados:
        tree.insert('', 'end', values=pessoa)


def capturar():
    entrada_nome = valida_campo(nome.get(), 'Nome')
    entrada_sobrenome = valida_campo(sobrenome.get(), 'Sobrenome')
    genero_selecionado = genero_var.get()

    if not entrada_nome:
        nome.focus_set()
        return
    if not entrada_sobrenome:
        sobrenome.focus_set()
        return
    if not genero_selecionado:
        messagebox.showwarning('Aviso', 'Selecione um gênero.')
        return

    pessoa = {
        'nome': entrada_nome,
        'sobrenome': entrada_sobrenome,
        'genero': genero_selecionado
    }

    grava_dados_arquivo(pessoa)
    atualizar_treeview(carregar_dados_arquivo())
    nome.delete(0, 'end')
    sobrenome.delete(0, 'end')
    genero_var.set('Masculino')  # Sempre volta para Masculino após gravar
    nome.focus_set()


# --- JANELA DE PESQUISA USANDO Toplevel ---

def abrir_janela_pesquisa():
    global janela_pesquisa, campo_pesquisa, tree_pesquisa

    # Se já existe, foca nela
    if 'janela_pesquisa' in globals() and janela_pesquisa.winfo_exists():
        janela_pesquisa.focus()
        return

    janela_pesquisa = Toplevel(app)
    janela_pesquisa.title('Pesquisar Cadastros')
    janela_pesquisa.geometry('700x400')
    janela_pesquisa.configure(background='#F8F8FF')
    janela_pesquisa.grab_set()  # Faz a janela modal (bloqueia a principal)

    Label(janela_pesquisa, text='Digite o nome ou sobrenome para pesquisar:', font=('Arial', 14), bg='#F8F8FF').pack(pady=(10, 0))

    campo_pesquisa = Entry(janela_pesquisa, font=('Arial', 14))
    campo_pesquisa.pack(pady=5, padx=10, fill=X)
    campo_pesquisa.focus_set()
    campo_pesquisa.bind('<KeyRelease>', filtrar_dados_pesquisa)

    # Treeview da pesquisa
    colunas = ('nome', 'sobrenome', 'genero')
    frame_tree = Frame(janela_pesquisa)
    frame_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

    tree_pesquisa = ttk.Treeview(frame_tree, columns=colunas, show='headings')
    tree_pesquisa.heading('nome', text='Nome')
    tree_pesquisa.heading('sobrenome', text='Sobrenome')
    tree_pesquisa.heading('genero', text='Gênero')
    tree_pesquisa.column('nome', width=200)
    tree_pesquisa.column('sobrenome', width=200)
    tree_pesquisa.column('genero', width=120)
    tree_pesquisa.pack(side=LEFT, fill=BOTH, expand=True)

    scroll_y = ttk.Scrollbar(frame_tree, orient='vertical', command=tree_pesquisa.yview)
    scroll_x = ttk.Scrollbar(frame_tree, orient='horizontal', command=tree_pesquisa.xview)
    tree_pesquisa.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)

    # Botão fechar pesquisa
    btn_fechar = Button(janela_pesquisa, text='Fechar Pesquisa', font=('Arial', 12), command=fechar_janela_pesquisa)
    btn_fechar.pack(pady=(0, 10))

    # Carrega dados completos na pesquisa inicialmente
    atualizar_treeview_pesquisa(carregar_dados_arquivo())


def fechar_janela_pesquisa():
    if 'janela_pesquisa' in globals() and janela_pesquisa.winfo_exists():
        janela_pesquisa.destroy()


def atualizar_treeview_pesquisa(dados):
    tree_pesquisa.delete(*tree_pesquisa.get_children())
    for pessoa in dados:
        tree_pesquisa.insert('', 'end', values=pessoa)


def filtrar_dados_pesquisa(event):
    query = campo_pesquisa.get().lower().strip()
    dados_filtrados = []

    for pessoa in carregar_dados_arquivo():
        nome_, sobrenome_, _ = pessoa
        nome_completo = f"{nome_} {sobrenome_}".lower()
        if query in nome_.lower() or query in sobrenome_.lower() or query in nome_completo:
            dados_filtrados.append(pessoa)

    atualizar_treeview_pesquisa(dados_filtrados)


# Início do programa
if __name__ == '__main__':
    app = Tk()
    configurar_app()
    frame = criar_frame()
    criar_labels(frame)
    nome, sobrenome = criar_entry(frame)
    genero_var = criar_checkbutton(frame)
    criar_botao()
    criar_treeview()
    atualizar_treeview(carregar_dados_arquivo())
    app.mainloop()
