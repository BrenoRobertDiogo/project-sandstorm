from flask import Flask, request, abort, redirect, url_for, render_template, make_response
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
        return render_template('login.html')
    else:
        return msgError

@app.route('/dados', methods=['POST', 'GET'])
def dados():
    if request.method=='GET':
        return render_template('index.html')
    else:
        resp = make_response(render_template('login.html'))
        nome = request.form['idPessoa']
        senha = request.form['senha']
        client = bibliotecas.chamar(nome, senha)
        contas = bibliotecas.retornaContas(client)
        tamanho = len(contas)
        
        resp.set_cookie('idPessoa', contas)
        resp.set_cookie('senhaPessoa', nome)
        return render_template('index.html', nome=contas, tamanho=tamanho)#bibliotecas.retornaContas(client)#render_template('index.html')

@app.route('/rota', methods=['POST', 'GET'])
def rota():
    return f"{request.cookies.get('idPessoa'), {request.cookies.get('client')}}"

if __name__=='__main__':
    app.run(debug=True)