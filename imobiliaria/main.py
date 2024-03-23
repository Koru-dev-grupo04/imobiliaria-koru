# Acrescentando as extenções previamente aplicadas na VM
from flask import Flask, render_template,request, redirect, url_for

import gspread
import diccionarios

# Inicialização do Flask
app = Flask(__name__)

#  Home do site
@app.route('/')
def index():
    dic = diccionarios.mostrar_imoveis("todos")
    return render_template('index.html', outro=dic)

@app.route('/venda')
def venda():
    dic = diccionarios.mostrar_imoveis("venda")
    return render_template('index.html', outro=dic)

@app.route('/aluguel')
def aluguel():
    dic = diccionarios.mostrar_imoveis("aluguel")
    return render_template('index.html', outro=dic)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/adicionar', methods= ['GET','POST'])
def adiciona_imovel():
    if request.method == 'POST':
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

@app.route('/remover/<int:id>')
def remover_imovel(id):
    diccionarios.apagar_imoveis(id)
    return redirect('/')

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

# Visão de cada imovel individual 
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

# Visão de criação de imoveis 
@app.route('/novo_imovel')

def criar_imovel():

    return render_template('criar.html' )  

app.run(debug=True)
 