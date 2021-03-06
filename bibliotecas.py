#A biblioteca contém As funções utilizadas na Main

from pprint import pprint#Importando Pprint

from belvo.client import Client#Importando a blibioteca da belvo

import json#Json para manipulações de arquivos



#Realiza o Login na API da belvo,e irá servir de parametro para as deais funções 
def chamar(nome, senha):
	
	client = Client(
		nome,#mDados['my-secret-key-id'], 
		senha,#mDados['my-secret-key'], 
		"https://sandbox.belvo.co"#"https://api.belvo.co"
	)
	return client




#Recebe a lista de Contas e apaga a contas por ID's
def apagarTodas(client, listaContas):
	for x in range(len(listaContas)):
		print('Apagando o ID: ', listaContas[x]['id'])
		client.Accounts.delete(listaContas[x]['id'])
	print('IDs que tem agora: ', len(listaContas))



#Recebe a lista de Contas e printas as contas na tela
def printarContas(listaContas):
	for x in range(len(listaContas)):
		pprint(listaContas[x])
		print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
		if x+1<10:
			print(f'xxxxxxxxxxxxxx<<<|{x+1}|{x+1}|{x+1}|{x+1}|{x+1}|>>>xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
		else:
			print(f'xxxxxxxxxxxxxxx<<<|{x+1}|{x+1}|{x+1}|{x+1}|{x+1}|>>>xxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
		print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')




#Recebe o ID e o apaga
def apagar(idPessoa, client):
	return client.Accounts.delete(idPessoa)



#Recebe a instituição, nome, senha desejados para a criação de um novo link
def registrar(client, instituição, nome, senha):
	# Register a link 
	link = client.Links.create(
	    institution=instituição,
	    username=nome,
	    password=senha
	)
	return link



#Recebe os links e cria contas a partir deles
def criar(client):
	links = [x for x in client.Links.list()]
	x = client.Accounts.create(links[0]['id'])
	return x



#Recebe os links e o printa na tela
def ver_link(client):
	links = [x for x in client.Links.list()]
	return links



#Recebe as intituições cadastradas na belvo e as retorna
def ver_instituicoes(client):
	instituicoes = [x for x in client.Institutions.list()]
	return instituicoes 



#Recebe as Transações realizadas e as retorna para o cliente
def transacoes(client):
	transacoes= [x for x in client.Transactions.list()]
	return transacoes



#Lista as as contas cadastradas e as retornas
def retornaContas(client):
	return [x for x in client.Accounts.list()]