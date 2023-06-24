#importando sqlite
import sqlite3 as lite

#criando conexão
con = lite.connect('banco-de-dados//controle.db')

#comandos de inserção ---------------------------------------------------------------------------------------

#função inserir categoria
def inserir_categoria(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Categorias(nome) VALUES(?)"
        cur.execute(query,i)

#função inserir usuario
def inserir_usuario(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Usuarios(nome, email, login, senha) VALUES(?,?,?,?)"
        cur.execute(query,i)

#função inserir receita
def inserir_receita(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Receitas(categoria, adicionado_em, valor) VALUES(?,?,?)"
        cur.execute(query,i)

#função inserir gasto
def inserir_gasto(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Gastos(categoria, retirado_em, valor) VALUES(?,?,?)"
        cur.execute(query,i)

#função inserir despesa
def inserir_despesa(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Despesas(nome, categoria, valor) VALUES(?,?,?)"
        cur.execute(query,i)


#funcao inserir renda
def inserir_renda():
    with con:
        cur = con.cursor()
        cur.execute('INSERT INTO Renda(valor) VALUES(1600.10)')


#comandos para deletar ---------------------------------------------------------------------------------------
def deletar_receita(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Receitas WHERE id=?"
        cur.execute(query, i)

def deletar_gasto(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Gastos WHERE id=?"
        cur.execute(query, i)


def deletar_categoria(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Categorias WHERE nome=?"
        cur.execute(query, i)


#consultar dados-----------------------------------------------------------------------------------

#exibir categorias

def ver_categorias():
    lista_itens = []
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Categorias')
        lista = cur.fetchall()
        for i in lista:
            lista_itens.append(i[1])
    return lista_itens
#exibir receitas

def ver_receitas():
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Receitas')
    return cur.fetchall()

#exibir gastos

def ver_gastos():
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Gastos')
    return cur.fetchall()


#exibir despesas

def ver_despesas():
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Despesas')
    return cur.fetchall()
#exibir renda
def ver_renda():
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Renda')
    return cur.fetchall()

def tabela():
    receitas = ver_receitas()
    gastos = ver_gastos()
    lista_itens = []
    for i in receitas:
        lista_itens.append(i)
    for i in gastos:
        lista_itens.append(i)
    return lista_itens

#pegar valores por categoria
def valores_categorias():
    lista_valores = []
    categorias = ver_categorias()
    gastos = ver_gastos()
    show_categoria = []
    show_gasto = []
    for i in categorias:
        with con:
            cur=con.cursor()
            query='SELECT valor FROM Gastos WHERE categoria=?'
            cur.execute(query,[i])
            dados = cur.fetchall()
            lista = []
            for i in dados:
                lista.append(i[0])
            valor_total= sum(lista)
            lista_valores.append(valor_total)
        c=0
        for i in lista_valores:
            if i!=0:
                show_gasto.append(i)
                show_categoria.append(categorias[c])
                c+=1
    return lista_valores, show_categoria,show_gasto

print(valores_categorias())

#porcentagem renda gasta em despesas
def valor_porcentagem():
    try:
        porcentagem = (total_gastos() * 100)/total_renda()
    except:
        porcentagem = 0
    return porcentagem

#total renda
def total_renda():
    receitas = ver_receitas()
    lista_valores = []
    for i in receitas:
        lista_valores.append(i[3])
    total_renda = sum(lista_valores)
    return total_renda
#total gastos
def total_gastos():
    receitas = ver_gastos()
    lista_valores = []
    for i in receitas:
        lista_valores.append(i[3])
    total_gastos = sum(lista_valores)
    return total_gastos

#Saldo atual
def saldo_atual():
    saldo = (total_renda()-total_gastos())
    return saldo


