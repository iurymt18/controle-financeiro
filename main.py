#importando tkinter
from tkinter import *
from tkinter import Tk, ttk

#importando barra de progresso
from tkinter.ttk import Progressbar
#importando message box
from tkinter import messagebox

#importando matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

#importando pillow
from PIL import Image, ImageTk

#importando tkcalendar
from tkcalendar import Calendar, DateEntry
from datetime import date

#importando funcoes da view
from view import inserir_receita, inserir_gasto,ver_gastos, inserir_despesa, inserir_categoria, ver_categorias,tabela,\
    deletar_receita, deletar_gasto, valores_categorias,valor_porcentagem,total_renda, total_gastos,saldo_atual, deletar_categoria


janela = Tk()
janela.title("Controle Financeiro")
janela.geometry("1000x750")
janela.resizable("False","False")
janela.config(bg="black")
style = ttk.Style(janela)
style.theme_use("clam")

#criando frames

frameCima = Frame(janela, height=50,width=1043,bg="white", relief="flat")
frameCima.grid(column=0, row=0)

frameMeio = Frame(janela, height=380,width=1043, bg="black", pady=20, relief="raised")
frameMeio.grid(column=0, row=1, pady=1, padx=0, sticky=NSEW)

frameBaixo = Frame(janela, height=320,width=1043,bg="black", relief="flat")
frameBaixo.grid(column=0, row=2, pady=0, padx=0, sticky=NSEW)

#trabalhando no frame cima

#acessando imagem
app_img = Image.open("img//logo.png")
app_img = app_img.resize((45,45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, text="Controle financeiro", width=900, compound=LEFT, padx=5, relief=FLAT, anchor=NW, font="verdana 20 bold", bg="white", fg="black")
app_logo.place(x=0,y=0)


#funcoes de insercao frame baixo
##nomeados usando "nova, um, uma" para nao haver confusao com as funcoes importadas da view
#funcao inserir nova categoria no banco de dados

#definindo tree como global
global tv
def inserir_nova_categoria():
    nome = e_nova_categoria.get()
    lista_inserir = [nome]
    print(nome)
    for i in lista_inserir:
        if i=='':
            messagebox.showerror("Ops","Insira o nome da categoria")
        else:
            inserir_categoria(lista_inserir)
            messagebox.showinfo("Sucesso!", f"Categoria {i} adicionada")
            e_nova_categoria.delete(0,'end')

            #atualizando categorias combobox
            categoria_funcao = ver_categorias()
            categoria = []
            for i in categoria_funcao:
                categoria.append(i)
            combo_categoria_gasto['values'] = (categoria)


#insira um gasto
def inserir_um_gasto():
    categoria = combo_categoria_gasto.get()
    data = e_cal_gastos.get()
    valor = e_val_gasto.get().replace(',','.')

    lista_inserir =[categoria,data,valor]
    for i in lista_inserir:
        if i=='':
            messagebox.showerror("ops", "Preencha todos os campos!")
            return
    inserir_gasto(lista_inserir)
    messagebox.showinfo("sucesso", "Os dados foram inseridos")
    #atualizando valores da tabela
    mostrar_tabela()
    grafico_bar()
    resumo()
    percentagem()


#insira uma receita
def inserir_uma_receita():
    categoria = 'Receita'
    data = e_cal_receita.get()
    valor = e_val_receita.get()
    lista_inserir =[categoria,data,valor]
    for i in lista_inserir:
        if i=='':
            messagebox.showerror("ops", "Preencha todos os campos!")
            return
    inserir_receita(lista_inserir)
    messagebox.showinfo("sucesso", "Os dados foram inseridos")
    #atualizando valores da tabela
    mostrar_tabela()
    grafico_bar()
    resumo()
    percentagem()

#funcao do botao excluir
def deletar_registro():
    try:
        item_selecionado = tv.selection()[0]
        valores = tv.item(item_selecionado, "values")
        nome = valores[1]
        id = valores[0]
        if nome=='Receita':
            deletar_receita([id])
            messagebox.showinfo('sucesso', 'Os dados foram deletados')
            mostrar_tabela()
            grafico_bar()
            resumo()
            percentagem()

        else:
            deletar_gasto([id])
            messagebox.showinfo('sucesso', 'Os dados foram deletados')
            mostrar_tabela()
            grafico_bar()
            resumo()
            percentagem()
    except IndexError:
        messagebox.showerror('Ops', 'Selecione os dados na tabela')

def deletar_uma_categoria():
    deletar_categoria([e_nova_categoria.get()])
    messagebox.showinfo('Sucesso', 'Categoria deletada')
    mostrar_tabela()
    grafico_bar()
    resumo()
    percentagem()
    # atualizando categorias combobox
    categoria_funcao = ver_categorias()
    categoria = []
    for i in categoria_funcao:
        categoria.append(i)
    combo_categoria_gasto['values'] = (categoria)



#percentagem
def percentagem():
    l_nome = Label(frameMeio, text="Porcentagem da renda gasta", height=1, anchor=NW, font="verdana 12", bg="black", fg="white")
    l_nome.place(x=7, y=0)
    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar",background="blue")
    style.configure("TProgressbar",thickness=25)
    bar = Progressbar(frameMeio, length=180, style='black.Horizontal.TProgressbar')
    bar.place(x=7, y=25)
    valor=valor_porcentagem()
    bar['value']=valor_porcentagem()
    l_porcentagem = Label(frameMeio, text="{:,.2f}%".format(valor), height=1, anchor=NW, font="verdana 15 bold",
                   bg="black", fg="white")
    l_porcentagem.place(x=200, y=25)


#grafico de barras
def grafico_bar():
    figura = plt.Figure(figsize=(6, 3.2),dpi=90)
    ax = figura.add_subplot(111)


    lista_categorias = ver_categorias()
    lista_categorias = valores_categorias()[1]
    # lista_valores = valores_categorias()
    lista_valores = valores_categorias()[2]
    bar_colors = ['tab:blue']
    bar_labels = lista_categorias
    ax.bar(lista_categorias, lista_valores, label=bar_labels, color=bar_colors)
    ax.set_title("Gastos por categoria.")
    c=0
    for i in ax.patches:
        ax.text(i.get_x()+0.2, i.get_height()+1, 'R${:,.2f}'.format(lista_valores[c]), fontsize=12, fontstyle='italic',verticalalignment='baseline',color='black')
        c += 1
    ax.patch.set_facecolor("white")
    ax.spines['bottom'].set_color("gray")
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color("gray")
    ax.spines['left'].set_linewidth(1)
    ax.yaxis.grid(True, color='gray')
    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=5,y=70)



#função de resumo total
def resumo():
    valor = [total_renda(),total_gastos(),saldo_atual()]
    l_linha = Label(frameMeio, text="", width=250, height=1, anchor=NW,font="Arial 1", bg="#545454")
    l_linha.place(x=650, y=152)
    l_resumo = Label(frameMeio, text="Total Renda Mensal            ".upper(), anchor=NW,font="verdana 12", bg="black", fg="white")
    l_resumo.place(x=650, y=135)
    l_resumo = Label(frameMeio, text="R${:,.2f}".format(valor[0]), anchor=NW,font="verdana 15", bg="black", fg="white")
    l_resumo.place(x=650, y=165)

    l_linha = Label(frameMeio, text="", width=250, height=1, anchor=NW,font="Arial 1", bg="#545454")
    l_linha.place(x=650, y=232)
    l_resumo = Label(frameMeio, text="Total Despesas Mensais            ".upper(), anchor=NW,font="verdana 12", bg="black", fg="white")
    l_resumo.place(x=650, y=215)
    l_resumo = Label(frameMeio, text="R${:,.2f}".format(valor[1]), anchor=NW,font="verdana 15", bg="black", fg="white")
    l_resumo.place(x=650, y=250)

    l_linha = Label(frameMeio, text="", width=250, height=1, anchor=NW,font="Arial 1", bg="#545454")
    l_linha.place(x=650, y=307)
    l_resumo = Label(frameMeio, text="Saldo Atual                       ".upper(), anchor=NW,font="verdana 12", bg="black", fg="white")
    l_resumo.place(x=650, y=290)
    l_resumo = Label(frameMeio, text="R${:,.2f}".format(valor[2]), anchor=NW,font="verdana 15", bg="black", fg="white")
    l_resumo.place(x=650, y=320)
    l_resumo.place(x=650, y=320)

percentagem()
grafico_bar()
resumo()


#Criando frames dentro do frameBaixo
frameTabela = Frame(frameBaixo, height=320,width=332,bg="black")
frameTabela.grid(column=0, row=0)

frameGastos = Frame(frameBaixo, height=320,width=332,bg="black")
frameGastos.grid(column=1, row=0, padx=1)

frameReceitas = Frame(frameBaixo, height=320,width=332,bg="black")
frameReceitas.grid(column=2, row=0, padx=1)

#tabela extrato -------------------------------------------------
l_tabela = Label(frameTabela, text="Tabela Receitas e Gastos ", font="verdana 12", bg="black", fg="white")
l_tabela.place(x=50,y=5)

#treeview tabela

def mostrar_tabela():
    global tv
    lista_tabela = tabela()
    tv = ttk.Treeview(frameTabela, columns=('id', 'categoria', 'data', 'quantia'), show='headings', height=12)
    tv.column('id', minwidth=0, width=50, anchor='center')
    tv.column('categoria', minwidth=0, width=100, anchor='center')
    tv.column('data', minwidth=0, width=100, anchor='center')
    tv.column('quantia', minwidth=0, width=100, anchor='center')
    tv.heading('id', text='id'.upper())
    tv.heading('categoria', text='categoria'.upper())
    tv.heading('data', text='data'.upper())
    tv.heading('quantia', text='quantia'.upper())
    tv.place(x=5, y=40)
    for i in lista_tabela:
        tv.insert("", "end", values=(i))
mostrar_tabela()

#configurando Gastos
l_info = Label(frameGastos, text="Insira um gasto", height=1, anchor=NW, font='verdana 10 bold', bg="black", fg="white")
l_info.place(x=10, y=10)

#Categoria-------------------------------------------------------------------------------------
l_Categoria = Label(frameGastos, text="Categoria", height=1, anchor=NW, font='Ivy 12', bg="black", fg="white")
l_Categoria.place(x=10, y=40)

#pegando categorias-------------------------------------------------------------------------------------

combo_categoria_gasto = ttk.Combobox(frameGastos, width=10, font="Ivy 12")
combo_categoria_gasto['values'] = (ver_categorias())
combo_categoria_gasto.place(x=110,y=41)

#gastos-------------------------------------------------------------------------------------
#label calendario
l_cal_gasto = Label(frameGastos, text="Data", height=1, anchor=NW, font='Ivy 12', bg="black", fg="white")
l_cal_gasto.place(x=10, y=80)

#entry calendario
e_cal_gastos = DateEntry(frameGastos, width=12, bg='darkblue',font='Ivy 12', fg='white', borderwidth=2, year=2023)
e_cal_gastos.place(x=110, y=81)

#valor-------------------------------------------------------------------------------------
l_val_gasto = Label(frameGastos, text="Valor", height=1, anchor=NW, font='Ivy 12', bg="black", fg="white")
l_val_gasto.place(x=10, y=120)

e_val_gasto = Entry(frameGastos, width=14, justify='left', relief='solid',font='Ivy 12' )
e_val_gasto.place(x=110, y=121)

#Botao inserir
img_add_gasto = Image.open("img//img_add.png")
img_add_gasto = img_add_gasto.resize((20,20))
img_add_gasto = ImageTk.PhotoImage(img_add_gasto)

botao_add_gasto = Button(frameGastos, command=inserir_um_gasto, image=img_add_gasto, text=" Adicionar".upper(), width=80, compound=LEFT, padx=0, relief=FLAT, anchor=NW, font="Ivy 7 bold", bg="black", fg="white", overrelief=RIDGE)
botao_add_gasto.place(x=110,y=151)

#botao excluir registro

img_delete_gasto = Image.open("img//img_delete.jpg")
img_delete_gasto = img_delete_gasto.resize((20,20))
img_delete_gasto = ImageTk.PhotoImage(img_delete_gasto)

botao_delete = Button(frameGastos,command=deletar_registro, image=img_delete_gasto, text=" Excluir registro selecionado".upper(), width=200, compound=LEFT, padx=0, relief=FLAT, anchor=NW, font="Ivy 7 bold", bg="black", fg="white", overrelief=RIDGE)
botao_delete.place(x=110,y=191)


#configurando receitas-----------------------------------------------------------------------------------------

l_info = Label(frameReceitas, text="Insira uma receita", height=1, anchor=NW, font='verdana 10 bold', bg="black", fg="white")
l_info.place(x=10, y=10)

#label calendario
l_cal_receita = Label(frameReceitas, text="Data", height=1, anchor=NW, font='Ivy 12', bg="black", fg="white")
l_cal_receita.place(x=10, y=40)

#entry calendario
e_cal_receita = DateEntry(frameReceitas, width=12, bg='darkblue',font='Ivy 12', fg='white', borderwidth=2, year=2023)
e_cal_receita.place(x=110,y=41)

#valor-------------------------------------------------------------------------------------
#label valor
l_val_gasto = Label(frameReceitas, text="Valor", height=1, anchor=NW, font='Ivy 12', bg="black", fg="white")
l_val_gasto.place(x=10, y=80)
#entry valor
e_val_receita = Entry(frameReceitas, width=14, justify='left', relief='solid',font='Ivy 12' )
e_val_receita.place(x=110,y=81)

#botao inserir
botao_add_receita = Button(frameReceitas,command=inserir_uma_receita, image=img_add_gasto, text=" Adicionar".upper(), width=80, compound=LEFT, padx=0, relief=FLAT, anchor=NW, font="Ivy 7 bold", bg="black", fg="white", overrelief=RIDGE)
botao_add_receita.place(x=110,y=121)

#nova categoria
l_info = Label(frameReceitas, text="Insira nova categoria", height=1, anchor=NW, font='verdana 10 bold', bg="black", fg="white")
l_info.place(x=10, y=160)

#label nova categoria
l_nova_categoria = Label(frameReceitas, text="Categoria", height=1, anchor=NW, font='Ivy 12', bg="black", fg="white")
l_nova_categoria.place(x=10, y=190)
#entry nova categoria
e_nova_categoria = Entry(frameReceitas, width=14, justify='left', relief='solid',font='Ivy 12' )
e_nova_categoria.place(x=110,y=191)

#botao add nova categoria
botao_add_nova_categoria = Button(frameReceitas, image=img_add_gasto, text=" Adicionar".upper(), width=80, compound=LEFT, padx=0, relief=FLAT, anchor=NW, font="Ivy 7 bold", bg="black", fg="white", overrelief=RIDGE, command=inserir_nova_categoria)
botao_add_nova_categoria.place(x=110,y=221)

#botao excluir categoria



botao_delete_categoria = Button(frameReceitas,command=deletar_uma_categoria, image=img_delete_gasto, text=" Excluir categoria".upper(), width=200, compound=LEFT, padx=0, relief=FLAT, anchor=NW, font="Ivy 7 bold", bg="black", fg="white", overrelief=RIDGE)
botao_delete_categoria.place(x=110,y=251)


janela.mainloop()




