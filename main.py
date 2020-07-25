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
        

        instituicoes = bibliotecas.ver_instituicoes(client)
        tamanhoInst = len(instituicoes)
        #Contas que tem la
        contas = bibliotecas.retornaContas(client)
        tamanhoContas = len(contas)               #Quantas contas tem

        instituicoes = bibliotecas.ver_instituicoes(client)
        ###Fazendo os cookies###
       #valor = str(contas[0])
        #return valor
<<<<<<< HEAD
        resp = make_response(render_template('index.html', instituicoes = instituicoes,tamanho=tamanhoInst))#Site a ser retornado
=======
        resp = make_response(render_template('index.html', nome=contas, tamanho=tamanhoContas,instituicoes = instituicoes,numero_instituicoes=len(instituicoes) ))#Site a ser retornado
>>>>>>> bf4ebba3426f7cd964d5c7a45044124ad9464c3f
        resp.set_cookie('idPessoa', json.dumps(nome))    #id
        resp.set_cookie('senhaPessoa', json.dumps(senha))#senha

        """#######################COOKIES###############"""
        ##########RETORNANDO CONTAS COMO COOKIE######
        [resp.set_cookie(f'id{x}', json.dumps(str(contas[x]))) for x in range(tamanhoContas)]
        ##############RETORNANDO TRANSAÇÕES##########
        #[resp.set_cookie(f'tran{x}', json.dumps(str(transacoes[x]))) for x in range(tamanhoTran)]


        cookie1 = request.cookies.get('idPessoa')
        cookie3 = request.cookies.get('teste')
        #resp.set_cookie('clientPessoa', json.dumps(client))
        return resp
@app.route('/rota', methods=['POST', 'GET'])
def rota():
    cookie1 = request.cookies.get('idPessoa')
    cookie2 = request.cookies.get('senhaPessoa')
    return f"{cookie1}, {cookie2}"


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