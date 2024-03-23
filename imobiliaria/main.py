# Acrescentando as extenções previamente aplicadas na VM
from flask import Flask, render_template, request, redirect, url_for
import gspread
import diccionarios

# Inicialização do Flask
app = Flask(__name__)

#  Home do site
@app.route('/')
def index():
    dic = diccionarios.mostrar_imoveis()
    return render_template('index.html', outro=dic)

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
 