from flask import Flask, request, abort, redirect, url_for, render_template
import bibliotecas
from pprint import pprint
from belvo.client import Client
import json
import random

app = Flask(__name__, static_folder='templates')

msgError = '<h1> Método ou site não encontrado <h1> <script>window.alert()</script>'



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='GET':
        return render_template('link.html')
    else:
        return msgError

"""@app.route('/dados', methods=['POST', 'GET'])
def dados():"""

@app.route("/transacoes",methods=["POST"])

def transacoes():
    login = request.form.to_dict()
    
    nome = login["id"]
    senha = login["pass"]
    
    client = Client(f"{nome}", 
f"{senha}", 
"https://sandbox.belvo.co")
    transacoes = []

    [transacoes.append(x) for x in client.transactions.list()]

    return render_template("transactions.html",numero_transacoes = len(transacoes),transacoes = transacoes)

if __name__=='__main__':
    app.run(debug=True)



