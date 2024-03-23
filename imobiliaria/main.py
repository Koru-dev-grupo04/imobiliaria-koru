# Acrescentando as extenções previamente aplicadas na VM
from flask import Flask, render_template,request, redirect
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

@app.route('/adm')
def adm():
    dic = diccionarios.mostrar_imoveis("todos")
    return render_template('adm.html', outro=dic)

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
    return redirect('/adm')



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
@app.route('/imovel/<int:id>')
def imovel(id):
    
    imovel = diccionarios.mostrar_imovel(id)
    imovel['id'] = id
    return render_template('imovel.html', **imovel ) 

app.run(debug=True)
