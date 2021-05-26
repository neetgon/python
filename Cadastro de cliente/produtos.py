from tkinter import *

import time, os
from multiprocessing import Process
from PIL import ImageTk, Image

app = Tk()
app . title("Cadastro")
app . config(bg='#1e2124')
app . geometry('800x650')

def salvar(nome, revista, produto, codigo, valor, pagina, lista):
    if len(nome) > 0 and len(revista) > 0 and len(produto) > 0 and len(codigo) > 0 and len(valor) > 0 and len(pagina) > 0:
        if not os.path.exists('Clientes'):
            os.makedirs('Clientes')
        
        file = open("Clientes/" + str(nome) + str('.txt'), "w")
        file.writelines('{}'.format(nome) + "\n")
        file.writelines('{}'.format(revista) + "\n")
        file.writelines('{}'.format(produto) + "\n")
        file.writelines('{}'.format(codigo) + "\n")
        file.writelines('{}'.format(valor) + "\n")
        file.writelines('{}'.format(pagina) + "\n")
        file.close()
        
        not_in_list = False
        
        if lista.size() > 0:
            for i in range(lista.size()):
                name = str(lista.get(i))
                
                if name == nome:
                    not_in_list = True
                    break
        
        if not not_in_list:
            lista.insert(END, nome)

def limpar_entry(lista, nome, revista, produto, codigo, valor, pagina):
    # Limpar
    nome.delete(0, END)
    revista.delete(0, END)
    produto.delete(0, END)
    codigo.delete(0, END)
    valor.delete(0, END)
    pagina.delete(0, END)

def excluir_usuario(lista, nome, revista, produto, codigo, valor, pagina):
    if lista.size() > 0:
        item = int(lista.curselection()[0])
        name = str(lista.get(item))
        file = '.txt'
        os.remove("{}{}{}".format("clientes/", str(name), file))
        
        lista.delete(item)
        
        # Limpar
        nome.delete(0, END)
        revista.delete(0, END)
        produto.delete(0, END)
        codigo.delete(0, END)
        valor.delete(0, END)
        pagina.delete(0, END)

def redefenir_lista(lista, nome, revista, produto, codigo, valor, pagina):
    if lista.size() > 0:
        item = int(lista.curselection()[0])
        name = str(lista.get(item))
        file = '.txt'
        client = open("{}{}{}".format("clientes/", str(name), file), "r")
        
        lista_do_client = []
        
        for line in client:
            if line.endswith('\n'):
                line = line[:-1]
            lista_do_client.append(line)
        
        # Limpar
        nome.delete(0, END)
        revista.delete(0, END)
        produto.delete(0, END)
        codigo.delete(0, END)
        valor.delete(0, END)
        pagina.delete(0, END)
        
        # Mostrar
        nome.insert(END, lista_do_client[0])
        revista.insert(END, lista_do_client[1])
        produto.insert(END, lista_do_client[2])
        codigo.insert(END, lista_do_client[3])
        valor.insert(END, lista_do_client[4])
        pagina.insert(END, lista_do_client[5])
        
def interface():
    
    nome_icon_label = Canvas(width=2000, heigh=2000, bg="#1e2124", relief='flat')
    nome_icon_label . place(x=-396, y=-338)
    
    photo = photo=PhotoImage(file="data/imagens/buttons.png")
    nome_icon_label.create_image(800, 650, image=photo)
    
    # Nome
    nome_label = Label(text="Cliente:", font='tahoma 15', bg='#1e2124', fg='orange')
    nome_label . place(x=75, y=10)
    nome_entry = Entry(relief='flat', font='tahoma 12', bg='#272a2d', fg='white')
    nome_entry . place(x=75, y=40, width=200, height=50)
    
    # Revista
    revista_label = Label(text="Revista:", font='tahoma 15', bg='#1e2124', fg='orange')
    revista_label . place(x=75, y=100)
    revista_entry = Entry(relief='flat', font='tahoma 12', bg='#272a2d', fg='white')
    revista_entry . place(x=75, y=130, width=200, height=50)
    
    # Produto
    produto_label = Label(text="Produto:", font='tahoma 15', bg='#1e2124', fg='orange')
    produto_label . place(x=75, y=190)
    produto_entry = Entry(relief='flat', font='tahoma 12', bg='#272a2d', fg='white')
    produto_entry . place(x=75, y=220, width=200, height=50)

    # Codigo
    codigo_label = Label(text="Código:", font='tahoma 15', bg='#1e2124', fg='orange')
    codigo_label . place(x=75, y=280)
    codigo_entry = Entry(relief='flat', font='tahoma 12', bg='#272a2d', fg='white')
    codigo_entry . place(x=75, y=310, width=200, height=50)
    
    # Valor
    valor_label = Label(text="Valor:", font='tahoma 15', bg='#1e2124', fg='orange')
    valor_label . place(x=75, y=370)
    valor_entry = Entry(relief='flat', font='tahoma 12', bg='#272a2d', fg='white')
    valor_entry . place(x=75, y=400, width=200, height=50)
    
    # Pagina
    pagina_label = Label(text="Página:", font='tahoma 15', bg='#1e2124', fg='orange')
    pagina_label . place(x=75, y=460)
    pagina_entry = Entry(relief='flat', font='tahoma 12', bg='#272a2d', fg='white')
    pagina_entry . place(x=75, y=500, width=200, height=50)
        
    # Lista
    lista_name = Label(text="Lista de clientes:", font='tahoma 15', bg='#1e2124', fg='orange')
    lista_name . place(x=400, y=10)
    lista_listbox = Listbox(borderwidth=0, bg='#272a2d', fg='white', font='tahoma 12', activestyle=None, selectborderwidth=0, highlightthickness=0)
    lista_listbox.place(x=405, y =40, width=300, height=500)
    lista_listbox.bind('<<ListboxSelect>>', lambda event: redefenir_lista(lista_listbox, nome_entry, revista_entry, produto_entry, codigo_entry, valor_entry, pagina_entry))
        
    # Adicionar todos objetos na lista
    if os.path.exists('Clientes'):
        lista = os.listdir('clientes')
        
        for i in range(len(lista)):
            lista_name = lista[i]
            
            if lista_name.endswith('.txt'):
                lista_name = lista_name[:-4]
            
            lista_listbox.insert(END, lista_name)
    
    scrollbar = Scrollbar(orient="vertical")
    scrollbar.config(command=lista_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    lista_listbox.config(yscrollcommand=scrollbar.set)
    
    
    # Salvar
    salvar_button = Button(text="Salvar", font='tahoma 15 bold', bg='orange', fg='white', relief='flat', 
    command=lambda: salvar(nome_entry.get(), revista_entry.get(), produto_entry.get(), codigo_entry.get(), valor_entry.get(), pagina_entry.get(), lista_listbox))
    salvar_button . place(x=10, y=580, width=100, height=50)
    
    # Limpar
    salvar_button = Button(text="Limpar", font='tahoma 15 bold', bg='green', fg='white', relief='flat', 
    command=lambda: limpar_entry(lista_listbox, nome_entry, revista_entry, produto_entry, codigo_entry, valor_entry, pagina_entry))
    salvar_button . place(x=120, y=580, width=100, height=50)
    
    # Excluir
    salvar_button = Button(text="Excluir", font='tahoma 15 bold', bg='red', fg='white', relief='flat', 
    command=lambda: excluir_usuario(lista_listbox, nome_entry, revista_entry, produto_entry, codigo_entry, valor_entry, pagina_entry))
    salvar_button . place(x=230, y=580, width=100, height=50)
    
    # loop inicial
    app.mainloop()
    
if __name__ == "__main__":
    interface()
