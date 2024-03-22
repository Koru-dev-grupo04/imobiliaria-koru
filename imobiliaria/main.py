# Acrescentando as extenções previamente aplicadas na VM
from flask import Flask, render_template,request
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
@app.route('/imovel/<int:id>')
def imovel(id):
    
    imovel = diccionarios.mostrar_imovel(id)
    imovel['id'] = id
    return render_template('imovel.html', **imovel ) 

app.run(debug=True)
