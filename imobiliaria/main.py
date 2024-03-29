# Acrescentando as extenções previamente aplicadas na VM
from flask import Flask, render_template,request, redirect, url_for
from pathlib import Path

import gspread
import diccionarios

file_path = Path('../') / 'imobiliaria-koru-2.json'

gc = gspread.service_account(file_path)
sp = gc.open('contato-imobiliaria')

spContacts = sp.get_worksheet(0)

app = Flask(__name__)

# Inicialização do Flask
app = Flask(__name__)

#  Home do site (Read)
@app.route('/')
def index():
    dic = diccionarios.mostrar_imoveis("todos")
    return render_template('index.html', outro=dic)

#  Filtro dos imóveis 'Venda' (Read)
@app.route('/venda')
def venda():
    dic = diccionarios.mostrar_imoveis("venda")
    return render_template('index.html', outro=dic)

#  Filtro dos imóveis 'Aluguel' (Read)
@app.route('/aluguel')
def aluguel():
    dic = diccionarios.mostrar_imoveis("aluguel")
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
            diccionarios.criar_imovel(imovel)
            return redirect("/")
        else:
            imovel = {}
            imovel['imagem'] = request.form["imagem"]
            imovel['tipo'] = request.form['tipo']
            imovel['cidade'] = request.form['cidade']
            imovel['endereco'] = request.form['endereco']
            imovel['descricao'] = request.form['descricao']
            imovel['valor'] = request.form['valor']
            diccionarios.criar_imovel(imovel)
            return redirect("/")
    else:
        return render_template("cadastro.html") 

# Função para remover imóveis (Delete)
@app.route('/remover/<int:id>')
def remover_imovel(id):
    diccionarios.apagar_imoveis(id)
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
        diccionarios.modif_imoveis(id,imovel)
        return redirect("/")
    else:
        imovel = diccionarios.mostrar_imovel(id)
        imovel['id'] = id
        return render_template('cadastro.html',**imovel)

# Função para mostrar de cada imovel individualmente (read)
@app.route('/imovel/<int:id>', methods=['GET', 'POST'])
def imovel(id):

    if request.method == 'POST':  
    
        if "excluir" in request.form:
            diccionarios.apagar_imoveis(id)
            return redirect(url_for('index'))
    else: 
        imovel = diccionarios.mostrar_imovel(id)
        imovel['id'] = id
        return render_template('imovel.html', **imovel )

app.run(debug=True)