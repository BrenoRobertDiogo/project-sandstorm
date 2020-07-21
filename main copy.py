from flask import Flask, request, abort, redirect, url_for, render_template
import bibliotecas
from pprint import pprint
from belvo.client import Client
import json
import random

app = Flask(__name__, static_folder='templates')
#
with open(r'C:\Users\breno\OneDrive\Documentos\Scripts\Belvo\Testes\meusDados.json', 'r') as arquivo:
        mDados = json.load(arquivo)

client = Client(
    mDados['my-secret-key-id'], 
    mDados['my-secret-key'], 
    "https://sandbox.belvo.co"#"https://api.belvo.co"
)
nome = bibliotecas.retornaContas(client)
tamanho = range(0, len(nome), 3)

owners = client.Owners.create("8228337f-cc20-4122-a324-aa9d81c48e89")
tOwners = range(len(owners))

instituicoes = list(client.Institutions.list())


@app.route('/pessoas')
def pessoas():
    owners = client.Owners.create("1340ab36-f328-4710-b28d-fe046b3742ab")
    tOwners = range(len(owners))
    return render_template('pessoas.html', nomes=owners, tamanho=tOwners)

@app.route('/dev', methods=['GET', 'POST'])#, methods=['GET', 'POST'])
def enviarInf():
    msg = 'Ocorreu um erro'
    comando = f"window.alert()"
    nome = bibliotecas.retornaContas(client)
    tamanho = range(0, len(nome), 3)
    if request.method!='POST':
        return render_template('index.html', nome=nome, tamanho=tamanho)

    elif request.method=='POST':#:request.form['apagar']!=''
        #return '<script>window.alert("Ocorreu um erro")</script>'#request.form['enviar']
        if request.form['enviar']!='' and request.form['enviar'].lower() not in ['tudo', 'criar']:
            for valor in range(len(nome)):
                try:
                    if request.form['enviar'] in nome[valor]['id']:
                        bibliotecas.apagar(idPessoa=nome[valor]['id'], client=client)
                        bibliotecas.apagar(idPessoa=nome[valor+1]['id'], client=client)
                        bibliotecas.apagar(idPessoa=nome[valor+2]['id'], client=client)
                        return render_template('index.html', nome=nome, tamanho=tamanho, comando='')
                            #return f"{request.form['apagar']} foi apagado com Status: {x}"
        
                except TypeError:
                    return comando
        elif request.form['enviar']=='tudo':
            listaContas = [x for x in client.Accounts.list()]
            for x in range(len(listaContas)):
                #print('Apagando o ID: ', listaContas[x]['id'])
                client.Accounts.delete(listaContas[x]['id'])
            return ('IDs que tem agora: ', len(listaContas))

        elif request.form['enviar']=='criar':
            links = [x for x in client.Links.list()]
            aleatorio = random.randint(0, len(links))
            x = client.Accounts.create(links[aleatorio]['id'])


        
        return render_template('index.html', nome=nome, tamanho=tamanho, comando=comando)


            #x = bibliotecas.apagar(idPessoa=request.form['apagar'], client=client)
            #return f"{request.form['apagar']} foi apagado com Status: {x}"
        """elif request.form['enviar'] != '':
                                    y = bibliotecas.criar(client)
                                    return render_template('index.html', nome=nome, tamanho=tamanho)"""
            #return f"{request.form['criar']} foi criado com status: {pprint(y)}"

        




@app.route('/entrada')
def entrada():
    return render_template('entrada.html')


@app.route('/criar', methods=['GET', 'POST'])
def criar():
    return render_template('criar.html')
    
    
"""if request.form('criar')==True:
        return redirect(url_for('qualquercoisa'))"""
"""
enviamento de formulário
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        if request.form['username']=='admin' and request.form['pass']=='admin':
            return redirect(url_for('sucesso'))
        else:
            abort(401)
    else:
        abort(403)#Mostrar status caso erro"""

@app.route('/sucesso')
def sucesso():
    """nome = 'nome'
    senha = 'senha'"""
    return render_template('resultado.html')#, nome=nome, senha=senha, definir=defina)

if __name__=='__main__':
    app.run(debug=True)