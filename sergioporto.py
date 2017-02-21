#!/usr/bin/env python
# coding: utf-8

import os
import re
import requests

def separateInfo(page, string):
	idx = page.find(string)

	return (page[0 : idx], page[idx : len(page)])

def findAnyContain(arrayPage, lista):
	for i in xrange(len(arrayPage) - 1, 0, -1):
		for j in xrange(len(lista)):
			if(arrayPage[i].find(lista[j]) != -1):
				return arrayPage[i]
	return ""

def removeTags(string):
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

def getInfoInside(page, stringA, stringB, pos):
	#Pega a informação que está entre stringA e stringB apartir de pos
	idx = page.find(stringA, pos)
	if(idx == -1):
		return ("", -1)

	idx += len(stringA)

	idxend = page.find(stringB, idx)

	return (page[idx : idxend], idxend + len(stringB))


def getEventsUrl(url, page, lista):
	page = requests.get(url).content

	pos = 0
	while True:
		ans = getInfoInside(page, "<div class=\"et_pb_image_container\">							<a href=\"", "\"", pos)

		if(ans[1] == -1):
			break
		else:
			lista.append(ans[0])
			pos = ans[1]


def main():
	
	page = ""
	eventos = []
	getEventsUrl("http://projetoentre.com/sergioporto/", page, eventos)
	
	mes = ['Dia', 'dia', 'temporada', 'Temporada', 'Janeiro', 'janeiro', 'Fevereiro', 'fevereiro', 'Março', 'março', 'Abril', 'abril', 'Maio', 'maio', 'Junho', 'junho', 'Julho', 'julho', 'Agosto', 'agosto', 'Setembro', 'setembro', 'Outubro', 'outubro', 'Novembro', 'novembro', 'Dezembro', 'dezembro']
	dias = ['Segunda', 'segunda', 'terça', 'Terça', 'Quarta', 'quarta', 'Quinta', 'quinta', 'Sexta', 'sexta', 'Sábado', 'sábado', 'Domingo', 'domingo']

	infor = []
	imagem = []
	data = []
	dia = []
	horario = []
	valor = []
	classificacao = []

	for i in xrange(len(eventos)):
		
		page = requests.get(eventos[i]).content

		imagem.append(getInfoInside(page, "meta property=\"og:image\" content=\"", "\"", 0)[0])

		inf = getInfoInside(page, "<div class=\"et_pb_text et_pb_module et_pb_bg_layout_light et_pb_text_align_left  et_pb_text_0\">", "</div>", 0)[0]
		inf = removeTags(inf)
		#infor.append(inf)
		inf = inf.split('\n')

		data.append(findAnyContain(inf, mes))
		dia.append(findAnyContain(inf, dias))
		horario.append(findAnyContain(inf, ['Horário', 'horário']))
		valor.append(findAnyContain(inf, ['R$']))
		classificacao.append(findAnyContain(inf, ['lassifica']))



	for i in xrange(len(eventos)):
		print '\n' + eventos[i]	
		print imagem[i]
		#print infor[i] + '\n'
		print data[i]

		if(len(dia[i]) > 0):
			print dia[i]

		if(len(horario[i]) > 0 and horario[i] != dia[i]):
			print horario[i]

		print valor[i]
		print classificacao[i] + '\n'



main()