"""
Claudinei de Oliveira - UTF8 - pt-br - 13-11-2023
- Tkinter: teste de aceitação - arquivo de dados 
JSON - JavaScript Object Notation

import os
import json
import regex as re
from tkinter import *
from tkinter import ttk, messagebox

# Funções do código modo interativo

def valida_campo(campo, tipo_campo):
    if not campo:
        messagebox.showwarning('Aviso', f'{tipo_campo} inválido.')
        return False
    if len(campo) > 50:
        messagebox.showwarning('Aviso', f'{tipo_campo} muito longo. Deve ter no máximo 50 caracteres.')
        return False

    pattern = r'^[\p{L}\s]{1,50}$'
    if not re.match(pattern, campo):
        messagebox.showwarning('Aviso', f'{tipo_campo} inválido. Não use números ou caracteres especiais.')
        return False

    preposicoes = ['da', 'de', 'do', 'das', 'dos']
    campo = ' '.join([parte.capitalize() if parte not in preposicoes else parte for parte in re.sub(r'\s+', ' ', campo).split()])
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

# Funções do Tkinter

def configurar_app():
    app.title('Análise e Desenvolvimento de Sistemas')
    app.geometry('1360x670')
    app.configure(background='#F8F8FF')
    app.resizable(True, True)
    app.maxsize(width=1360, height=670)

def criar_frame():
    frame = LabelFrame(app, text=' Cadastro ', borderwidth=1, relief='solid')
    frame.place(x=10, y=10, width=1340, height=340)
    return frame

def criar_labels(frame):
    lb_1 = Label(frame, text='Contatos: ', fg='red', font=('Arial', 14, 'italic', 'bold'))
    lb_1.place(x=15, y=10, width=70, height=20)
    lb_nome = Label(frame, text='Digite um nome: ', font=('Arial', 14))
    lb_nome.place(x=20, y=35, width=120, height=20)
    lb_sobrenome = Label(frame, text='Digite um sobrenome: ', font=('Arial', 14))
    lb_sobrenome.place(x=20, y=65, width=180, height=20)

def criar_entry(frame):
    global nome, sobrenome
    nome = Entry(frame, font=('Arial', 14))
    nome.place(x=200, y=35, width=400, height=20)
    sobrenome = Entry(frame, font=('Arial', 14))
    sobrenome.place(x=200, y=65, width=400, height=20)
    return nome, sobrenome

def criar_checkbutton(frame):
    global genero_var
    genero_var = StringVar()
    generos = ['Masculino', 'Feminino', 'Outros']
    y_pos = 95
    for gen in generos:
        Radiobutton(frame, text=gen, variable=genero_var, value=gen, font=('Arial', 14)).place(x=200, y=y_pos)
        y_pos += 30
    return genero_var

def criar_botao():
    btn_captura = Button(app, text='Inserir dados', font=('Arial', 14, 'bold'), command=capturar)
    btn_captura.place(x=490, y=360, width=125, height=40)
    btn_sair = Button(app, text='Sair', font=('Arial', 14, 'bold'), command=app.quit)
    btn_sair.place(x=625, y=360, width=125, height=40)

def criar_treeview():
    cols = ('Nome', 'Sobrenome', 'Genero')
    tree = ttk.Treeview(app, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=200)

    scroll_y = ttk.Scrollbar(app, orient='vertical', command=tree.yview)
    scroll_x = ttk.Scrollbar(app, orient='horizontal', command=tree.xview)
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tree.place(x=10, y=410, width=1340, height=250)
    scroll_y.place(x=1350, y=410, width=20, height=250)
    scroll_x.place(x=10, y=660, width=1340, height=20)
    return tree

def capturar():
    entrada_nome = valida_campo(nome.get().strip(), 'Nome')
    entrada_sobrenome = valida_campo(sobrenome.get().strip(), 'Sobrenome')
    genero_selecionado = genero_var.get()

    if entrada_nome == entrada_sobrenome:
        messagebox.showwarning('Aviso', 'Sobrenome não deve ser igual ao nome...')
        return

    if not genero_selecionado:
        messagebox.showwarning('Aviso', 'Nenhum gênero selecionado. Por favor, selecione um gênero.')
        return

    if entrada_nome and entrada_sobrenome and genero_selecionado:
        pessoa = {
            'nome': entrada_nome,
            'sobrenome': entrada_sobrenome,
            'genero': genero_selecionado
        }
        grava_dados_arquivo(pessoa)
        tree.insert('', 'end', values=(entrada_nome, entrada_sobrenome, genero_selecionado))
        nome.delete(0, 'end')
        sobrenome.delete(0, 'end')
        nome.focus_set()

app = Tk()
configurar_app()
frame = criar_frame()
criar_labels(frame)
nome, sobrenome = criar_entry(frame)
genero_var = criar_checkbutton(frame)
criar_botao()
tree = criar_treeview()

# Carregando dados do arquivo no Treeview
# ao iniciar a aplicação
for pessoa in carregar_dados_arquivo():
    tree.insert('', 'end', values=pessoa)

app.mainloop()


#######  Teste

import os
import json
import regex as re
from tkinter import *
from tkinter import ttk, messagebox

# Funções do código modo interativo

def valida_campo(campo, tipo_campo):
    if not campo:
        messagebox.showwarning('Aviso', f'{tipo_campo} inválido.')
        return False
    if len(campo) > 50:
        messagebox.showwarning('Aviso', f'{tipo_campo} muito longo. Deve ter no máximo 50 caracteres.')
        return False

    pattern = r'^[\p{L}\s]{1,50}$'
    if not re.match(pattern, campo):
        messagebox.showwarning('Aviso', f'{tipo_campo} inválido. Não use números ou caracteres especiais.')
        return False

    preposicoes = ['da', 'de', 'do', 'das', 'dos']
    campo = ' '.join([parte.capitalize() if parte not in preposicoes else parte for parte in re.sub(r'\s+', ' ', campo).split()])
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

# Funções do Tkinter

def configurar_app():
    app.title('Análise e Desenvolvimento de Sistemas')
    app.geometry('1024x512')
    app.configure(background='#F8F8FF')
    app.resizable(True, True)
    app.maxsize(width=1024, height=512)

def criar_frame():
    frame = LabelFrame(app, text=' Cadastro ', borderwidth=1, relief='solid')
    frame.place(x=10, y=10, width=1000, height=120)
    return frame

def criar_labels(frame):
    lb_1 = Label(frame, text='Contatos: ', fg='red', font=('Arial', 14, 'italic', 'bold'))
    lb_1.place(x=15, y=10, width=70, height=20)
    lb_nome = Label(frame, text='Digite um nome: ', font=('Arial', 14))
    lb_nome.place(x=20, y=35, width=120, height=20)
    lb_sobrenome = Label(frame, text='Digite um sobrenome: ', font=('Arial', 14))
    lb_sobrenome.place(x=20, y=65, width=180, height=20)

def criar_entry(frame):
    global nome, sobrenome
    nome = Entry(frame, font=('Arial', 14))
    nome.place(x=200, y=35, width=400, height=20)
    sobrenome = Entry(frame, font=('Arial', 14))
    sobrenome.place(x=200, y=65, width=400, height=20)
    return nome, sobrenome

def criar_checkbutton(frame):
    global genero_var
    genero_var = StringVar()
    generos = ['Masculino', 'Feminino', 'Outros']
    y_pos = 95
    for gen in generos:
        Radiobutton(frame, text=gen, variable=genero_var, value=gen, font=('Arial', 14)).place(x=200, y=y_pos)
        y_pos += 30
    return genero_var

def criar_botao():
    btn_captura = Button(app, text='Inserir dados', font=('Arial', 14, 'bold'), command=capturar)
    btn_captura.place(x=200, y=140, width=125, height=40)
    btn_sair = Button(app, text='Sair', font=('Arial', 14, 'bold'), command=app.quit)
    btn_sair.place(x=335, y=140, width=125, height=40)
    btn_pesquisar = Button(app, text='Pesquisar dados', font=('Arial', 14, 'bold'), command=mostrar_campo_pesquisa)
    btn_pesquisar.place(x=470, y=140, width=155, height=40)

def criar_campo_pesquisa():
    global campo_pesquisa, lb_pesquisa
    lb_pesquisa = Label(app, text='Digite o nome a pesquisar:', font=('Arial', 14))
    lb_pesquisa.place(x=20, y=190, width=250, height=20)
    campo_pesquisa = Entry(app, font=('Arial', 14))
    campo_pesquisa.place(x=275, y=190, width=425, height=20)
    campo_pesquisa.bind('<KeyRelease>', filtrar_dados)
    campo_pesquisa.focus()

def criar_treeview():
    cols = ('Nome', 'Sobrenome', 'Genero')
    tree = ttk.Treeview(app, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=200)

    scroll_y = ttk.Scrollbar(app, orient='vertical', command=tree.yview)
    scroll_x = ttk.Scrollbar(app, orient='horizontal', command=tree.xview)
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tree.place(x=10, y=220, width=1000, height=282)
    scroll_y.place(x=1010, y=220, width=20, height=282)
    scroll_x.place(x=10, y=502, width=1000, height=20)
    return tree

def capturar():
    entrada_nome = valida_campo(nome.get().strip(), 'Nome')
    entrada_sobrenome = valida_campo(sobrenome.get().strip(), 'Sobrenome')
    genero_selecionado = genero_var.get()

    if entrada_nome == False or entrada_sobrenome == False:
        return

    pessoa = {
        'nome': entrada_nome,
        'sobrenome': entrada_sobrenome,
        'genero': genero_selecionado
    }
    grava_dados_arquivo(pessoa)
    tree.insert('', 'end', values=(entrada_nome, entrada_sobrenome, genero_selecionado))
    nome.delete(0, 'end')
    sobrenome.delete(0, 'end')
    genero_var.set(None)

def mostrar_campo_pesquisa():
    criar_campo_pesquisa()
    sobrenome.delete(0, 'end')
    nome.delete(0, 'end')
    genero_var.set(None)

# Função para filtrar dados com base na pesquisa
def filtrar_dados(event):
    query = campo_pesquisa.get()
    filtrar_dados_treeview(query)

def filtrar_dados_treeview(query):
    # Primeiro, limpe todos os registros da treeview
    for i in tree.get_children():
        tree.delete(i)
    
    # Carregue todos os dados que correspondem à consulta
    dados_filtrados = [pessoa for pessoa in carregar_dados_arquivo() if query.lower() in pessoa[0].lower() or query.lower() in pessoa[1].lower()]
    for pessoa in dados_filtrados:
        tree.insert('', 'end', values=pessoa)

# Inicialização do aplicativo
if __name__ == '__main__':
    app = Tk()
    configurar_app()
    frame = criar_frame()
    criar_labels(frame)
    nome, sobrenome = criar_entry(frame)
    genero_var = criar_checkbutton(frame)
    criar_botao()
    tree = criar_treeview()
    for pessoa in carregar_dados_arquivo():
        tree.insert('', 'end', values=pessoa)
    app.mainloop()


### Teste 2

import os
import json
import regex as re
from tkinter import *
from tkinter import ttk, messagebox
# Funções do código modo interativo

def valida_campo(campo, tipo_campo):
    if not campo:
        messagebox.showwarning('Aviso', f'{tipo_campo} inválido.')
        return False
    if len(campo) > 50:
        messagebox.showwarning('Aviso', f'{tipo_campo} muito longo. Deve ter no máximo 50 caracteres.')
        return False

    pattern = r'^[\p{L}\s]{1,50}$'
    if not re.match(pattern, campo):
        messagebox.showwarning('Aviso', f'{tipo_campo} inválido. Não use números ou caracteres especiais.')
        return False

    preposicoes = ['da', 'de', 'do', 'das', 'dos']
    campo = ' '.join([parte.capitalize() if parte not in preposicoes else parte for parte in re.sub(r'\s+', ' ', campo).split()])
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

# Funções do Tkinter

def configurar_app():
    app.title('Análise e Desenvolvimento de Sistemas')
    app.geometry('1024x600')
    app.configure(background='#F8F8FF')
    app.resizable(True, True)
    app.maxsize(width=1024, height=600)

def criar_frame():
    frame = LabelFrame(app, text=' Cadastro ', borderwidth=1, relief='solid')
    frame.place(x=10, y=10, width=1000, height=200)
    return frame

def criar_labels(frame):
    lb_1 = Label(frame, text='Contatos: ', fg='red', font=('Arial', 14, 'italic', 'bold'))
    lb_1.place(x=15, y=10, width=70, height=20)
    lb_nome = Label(frame, text='Digite um nome: ', font=('Arial', 14))
    lb_nome.place(x=20, y=35, width=120, height=20)
    lb_sobrenome = Label(frame, text='Digite um sobrenome: ', font=('Arial', 14))
    lb_sobrenome.place(x=20, y=65, width=180, height=20)

def criar_entry(frame):
    global nome, sobrenome
    nome = Entry(frame, font=('Arial', 14))
    nome.place(x=200, y=35, width=400, height=20)
    sobrenome = Entry(frame, font=('Arial', 14))
    sobrenome.place(x=200, y=65, width=400, height=20)
    return nome, sobrenome

def criar_checkbutton(frame):
    global genero_var
    genero_var = StringVar()
    generos = ['Masculino', 'Feminino', 'Outros']
    y_pos = 95
    for gen in generos:
        Radiobutton(frame, text=gen, variable=genero_var, value=gen, font=('Arial', 14)).place(x=200, y=y_pos)
        y_pos += 30
    return genero_var

def criar_botao():
    btn_captura = Button(app, text='Inserir dados', font=('Arial', 14, 'bold'), command=capturar)
    btn_captura.place(x=200, y=220, width=125, height=40)
    btn_sair = Button(app, text='Sair', font=('Arial', 14, 'bold'), command=app.quit)
    btn_sair.place(x=335, y=220, width=125, height=40)
    btn_pesquisar = Button(app, text='Pesquisar dados', font=('Arial', 14, 'bold'), command=mostrar_campo_pesquisa)
    btn_pesquisar.place(x=470, y=220, width=155, height=40)

def criar_campo_pesquisa():
    global campo_pesquisa, btn_fechar_pesquisa
    lb_pesquisar = Label(app, text='Digite o nome a pesquisar: ', font=('Arial', 14))
    lb_pesquisar.place(x=10, y=270, width=220, height=20)
    campo_pesquisa = Entry(app, font=('Arial', 14))
    campo_pesquisa.place(x=230, y=270, width=370, height=20)
    campo_pesquisa.bind('<KeyRelease>', filtrar_dados)
    btn_fechar_pesquisa = Button(app, text='Fechar pesquisa', font=('Arial', 14, 'bold'), command=fechar_pesquisa)
    btn_fechar_pesquisa.place(x=610, y=265, width=155, height=30)

def fechar_pesquisa():
    lb_pesquisar.destroy()
    campo_pesquisa.destroy()
    btn_fechar_pesquisa.destroy()
    for i in tree.get_children():
        tree.delete(i)
    for pessoa in carregar_dados_arquivo():
        tree.insert('', 'end', values=pessoa)

def criar_treeview():
    global tree
    colunas = ('nome', 'sobrenome', 'genero')
    tree = ttk.Treeview(app, columns=colunas, show='headings')
    tree.heading('nome', text='Nome')
    tree.heading('sobrenome', text='Sobrenome')
    tree.heading('genero', text='Gênero')
    tree.column('nome', minwidth=0, width=250)
    tree.column('sobrenome', minwidth=0, width=250)
    tree.column('genero', minwidth=0, width=100)
    tree.place(x=10, y=300, width=1000, height=200)
    scroll_y = ttk.Scrollbar(app, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scroll_y.set)
    scroll_x = ttk.Scrollbar(app, orient='horizontal', command=tree.xview)
    tree.configure(xscroll=scroll_x.set)
    scroll_y.place(x=992, y=300, width=18, height=200)
    scroll_x.place(x=10, y=502, width=982, height=18)

    return tree

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
        messagebox.showwarning('Aviso', 'Selecione um gênero...')
        return

    pessoa = {
        'nome': entrada_nome,
        'sobrenome': entrada_sobrenome,
        'genero': genero_selecionado
    }

    grava_dados_arquivo(pessoa)
    tree.insert('', 'end', values=(entrada_nome, entrada_sobrenome, genero_selecionado))
    nome.delete(0, 'end')
    sobrenome.delete(0, 'end')
    genero_var.set(None)
    nome.focus_set()

def mostrar_campo_pesquisa():
    if 'campo_pesquisa' not in globals():
        criar_campo_pesquisa()
    nome.delete(0, 'end')
    sobrenome.delete(0, 'end')
    genero_var.set(None)

def filtrar_dados(event):
    query = campo_pesquisa.get()
    filtrar_dados_treeview(query)

def filtrar_dados_treeview(query):
    for i in tree.get_children():
        tree.delete(i)

    dados_filtrados = [pessoa for pessoa in carregar_dados_arquivo() if query.lower() in pessoa[0].lower() or query.lower() in pessoa[1].lower()]
    for pessoa in dados_filtrados:
        tree.insert('', 'end', values=pessoa)


if __name__ == '__main__':
    app = Tk()
    configurar_app()
    frame = criar_frame()
    criar_labels(frame)
    nome, sobrenome = criar_entry(frame)
    genero_var = criar_checkbutton(frame)
    criar_botao()
    tree = criar_treeview()
    for pessoa in carregar_dados_arquivo():
        tree.insert('', 'end', values=pessoa)
    app.mainloop()
"""

### Teste 2

import os
import json
import regex as re
from tkinter import *
from tkinter import ttk, messagebox

# funções do código modo interativo
def valida_campo(campo, tipo_campo):
    if not campo:
        messagebox.showwarning('Aviso', f'{tipo_campo} inválido.')
        return False
    if len(campo) > 50:
        messagebox.showwarning('Aviso', f'{tipo_campo} muito longo. Deve ter no máximo 50 caracteres.')
        return False

    pattern = r'^[\p{L}\s]{1,50}$'
    if not re.match(pattern, campo):
        messagebox.showwarning('Aviso', f'{tipo_campo} inválido. Não use números ou caracteres especiais.')
        return False

    preposicoes = ['da', 'de', 'do', 'das', 'dos']
    campo = ' '.join([parte.capitalize() if parte not in preposicoes else parte for parte in re.sub(r'\s+', ' ', campo).split()])
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


# Funções do Tkinter
def configurar_app():
    app.title('Análise e Desenvolvimento de Sistemas')
    app.geometry('1024x600')
    app.configure(background='#F8F8FF')
    app.resizable(True, True)
    app.maxsize(width=1024, height=600)


def criar_frame():
    frame = LabelFrame(app, text=' Cadastro ', borderwidth=1, relief='solid')
    frame.place(x=10, y=10, width=1000, height=200)
    return frame


def criar_labels(frame):
    lb_1 = Label(frame, text='Contatos: ', fg='red', font=('Arial', 14, 'italic', 'bold'))
    lb_1.place(x=15, y=10, width=70, height=20)
    lb_nome = Label(frame, text='Digite um nome: ', font=('Arial', 14))
    lb_nome.place(x=20, y=35, width=120, height=20)
    lb_sobrenome = Label(frame, text='Digite um sobrenome: ', font=('Arial', 14))
    lb_sobrenome.place(x=20, y=65, width=180, height=20)


def criar_entry(frame):
    global nome, sobrenome
    nome = Entry(frame, font=('Arial', 14))
    nome.place(x=200, y=35, width=400, height=20)
    sobrenome = Entry(frame, font=('Arial', 14))
    sobrenome.place(x=200, y=65, width=400, height=20)
    return nome, sobrenome


def criar_checkbutton(frame):
    global genero_var
    genero_var = StringVar()
    generos = ['Masculino', 'Feminino', 'Outros']
    y_pos = 95
    for gen in generos:
        Radiobutton(frame, text=gen, variable=genero_var, value=gen, font=('Arial', 14)).place(x=200, y=y_pos)
        y_pos += 30
    return genero_var


def criar_botao():
    btn_captura = Button(app, text='Inserir dados', font=('Arial', 14, 'bold'), command=capturar)
    btn_captura.place(x=200, y=220, width=125, height=40)
    btn_sair = Button(app, text='Sair', font=('Arial', 14, 'bold'), command=app.quit)
    btn_sair.place(x=335, y=220, width=125, height=40)
    btn_pesquisar = Button(app, text='Pesquisar dados', font=('Arial', 14, 'bold'), command=mostrar_campo_pesquisa)
    btn_pesquisar.place(x=470, y=220, width=155, height=40)


def criar_campo_pesquisa():
    global campo_pesquisa, btn_fechar_pesquisa, lb_pesquisar  # Adicione 'lb_pesquisar' aqui
    lb_pesquisar = Label(app, text='Digite o nome a pesquisar: ', font=('Arial', 14), bg='white')
    lb_pesquisar.place(x=10, y=270, width=220, height=20)
    campo_pesquisa = Entry(app, font=('Arial', 14))
    campo_pesquisa.place(x=230, y=270, width=370, height=20)
    campo_pesquisa.bind('<KeyRelease>', filtrar_dados)
    btn_fechar_pesquisa = Button(app, text='Fechar pesquisa', font=('Arial', 14, 'bold'), command=fechar_pesquisa)
    btn_fechar_pesquisa.place(x=610, y=265, width=155, height=30)

def fechar_pesquisa():
    lb_pesquisar.destroy()
    campo_pesquisa.destroy()
    btn_fechar_pesquisa.destroy()
    for i in tree.get_children():
        tree.delete(i)
    for pessoa in carregar_dados_arquivo():
        tree.insert('', 'end', values=pessoa)


def criar_treeview():
    global tree
    colunas = ('nome', 'sobrenome', 'genero')
    tree = ttk.Treeview(app, columns=colunas, show='headings')
    tree.heading('nome', text='Nome')
    tree.heading('sobrenome', text='Sobrenome')
    tree.heading('genero', text='Gênero')
    tree.column('nome', minwidth=0, width=250)
    tree.column('sobrenome', minwidth=0, width=250)
    tree.column('genero', minwidth=0, width=100)
    tree.place(x=10, y=300, width=1000, height=200)
    scroll_y = ttk.Scrollbar(app, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scroll_y.set)
    scroll_x = ttk.Scrollbar(app, orient='horizontal', command=tree.xview)
    tree.configure(xscroll=scroll_x.set)
    scroll_y.place(x=992, y=300, width=18, height=200)
    scroll_x.place(x=10, y=502, width=982, height=18)

    return tree


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
        messagebox.showwarning('Aviso', 'Selecione um gênero...')
        return

    pessoa = {
        'nome': entrada_nome,
        'sobrenome': entrada_sobrenome,
        'genero': genero_selecionado
    }


    grava_dados_arquivo(pessoa)
    tree.insert('', 'end', values=(entrada_nome, entrada_sobrenome, genero_selecionado))
    nome.delete(0, 'end')
    sobrenome.delete(0, 'end')
    genero_var.set(None)
    nome.focus_set()


def mostrar_campo_pesquisa():
    if 'campo_pesquisa' not in globals():
        criar_campo_pesquisa()
    nome.delete(0, 'end')
    sobrenome.delete(0, 'end')
    genero_var.set(None)

def filtrar_dados(event):
    query = campo_pesquisa.get()
    filtrar_dados_treeview(query)


def filtrar_dados_treeview(query):
    for i in tree.get_children():
        tree.delete(i)

    dados_filtrados = [pessoa for pessoa in carregar_dados_arquivo() if query.lower() in pessoa[0].lower() or query.lower() in pessoa[1].lower()]
    for pessoa in dados_filtrados:
        tree.insert('', 'end', values=pessoa)


if __name__ == '__main__':
    app = Tk()
    configurar_app()
    frame = criar_frame()
    criar_labels(frame)
    nome, sobrenome = criar_entry(frame)
    genero_var = criar_checkbutton(frame)
    criar_botao()
    tree = criar_treeview()
    for pessoa in carregar_dados_arquivo():
        tree.insert('', 'end', values=pessoa)
    app.mainloop()
