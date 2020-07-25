from flask import Flask, request, abort, redirect, url_for, render_template, make_response
import bibliotecas
from pprint import pprint
from belvo.client import Client
import json
import random

app = Flask(__name__, static_folder='templates')

msgError = '<h1> Método ou site não encontrado <h1> <script>window.alert()</script>'

def transformers(idPessoa, senhaPessoa):
    return Client(
		idPessoa,
		senhaPessoa,
		"https://sandbox.belvo.co"
	)


@app.route('/login', methods=['POST', 'GET'])
def login():
    resp = make_response(render_template('login.html'))
    if request.method=='GET':
        return resp#render_template('login.html')
    else:
        return msgError

@app.route('/dados', methods=['POST', 'GET'])
def dados():
    if request.method=='GET':
        return render_template('index.html')
    else:
        ###Pegando os dados do formulário
        nome = request.form['idPessoa']           #id
        senha = request.form['senha']             #senha
        client = bibliotecas.chamar(nome, senha)  #Cazendo o client
        #x = [x for x in str(client)]
        #return str(x)
        contas = bibliotecas.retornaContas(client)#Contas que tem la
        tamanho = len(contas)                     #Quantas contas tem
        
        #return str(contas)
        ###Fazendo os cookies
        valor = str(contas[0])
        #return valor
        resp = make_response(render_template('index.html', nome=contas, tamanho=tamanho))#Site a ser retornado
        resp.set_cookie('idPessoa', json.dumps(nome))#id
        resp.set_cookie('senhaPessoa', json.dumps(senha))#senha
        resp.set_cookie('teste', json.dumps(valor))#json.dumps(contas[0]))
        for x in range(tamanho):
            resp.set_cookie(f'id{x}', json.dumps(str(contas[x])))
        cookie1 = request.cookies.get('idPessoa')
        cookie3 = request.cookies.get('teste')
        #resp.set_cookie('clientPessoa', json.dumps(client))
        return resp
@app.route('/rota', methods=['POST', 'GET'])
def rota():
    cookie1 = request.cookies.get('idPessoa')
    cookie2 = request.cookies.get('senhaPessoa')
    cookie3 = request.cookies.get('teste')
    return f"{cookie1}, {cookie2}, {cookie3}"


@app.route("/link",methods=["POST", "GET"])

def link():
    if request.method == "GET":
        
        
        nome = request.cookies.get('idPessoa')
        senha = request.cookies.get('senhaPessoa')
        
        client = bibliotecas.chamar(nome,senha)

        instituicoes = bibliotecas.ver_instituicoes(client)

        link = bibliotecas.ver_link(client)
        
        return render_template("link.html",id=nome,senha=senha,links = link,instituicoes=instituicoes,
    numero_instituicoes = len(instituicoes),numero_links=len(link))

@app.route("/transacoes",methods=["POST", "GET"])
def transacoes():
    nome = request.cookies.get('idPessoa')
    senha = request.cookies.get('senhaPessoa')
    
    client = transformers(nome, senha)
    transacoes = [transacao for transacao in client.Transactions.list()]
    return render_template("transacoes.html",numero_transacoes = len(transacoes),transacoes = transacoes)


@app.route('/contato')
def contato():
    
    return render_template('contato.html')
    

if __name__=='__main__':
    app.run(debug=True)