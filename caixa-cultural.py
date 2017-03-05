#!/usr/bin/env python
# coding: utf-8
# Centro Cultural do Banco do Brasil
# 3:34

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

def getDate():
	day = time.strftime("%d")
	month = time.strftime("%m")
	year = time.strftime("%Y")
	return (day, month, year)

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
		lista.append('http://www.caixacultural.com.br/SitePages/' + info[ i ].attrib['href'])

	return lista

def main():
	cidade = ['Brasilia', 'Curitiba', 'Fortaleza', 'Recife', 'Rio de Janeiro', 'Salvador', 'São Paulo']
	idcidade = ['1', '2', '3', '5', '6', '7', '9']

	today = getDate()

	for i in xrange(len(idcidade)):
		
		print cidade[i] + ':'

		hhtml = requests.get('http://www.caixacultural.com.br/SitePages/unidade-programacao.aspx?uid=' + idcidade[i]).content

		urls = getInfoInside(hhtml, '<div id="ctl00_mainright_g_629ce2dc_c906_412b_9856_8e7a64c83102" WebPart="true" __MarkupType="vsattributemarkup" __WebPartId="{629ce2dc-c906-412b-9856-8e7a64c83102}">', '<!-- **************************** -->', 0)
		if(len(urls[0]) < 50):
			print "\n"
			continue
		
		page = html.fromstring(urls[0])
		urls = page.xpath('//div[contains(@class, "col-sm-4 sem-padding programacao-item")]/a')
		evento = getLinks(urls, "")

		hhtml = requests.get('http://www.caixacultural.com.br/SitePages/unidade-como-chegar.aspx?uid=' + idcidade[i]).content
		page = html.fromstring(hhtml)

		adress = page.xpath('//input[contains(@id, "txtendereco")]')
		adress = getAttrib(adress, 'value')

		for j in xrange(len(evento)):

			hhtml = requests.get(evento[j]).content
			page = html.fromstring(hhtml)

			datafim = page.xpath('//input[contains(@id, "datafim")]')
			datafim = getAttrib(datafim, 'value')

			info = page.xpath('//span[contains(@id, "eventook")]/..//*/text()')

			titulo = info[0].encode('utf-8')
			datainicio = info[2].encode('utf-8')
			horario = info[7].encode('utf-8')
			local = ""
			ingresso = ""
			entrada = ""
			for k in xrange(len(info)):
				if(info[k].find("Local:") != -1):
					local = info[k+2].encode('utf-8')
				elif(info[k].find("Valor do Ingresso:") != -1):
					ingresso = info[k+2].encode('utf-8')
				elif(info[k].find("Entrada:") != -1):
					entrada = info[k+2].encode('utf-8')


			info = page.xpath('//div[contains(@id, "ctl00_mainright_g_9c056b72_ca32_4f0e_9d55_283b29e306da")]/..//*/text()')
			descricao = ""
			flag = False
			for k in xrange(len(info)):
				if(info[k].find('Voltar para a Programa') != -1):
					break
				elif(flag == True):
					descricao += info[k].encode('utf-8') + '\n'
				elif(info[k].find('Evento Encerrado') != -1):
					flag = True

			image = page.xpath('//div[contains(@data-idgaleria, "123456789")]//*/li/a/img')
			image = getAttrib(image, 'data-original')

			print '\t' + titulo
			print '\t' + evento[j]
			print '\t' + 'Caixa Cultural Unidade ' + cidade[i]
			print '\t' + adress[0].encode('utf-8') + ' no ' + local
			print '\tTemporada: ' + datainicio + ' ate ' + datafim[0]
			print '\tHorario: ' + horario
			print '\tEntrada: ' + entrada
			print '\tIngresso: ' + ingresso
			print '\t' + descricao + '\n'
			for k in xrange(len(image)):
				print image[k].encode('utf-8')
			print "\n"

		print ""
		

main()