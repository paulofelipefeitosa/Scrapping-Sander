#!/usr/bin/env python
# coding: utf-8
# Teatro Municipal do Rio de Janeiro

import os
import re
from datetime import datetime
from lxml import html, etree
import requests

dig = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def clean(string):
	ans = ""
	for i in xrange(len(string)):
		if(string[i] == ','):
			ans += '.'
		elif(string[i] in dig):
			ans += string[i]
	return ans

def tclean(string):
	ans = ""
	if(string[0 : 5] == "     "):
		for i in xrange(5, len(string)):
			if(string[i] != '\t' and string[i] != '\n'):
				ans += string[i]
	else:
		for i in xrange(0, len(string)):
			if(string[i] != '\t' and string[i] != '\n'):
				ans += string[i]
	return ans

def find_push(page, start, end):
	idx = page.find(start)
	idx += len(start) + 1
	idxend = page.find(end, idx)

	return removetags(page[idx : idxend])

def ffind_push(page, start, end, eend):
	idx = page.find(start)
	idx += len(start) + 1
	idxend = page.find(end, idx)
	idxend += len(end)

	idxeend = page.find(eend, idxend)

	return removetags(page[idxend : idxeend])

def getimage(string):
	idx = string.find("<div class=\"page-title-content\">")
	idxst = string.find("src=\"", idx)
	idxst += len("src=\"")
	idxend = idxst
	while(string[idxend] != "\""):
		idxend += 1

	return string[idxst : idxend]

def removeFlags(string):
	# L&#8217; &#8216; &#8217; &#8211; [&#8230;] &nbsp;
	# Remove todas as flags do Tipo Acima

	while True:
		idx = string.find("&")
		if idx == -1:
			break

		ids = idx - 1
		ide = idx + 1

		while (ids > 0 and string[ids] != " "):

			if(string[ids].isalpha()):

				if(string[ids] == 'L' or string[ids] == 'n'):
					ids -= 1

				else:
					break

			else:
				ids -= 1

		while (string[ide] != ';'):
			ide += 1

		string = string[0 : ids + 1] + string[ide + 1 : len(string)]

	return string

def filter(string):
	ans = ""
	for i in xrange(len(string)):
		if(string[i].isupper()):
			if(i > 0 and ((string[i-1].isalnum() and not string[i-1].isupper()) or (string[i-1] == '.' or string[i-1] == ')'))):
				ans += "\n" + string[i]
			else:
				ans += string[i]	
		else:
			ans += string[i]

	return ans


def removetags(string):
	pt = 0
	ans = ""
	flag = False
	tam = len(string)

	while pt < tam:
		if(string[pt] == '<'):
			flag = True
		elif(string[pt] == '>'):
			flag = False

		if(string[pt] != '>' and flag == False):
			ans += string[pt]

		pt += 1

	return ans

def teatromunicipal():

	eventos = []
	descricao = []
	descricaoin = []
	categoria = []
	titulo = []
	data = []
	hora = []
	preco = []
	imagem = []

	page = requests.get('http://www.theatromunicipal.rj.gov.br/programacao/')
	string = page.content

	pos = -1
	while True:
		idx = string.find("http://www.theatromunicipal.rj.gov.br/programacao/", pos+1)
		if(idx == -1):
			break

		idxend = idx;
		while(string[idxend] != '\"'):
			idxend += 1

		url = string[idx : idxend]
		flag = False

		if(len(url) != len("http://www.theatromunicipal.rj.gov.br/programacao/")):
			if(len(eventos) == 0):
				eventos.append(url)
				flag = True
			elif(eventos[len(eventos) - 1] != url):
				eventos.append(url)
				flag = True

		pos = idx + 1

		if(flag == True):
			iidx = string.find("<div class=\"entry excerpt entry-summary\">", pos)
			iidx += len("<div class=\"entry excerpt entry-summary\">") + 1
			iidxend = string.find("</div>", iidx)

			descricao.append(removeflags(filter(tclean(removetags(string[iidx : iidxend])))))


	for i in xrange(len(eventos)):

		page = requests.get(eventos[i])
		string = page.content
	
		categoria.append(tclean(find_push(string, "<div class=\"category\">", "</div>")))
		titulo.append(removeflags(tclean(find_push(string, "<h2 class=\"post-title entry-title\">", "</h2>"))))

		datetime = tclean(find_push(string, "<div class=\"dates\">", "</div>")).split(",")
		data.append(datetime[0])
		hora.append(datetime[1][1 : len(datetime[1])])
		
		tree = html.fromstring(page.content)
		lista = tree.xpath("//div[contains(@class, 'precos')]//*/text()")
		lista_aux = []

		j = 2
		while j < len(lista):

			aux = lista[j].encode('utf-8').split("–")
			if(len(aux) < 2):
				j += 1
				aux.append(lista[j].encode('utf-8'))
			
			lista_aux.append((aux[0], clean(aux[1])))
			j += 1
		
		preco.append(lista_aux);

		descricaoin.append(removeflags(filter(tclean(ffind_push(string, "<h2 class=\"post-title entry-title\">", "</h2>", "<div class=\"dates\">")))))
		imagem.append(getimage(string))
	
	for i in xrange(len(eventos)):
		print '\n' + eventos[i]
		print titulo[i]
		print categoria[i]
		print descricao[i]
		print descricaoin[i]
		print data[i]
		print hora[i]
		for j in xrange(len(preco[i])):
			print '\t' + preco[i][j][0] + " " + preco[i][j][1]
		print imagem[i]
		print ""
	print ""


def main():
	teatromunicipal()

main()