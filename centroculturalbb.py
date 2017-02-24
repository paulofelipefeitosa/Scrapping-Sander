#!/usr/bin/env python
# coding: utf-8
# Centro Cultural do Banco do Brasil

import os
import re
import sys
import time
import requests
from lxml import html, etree

def getDate():
	day = time.strftime("%d")
	month = time.strftime("%m")
	year = time.strftime("%Y")
	numDay = time.strftime("%w")
	return (str(day), str(month), str(year), str(numDay))

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
		ans = getInfoInside(page, "<h4><a href=\"", "\"", pos)

		if(ans[1] == -1):
			break
		else:
			lista.append(ans[0])
			pos = ans[1]

def main():

	categorias = [ 'teatro', 'cinema', 'artes-visuais', 'musica' ]
	cidades = [ 'bh', 'rj', 'df', 'sp' ]

	for cidade in cidades:
		for categoria in categorias:
			todayInfo = getDate()

			eventos = []
			titulo = []
			temporada = []
			horario = []
			imagem = []
			descricao = []

			page = ""
			url = 'http://culturabancodobrasil.com.br/portal/wp-admin/admin-ajax.php?action=reuturnEventCalendarInicio&estado=' + cidade + '&cat=' + categoria + '&dia=' + todayInfo[0] + '&mes=' + todayInfo[1] + '&ano=' + todayInfo[2] + '&inicial=true&diaSemana=' + todayInfo[3]
			getEventsUrl(url, page, eventos)

			for i in xrange(len(eventos)):
				page = requests.get(eventos[i]).content
				tree = html.fromstring(page)

				title = tree.xpath("//h1[contains(@class, 'nome-evento')]/.././/*/text()")[1].encode('utf-8')

				season = tree.xpath("//div[contains(@class, 'data-evento')]//*/text()")

				time = tree.xpath("//li[contains(@class, 'horario')]//*/text()")

				image = getInfoInside(page, "<div class=\"banner-evento\" style=\"background-image:url(", ")\"", 0)[0]

				infor = tree.xpath("//div[contains(@class, 'saiba-mais-sobre')]//*/text()")

				print eventos[i]
				print title
				for j in xrange(len(season)):
					print season[j],

				print ""

				for j in xrange(len(time)):
					print time[j].encode('utf-8'), 

				print '\n' + image

				for j in xrange(1, len(infor)):
					if(infor[j].find("a href=\"") == -1):
						print infor[j].encode('utf-8'),

				print '\n\n'



	for cidade in cidades:
		for categoria in categorias:
			out = open('./Arquivos/' + categoria + '_' + cidade, 'w')
			page = requests.get('http://culturabancodobrasil.com.br/portal/wp-admin/admin-ajax.php?action=reuturnEventCalendarInicio&estado=' + cidade + '&cat=' + categoria + '&dia=' + todayInfo[0] + '&mes=' + todayInfo[1] + '&ano=' + todayInfo[2] + '&inicial=true&diaSemana=' + todayInfo[3]).content
			out.write(page)
			out.close()



main()