from flask import Flask, request, jsonify , render_template, redirect
from pathlib import Path
from imovel import Imovel
import gspread
import sqlite3
import diccionarios

from imovel import Imovel
from db_connector import DBconnector

#-- Google Spreadsheet -------------------------------------------------------------------------------

# Configuração do caminho para o arquivo Json do google spreadsheets
# Está sendo usada a biblioteca pathlib para permitir compatibilidade em diversos SO
file_path = Path('../') / 'imobiliaria-koru-2.json'

gc = gspread.service_account(file_path)
sp = gc.open('contato-imobiliaria')

spContacts = sp.get_worksheet(0)

#-- Inicialização do App ---------------------------------------------------------------

app = Flask(__name__)

#-- Setup do caminho do banco de dados ---------------------------------------------------

DATABASE = Path('../') / 'data_imoveis.db'

db = DBconnector(DATABASE)

#--API---------------------------------------------------------------------------------------------
    
#CREATE
@app.route("/api/imoveis", methods = ["POST"])
def create_imovel():
    data = request.get_json()
    imovel = Imovel(
        descricao= data['descricao'],
        endereco = data['endereco'],
        valor = data['valor'],
        cidade = data['cidade'],
        tipo = data['tipo'],
        imagem = data['imagem']
        )
    imovel.save(db.connect())
    return jsonify(imovel.to_dict())


#READ
@app.route("/api/imoveis", methods=['GET'])
def get_imoveis():
    imoveis = Imovel.get_all(db.connect())
    return jsonify(imoveis)

@app.route("/api/imoveis/<int:id_imovel>", methods=['GET'])
def get_imovel(id_imovel):
    imovel = Imovel.get_by_id(id_imovel,db.connect())
    if imovel:
        return jsonify(imovel.to_dict())
    else:
        return jsonify({"Erro": "Imóvel não localizado!"}), 404

#UPDATE 
@app.route("/api/imoveis/<int:id_imovel>", methods=['PUT'])
def update_imovel(id_imovel):
    data = request.get_json()
    imovel = Imovel.get_by_id(id_imovel,db.connect())
    if imovel:
        imovel.descricao= data['descricao']
        imovel.endereco = data['endereco']
        imovel.valor = data['valor']
        imovel.cidade = data['cidade']
        imovel.tipo = data['tipo']
        imovel.imagem = data['imagem']
        imovel.save(db.connect())
        return jsonify(imovel.to_dict())
    else:
        return jsonify({"Erro":"Imóvel não encontrado"}), 404


#DELETE
@app.route("/api/imoveis/<int:id_imovel>", methods=['DELETE'])
def delete_imovel(id_imovel):
    imovel = Imovel.get_by_id(id_imovel,db.connect())
    if imovel:
        imovel.delete(db.connect())
        return "", 204
    else:
        return jsonify({"Erro":"Imóvel não encontrado!"}), 404

#-- Website ----------------------------------------------------------------------------------

# Função que se conecta ao banco de dados
def get_db():
    db = sqlite3.connect(DATABASE)
    return db

# Função para criar uma nova tabela chamada IMOVEIS no banco de dados 
def create_table():
    db = get_db()
    cursor = db.cursor()
    
    # Define a estrutura da tabela
    create_table_sql = '''
        CREATE TABLE IF NOT EXISTS IMOVEIS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            DESCRICAO TEXT NOT NULL,
            ENDERECO TEXT NOT NULL,
            VALOR INTEGER NOT NULL,
            CIDADE VARCHAR(50) NOT NULL,
            TIPO VARCHAR(20) NOT NULL,
            IMAGEM TEXT NOT NULL
        )
    '''
    # Executa o comando SQL para criar a tabela
    cursor.execute(create_table_sql)
    
    # Commit as mudanças
    db.commit()
    
    # Fechar o cursor e a conexão com o banco de dados
    cursor.close()
    db.close()



def is_table_empty():
    db = get_db()
    cursor = db.cursor()

    # Define a query SQL para contar as linhas na tabela.
    count_query = 'SELECT COUNT(*) FROM IMOVEIS'

    # Executa a query SQL
    cursor.execute(count_query)

    # Fetch the result
    row_count = cursor.fetchone()[0]

    # Fecha o cursor e a conexão com o banco de dados.
    cursor.close()
    db.close()

    # Retorna verdadeiro se a tabela é vazia (row_count is 0), caso contrário, retorna falso.
    return row_count == 0

def populate_table():
    db = get_db()
    cursor = db.cursor()
    # Define a query SQL de inserção do imóvel cadastrado no dicionário
    sql_insert = '''
        INSERT INTO IMOVEIS (
        IMAGEM, TIPO, CIDADE, ENDERECO, DESCRICAO, VALOR
        ) VALUES (?, ?, ?, ?, ?, ?)
    '''
    for key,value in diccionarios.imoveis.items():
        cursor.execute(sql_insert,(
            value['imagem'],
            value['tipo'],
            value['cidade'],
            value['endereco'],
            value['descricao'],
            value['valor'],
            ))
    db.commit()
    cursor.close()
    db.close()


# Seleciona um imóvel do banco de dados
def seleciona_imovel(id):
    db = get_db()
    cursor = db.cursor()
    sql_select_unico = '''
        SELECT * FROM IMOVEIS WHERE ID = ?
'''
    cursor.execute(sql_select_unico,(id,))
    imovel_valores = cursor.fetchone()
    imovel_chaves = ('id','descricao', 'endereco', 'valor', 'cidade', 'tipo', 'imagem')
    imovel = dict(zip(imovel_chaves,imovel_valores))
    return imovel

# Mostra os imóveis do banco de dados
def mostra_imoveis(tipo=0):
    db = get_db()
    cursor = db.cursor()
    if tipo != 0:
        sql_select = '''
            SELECT * FROM IMOVEIS WHERE TIPO = ?
    '''
        cursor.execute(sql_select,(tipo,))
    else:
        sql_select = '''
            SELECT * FROM IMOVEIS
    '''
        cursor.execute(sql_select)

    imoveis_valores = cursor.fetchall()
    cursor.close()
    db.close()
    imovel_chaves = ('id','descricao', 'endereco', 'valor', 'cidade', 'tipo', 'imagem')
    imoveis = {}
    for imovel_valores in imoveis_valores:
        imoveis[imovel_valores[0]] = dict(zip(imovel_chaves,imovel_valores))
    return imoveis

# Deleta um imóvel do banco de dados
def deleta_imovel(id):
    db = get_db()
    cursor = db.cursor()
    # Define a query SQL de inserção do imóvel cadastrado no dicionário
    sql_delete = '''
        DELETE FROM IMOVEIS WHERE ID = ?
    '''
    cursor.execute(sql_delete,(id, ))
    db.commit()
    cursor.close()
    db.close()
    print(mostra_imoveis())


# Adiciona um novo imóvel ao banco de dados
def cria_imovel(imovel):
    db = get_db()
    cursor = db.cursor()
    # Define a query SQL de inserção do imóvel cadastrado no dicionário
    sql_insert = '''
        INSERT INTO IMOVEIS (
        IMAGEM, TIPO, CIDADE, ENDERECO, DESCRICAO, VALOR
        ) VALUES (?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(sql_insert,(
            imovel['imagem'],
            imovel['tipo'],
            imovel['cidade'],
            imovel['endereco'],
            imovel['descricao'],
            imovel['valor'],
            ))
    db.commit()
    cursor.close()
    db.close()    
    
# Atualiza um imóvel no banco de dados
def atualiza_imovel(id,imovel):
    db = get_db()
    cursor = db.cursor()
    # Define a query SQL de atualização do imóvel cadastrado no dicionário
    sql_update = '''
        UPDATE IMOVEIS 
        SET 
        IMAGEM = ?, TIPO = ?, CIDADE = ?, ENDERECO = ?, DESCRICAO = ?, VALOR = ?
        WHERE ID = ?
    '''
    cursor.execute(sql_update,(
            imovel['imagem'],
            imovel['tipo'],
            imovel['cidade'],
            imovel['endereco'],
            imovel['descricao'],
            imovel['valor'],
            id
            ))
    db.commit()
    cursor.close()
    db.close() 


#  Home do site (Read)
@app.route('/')
def index():
    dic = mostra_imoveis()
    return render_template('index.html', outro=dic)

@app.route("/sobre")
def sobre():
    return render_template('sobre.html')

#  Filtro dos imóveis 'Venda' (Read)
@app.route('/venda')
def venda():
    dic = mostra_imoveis("Venda")
    return render_template('index.html', outro=dic)

#  Filtro dos imóveis 'Aluguel' (Read)
@app.route('/aluguel')
def aluguel():
    dic = mostra_imoveis("Aluguel")
    return render_template('index.html', outro=dic)

# Site de contato
@app.route('/contato', methods=['POST','GET'])
def contato():
    if request.method == 'POST':
        spContacts.append_row([request.form['Nome'],request.form['Email'], request.form['Assunto'], request.form['Mensagem']])
        return redirect('/')
    else:
        return render_template('contato.html')

# Função para adicionar imóveis (Create)
@app.route('/adicionar', methods= ['GET','POST'])
def adiciona_imovel():
    if request.method == 'POST':
        imagem = request.form['imagem']
        if imagem == '':
            imovel = {}
            imovel['imagem'] = 'https://www.shutterstock.com/image-illustration/no-picture-available-placeholder-thumbnail-600nw-2179364083.jpg'
            imovel['tipo'] = request.form['tipo']
            imovel['cidade'] = request.form['cidade']
            imovel['endereco'] = request.form['endereco']
            imovel['descricao'] = request.form['descricao']
            imovel['valor'] = request.form['valor']
            cria_imovel(imovel)
            return redirect("/")
        else:
            imovel = {}
            imovel['imagem'] = request.form["imagem"]
            imovel['tipo'] = request.form['tipo']
            imovel['cidade'] = request.form['cidade']
            imovel['endereco'] = request.form['endereco']
            imovel['descricao'] = request.form['descricao']
            imovel['valor'] = request.form['valor']
            cria_imovel(imovel)
            return redirect("/")
    else:
        return render_template("cadastro.html") 

# Função para remover imóveis (Delete)
@app.route('/remover/<int:id>')
def remover_imovel(id):
    deleta_imovel(id)
    return redirect('/')

# Função para editar imóveis (Update)
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        imovel = {}
        imovel['imagem'] = request.form["imagem"]
        imovel['tipo'] = request.form['tipo']
        imovel['cidade'] = request.form['cidade']
        imovel['endereco'] = request.form['endereco']
        imovel['descricao'] = request.form['descricao']
        imovel['valor'] = request.form['valor']
        atualiza_imovel(id,imovel)
        return redirect("/")
    else:
        imovel = seleciona_imovel(id)
        return render_template('cadastro.html',**imovel)

# Função para mostrar de cada imovel individualmente (read)
@app.route('/imovel/<int:id>', methods=['GET', 'POST'])
def imovel(id):

    if request.method == 'POST':  
    
        if "excluir" in request.form:
            deleta_imovel(id)
            return redirect('/')
    else: 
        imovel = seleciona_imovel(id)
        return render_template('imovel.html',**imovel)

create_table()
if is_table_empty():
    populate_table()

app.run(debug=True)







