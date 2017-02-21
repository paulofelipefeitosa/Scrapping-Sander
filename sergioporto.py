#!/usr/bin/env python
# coding: utf-8
# Espaço Cultural Municipal Sérgio Porto

import os
import re
import requests

def separateInfo(string, pattern, pos):
	#Separa a informação em duas (retirando Pattern) apartir de POS, exemplo para a string = "Paulo Felipe Feitosa"
	#Se o Pattern for "Felipe", o retorno dessa função deve ser "Paulo " e " Feitosa"

	idx = string.find(pattern, pos) - 2
	idxend = idx + len(pattern)

	return (string[0 : idx], string[idxend + 1 : len(string)])

def removeFlags(string):
	# L&#8217; &#8216; &#8217; &#8211; [&#8230;] &nbsp;
	# Remove todas as flags do Tipo Acima

	while True:
		idx = string.find("&")
		if idx == -1:
			break

		ids = idx - 1
		ide = idx + 1

		if(string[ids] == 'L' or string[ids] == '['):
			ids += 1

		while (string[ide] != ';'):
			ide += 1

		if(string[ide + 1] == ']'):
			ide += 1

		string = string[0 : ids + 1] + string[ide + 1 : len(string)]

	return string

def findAnyContain(arrayPage, lista):
	#Encontra o ultimo array que contém qualquer elemento de lista.

	pos = -1
	for i in xrange(len(arrayPage) - 1, 0, -1):
		for j in xrange(len(lista)):
			if(arrayPage[i].find(lista[j]) != -1):
				return (arrayPage[i], i)
	return ("", -1)
	#Retorna a String e Posição da String no Array

def removeTags(string):
	#Remove todas as Tags HTML dentro de string.

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
	#Pega a informação que está entre stringA e stringB apartir de Pos
	idx = page.find(stringA, pos)
	if(idx == -1):
		return ("", -1)

	idx += len(stringA)

	idxend = page.find(stringB, idx)

	return (page[idx : idxend], idxend + len(stringB))
	#Retorna a string e a Posição do último caractere de stringB


def getEventsUrl(url, page, lista):
	#Pega todos os URLs de detalhamento em Page e põe em Lista.

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

	titulo = []
	descricao = []
	imagem = []
	data = []
	dia = []
	horario = []
	valor = []
	classificacao = []

	for i in xrange(len(eventos)):
		
		page = requests.get(eventos[i]).content

		title = getInfoInside(page, "meta property=\"og:title\" content=\"", "\"", 0)[0]
		title = separateInfo(title, " Espaço Cultural Municipal Sérgio Porto", 0)[0]
		titulo.append(title)

		imagem.append(getInfoInside(page, "meta property=\"og:image\" content=\"", "\"", 0)[0])

		info = getInfoInside(page, "<div class=\"et_pb_text et_pb_module et_pb_bg_layout_light et_pb_text_align_left  et_pb_text_0\">", "</div>", 0)[0]
		info = removeTags(info)
		info = removeFlags(info)

		info = info.split('\n')

		data.append(findAnyContain(info, mes)[0])

		dia.append(findAnyContain(info, dias)[0])

		horario.append(findAnyContain(info, ['Horário', 'horário'])[0])

		valor.append(findAnyContain(info, ['R$'])[0])

		classificacao.append(findAnyContain(info, ['lassifica'])[0])


		pos = findAnyContain(info, mes)[1]
		text = ""
		for j in xrange(0, pos):
			if(len(info[j]) > 1):
				text += info[j] + '\n'

		descricao.append(text)

	for i in xrange(len(eventos)):
		print '\n' + eventos[i]
		print imagem[i]
		print titulo[i]
		print descricao[i]
		print data[i]

		if(len(dia[i]) > 0):
			print dia[i]

		if(len(horario[i]) > 0 and horario[i] != dia[i]):
			print horario[i]

		print valor[i]
		print classificacao[i] + '\n'



main()