from pprint import pprint
from belvo.client import Client
import json

def retornaContas(client):
	return [x for x in client.Accounts.list()]

def chamar(nome, senha):
	#with open(diretorio, 'r') as arquivo:
	#	mDados = json.load(arquivo)

	client = Client(
		nome,#mDados['my-secret-key-id'], 
		senha,#mDados['my-secret-key'], 
		"https://sandbox.belvo.co"#"https://api.belvo.co"
	)
	return client

def apagarTodas(client, listaContas):
	for x in range(len(listaContas)):
		print('Apagando o ID: ', listaContas[x]['id'])
		client.Accounts.delete(listaContas[x]['id'])
	print('IDs que tem agora: ', len(listaContas))

def printarContas(listaContas):
	for x in range(len(listaContas)):
		pprint(listaContas[x])
		print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
		if x+1<10:
			print(f'xxxxxxxxxxxxxx<<<|{x+1}|{x+1}|{x+1}|{x+1}|{x+1}|>>>xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
		else:
			print(f'xxxxxxxxxxxxxxx<<<|{x+1}|{x+1}|{x+1}|{x+1}|{x+1}|>>>xxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
		print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

def apagar(idPessoa, client):
	return client.Accounts.delete(idPessoa)

def registrar(client, instituição, nome, senha):
	# Register a link 
	link = client.Links.create(
	    institution=instituição,
	    username=nome,
	    password=senha
	)
	return link

def criar(client):
	links = [x for x in client.Links.list()]
	x = client.Accounts.create(links[0]['id'])
	return x

def ver_link(client):
	links = [x for x in client.Links.list()]
	return links

def ver_instituicoes(client):
	instituicoes = [x for x in client.Institutions.list()]
	return instituicoes 

def transacoes(client):
	transacoes= [x for x in client.Transactions.list()]
	return transacoes