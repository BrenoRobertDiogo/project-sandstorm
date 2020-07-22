from flask import Flask, request, abort, redirect, url_for, render_template, make_response
import bibliotecas
from pprint import pprint
from belvo.client import Client
import json
import random
import jsonify
import json

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
        ###Pegando os dados do formulário
        nome = request.form['idPessoa']           #id
        senha = request.form['senha']             #senha
        client = bibliotecas.chamar(nome, senha)  #Cazendo o client
        contas = bibliotecas.retornaContas(client)#Contas que tem la
        tamanho = len(contas)                     #Quantas contas tem
        
        ###Fazendo os cookies
        resp = make_response(render_template('index.html', nome=contas, tamanho=tamanho))#Site a ser retornado
        resp.set_cookie('idPessoa', json.dumps(nome))#id
        resp.set_cookie('senhaPessoa', json.dumps(senha))#senha

        return resp
@app.route('/rota', methods=['POST', 'GET'])
def rota():
    cookie1 = request.cookies.get('idPessoa')
    cookie2 = request.cookies.get('senhaPessoa')
    return f"{cookie1}, {cookie2}"


"""@app.route('/dados', methods=['POST', 'GET'])
def dados():"""


@app.route("/link",methods=["POST"])

def link():
    if request.method == "POST":
        login = request.form.to_dict()
        
        nome = login["idPessoa"]
        senha = login["senha"]
        
        client = bibliotecas.chamar(nome,senha)

        instituicoes = bibliotecas.ver_instituicoes(client)

        link = bibliotecas.ver_link(client)

       
        
        return render_template("link.html",id=nome,senha=senha,links = link,instituicoes=instituicoes,
    numero_instituicoes = len(instituicoes),numero_links=len(link))

@app.route("/",methods=["POST"])
def transacoes():
    login = request.form.to_dict()
    
    nome = login["idPessoa"]
    senha = login["senha"]
    
    client = Client(f"{nome}", 
f"{senha}", 
"https://sandbox.belvo.co")
    transacoes = []

    [transacoes.append(x) for x in client.Transactions.list()]

    return render_template("transactions.html",numero_transacoes = len(transacoes),transacoes = transacoes)

if __name__=='__main__':
    app.run(debug=True)



