import sqlite3 as lite

con = lite.connect('banco-de-dados//controle.db')

#criando tabelas

# with con:
#     cur = con.cursor()
#     cur.execute('CREATE TABLE Usuarios(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT, login TEXT, senha TEXT)')

# with con:
#     cur = con.cursor()
#     cur.execute('CREATE TABLE Categorias(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)')

# with con:
#     cur = con.cursor()
#     cur.execute('CREATE TABLE Receitas(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor DECIMAL)')

# with con:
#     cur = con.cursor()
#     cur.execute('CREATE TABLE Gastos(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, retirado_em DATE, valor DECIMAL)')

# with con:
#     cur = con.cursor()
#     cur.execute('CREATE TABLE Despesas(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, valor DECIMAL)')

# with con:
#     cur = con.cursor()
#     cur.execute('CREATE TABLE Renda(id INTEGER PRIMARY KEY AUTOINCREMENT, valor DECIMAL)')



# with con:
#     cur = con.cursor()
#     i=[52]
#     query = 'DELETE FROM Gastos WHERE id=?'
#     cur.execute(query,i)

