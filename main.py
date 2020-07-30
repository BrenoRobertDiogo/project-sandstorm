from flask import Flask, request, abort, redirect, url_for, render_template, make_response
import flask
import bibliotecas
from pprint import pprint
from belvo.client import Client
import json

app = Flask(__name__, static_folder='templates')

msgError = '<h1> Método ou site não encontrado <h1> <script>window.alert()</script>'

#Função para logar
def transformers(idPessoa, senhaPessoa):
    return Client(
		idPessoa,
		senhaPessoa,
		"https://sandbox.belvo.co"
	)

#Aba de login
@app.route('/login', methods=['POST', 'GET'])
def login():
    resp = make_response(render_template('login.html'))
    if request.method=='GET':
        return resp    #Entra na página de login
    else:
        return msgError#Mensagem de erro se for POST

#Aba de dados, onde a pessoa vai ver os principais dados dela
@app.route('/dados', methods=['POST', 'GET'])
def dados():
    if request.method=='GET':               #Caso não esteja recebendo informação
        return render_template('index.html')#Retorna página dos dados
    else:
        ###Pegando os dados do formulário###
        nome = request.form['idPessoa']             #id
        senha = request.form['senha']               #senha
        client = bibliotecas.chamar(nome, senha)    #Cazendo o client
        ###instituições###
        instituicoes = bibliotecas.ver_instituicoes(client)#Instituições
        tamanhoInst = len(instituicoes)                    #Quantas instituições tem

        ####DADOS PARA CRIAR OS COOKIES####
        
        #TRANSAÇÕES
        transacoes  = bibliotecas.transacoes(client)#Puxando as transações
        tamanhoTran = len(transacoes)               #Quantas transações tem
        
        #LINK
        verLink = bibliotecas.ver_link(client)      #Puxando os links e informações
        tamanhoVerLink = len(verLink)               #Quandos links tem
        
        #CONTAS
        contas = bibliotecas.retornaContas(client)  #Contas que tem la
        tamanhoContas = len(contas)                 #Quantas contas tem

        ###Fazendo os cookies###
        resp = make_response(render_template('index.html',
                                            nome=contas,                     #Contas que tem
                                            tamanho=tamanhoContas,           #Tamanho da conta
                                            instituicoes = instituicoes,     #Instituições
                                            numero_instituicoes=tamanhoInst))#Site a ser retornado
        
        resp.set_cookie('idPessoa', json.dumps(nome))    #id
        resp.set_cookie('senhaPessoa', json.dumps(senha))#senha
        """#######################COOKIES###############"""
        
        ##############RETORNANDO INSTITUIÇÕES##########
        [resp.set_cookie(f'isnt{x}', json.dumps(instituicoes[x])) for x in range(tamanhoInst)]
        resp.set_cookie('lenInst', json.dumps(tamanhoInst))
        
        #######################VER LINK################
        [resp.set_cookie(f'verLink{x}', json.dumps(verLink[x])) for x in range(tamanhoVerLink)]
        resp.set_cookie('lenVerLink', json.dumps(tamanhoVerLink))
        
        ###############RETORNAR AS CONTAS##############
        [resp.set_cookie(f'conta{x}', json.dumps(contas[x])) for x in range(tamanhoContas)]
        resp.set_cookie('lenConta', json.dumps(tamanhoContas))

        ###############RETORNAR AS TRANSAÇÕES##########
        [resp.set_cookie(f'trans{x}', json.dumps(transacoes[x])) for x in range(tamanhoTran)]
        resp.set_cookie('lenTrans', json.dumps(tamanhoTran))

        return resp

#Aba de rota, direcionamento
@app.route('/rota', methods=['POST', 'GET'])
def rota():
    cookie1 = request.cookies.get('idPessoa')
    cookie2 = request.cookies.get('senhaPessoa')
    
    return f"{json.loads(cookie1)}, {json.loads(cookie2)}"

#Aba de links
@app.route("/link",methods=["POST", "GET"])
def link():
    if request.method == "GET":
        ####instituições e link e cadastro
        ##Instituições
        tamanhoInst  = int(request.cookies.get(f'lenInst'))#Pega quantas instituições tem do cookie
        instituicoes = [json.loads(request.cookies.get(f'isnt{instituicao}')) for instituicao in range(tamanhoInst)]#Instituições sendo adiciondas
        
        ##Link
        tamanhoVerLink = int(request.cookies.get('lenVerLink'))#Quantos links tem, sendo puxado pelos cookies
        links = [json.loads(request.cookies.get(f'verLink{link}')) for link in range(tamanhoVerLink)]#Adicionando os cookies na variável
        ##Cadastro informações

        nome  = request.cookies.get('idPessoa')   #ID da pessoa
        senha = request.cookies.get('senhaPessoa')#Senha da pessoa

        ##Passando as informações##

        return render_template("link.html",
            id=nome,                          #Nome
            senha=senha,                      #Senha
            links = links,                    #Links
            instituicoes=instituicoes,        #Instituições
            numero_instituicoes = tamanhoInst,#Quantas instituições tem
            numero_links = tamanhoVerLink)    #Quantos links tem

#Aba de transações
@app.route("/transacoes",methods=["POST", "GET"])
def transacoes():
     
    nome  = request.cookies.get('idPessoa')   #ID da pessoa
    senha = request.cookies.get('senhaPessoa')#Senha da pessoa

    tamanhoTransacoes = int(request.cookies.get('lenVerLink')) #Quantas transações houveram
    transacoes  = [json.loads(request.cookies.get(f'trans{transacao}')) for transacao in range(tamanhoTransacoes)]#Todas as transações
    idPessoa    = json.loads(request.cookies.get('idPessoa'))
    senhaPessoa = json.loads(request.cookies.get('senhaPessoa'))

    #return transacoes[0]
    return render_template("transacoes.html", #Página
        numero_transacoes = tamanhoTransacoes,#Quantas transações são
        transacoes = transacoes,              #Dados das transações
        id         = idPessoa,                #Nome de ID
        senha      = senhaPessoa              #Senha da pessoa
        )

#Aba de contato
@app.route('/contato')
def contato():
    
    return render_template('contato.html')
    

if __name__=='__main__':
    app.run(debug=True)