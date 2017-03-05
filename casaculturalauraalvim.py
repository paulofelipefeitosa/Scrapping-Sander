#!/usr/bin/env python
# coding: utf-8
# Casa Cultural Laura Alvim

import os
import re
import time
import requests
from lxml import html, etree
import xml.etree.ElementTree as ET

def getInfoInside(page, stringA, stringB, pos):
	#Pega a informação que está entre stringA e stringB apartir de Pos
	idx = page.find(stringA, pos)
	if(idx == -1):
		return ("", -1)

	idx += len(stringA)

	idxend = page.find(stringB, idx)

	return (page[idx : idxend], idxend + len(stringB))
	#Retorna a string e a Posição do último caractere de stringB

def getAttrib(info, type):

	lista = []

	for i in xrange(len(info)):
		string = etree.tostring(info[i])
		lista.append(info[i].attrib[type])

	return lista

def getLinks(info, start):
	lista = []

	for i in xrange(len( info )):
		string = etree.tostring( info[ i ] )
		lista.append(info[ i ].attrib['href'])

	return lista

def main():

	hhtml = requests.get('http://www.casadeculturalauraalvim.rj.gov.br/verprogramacao/').content
	page = html.fromstring(hhtml)

	urls = page.xpath('//div[contains(@class, "filtr-container")]/div/a')
	evento = getLinks(urls, "")

	for i in xrange(len(evento)):

		hhtml = requests.get(evento[i]).content
		page = html.fromstring(hhtml)

		titulo = getInfoInside(hhtml, '<h2 class="page-title">', '</h2>', 0)[0]

		image = page.xpath('//div[contains(@class, "destaque-img-wp")]/img')
		image = getAttrib(image, 'src')[0].encode('utf-8')

		description = page.xpath('//div[contains(@class, "info-wrapper row")]/div//*/text()')
		descricao = ""
		for j in xrange(1, len(description)):
			descricao += description[j].encode('utf-8') + '\n'

		info = page.xpath('//div[contains(@class, "info-wrapper row")]/ul//*/text()')

		entidade = info[1].encode('utf-8')
		temporada = info[5].encode('utf-8')
		horario = info[7].encode('utf-8')
		classificacao = info[9].encode('utf-8')
		preco = info[11].encode('utf-8')

		print titulo
		print image
		print descricao
		print 'Local: ' + entidade
		print 'Temporada: ' + temporada
		print 'Horario: ' + horario
		print 'Classificação Etária: ' + classificacao
		print 'Preço: ' + preco + '\n' 



main()