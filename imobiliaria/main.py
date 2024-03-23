# Acrescentando as extenções previamente aplicadas na VM
from flask import Flask, render_template,request
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
def alugel():
    dic = diccionarios.mostrar_imoveis("aluguel")
    return render_template('index.html', outro=dic)

# Visão de cada imovel individual 
@app.route('/imovel/<int:id>')
def imovel(id):
    
    imovel = diccionarios.mostrar_imovel(id)
    imovel['id'] = id
    return render_template('imovel.html', **imovel ) 

app.run(debug=True)
