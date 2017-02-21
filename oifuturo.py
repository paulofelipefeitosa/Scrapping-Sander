#!/usr/bin/env python
# coding: utf-8

'''
Referencia:
http://lxml.de/xpathxslt.html
'''

import os
import re
from datetime import datetime
from lxml import html, etree
import requests

def gettitle(page):
	t_st = page.find("meta property=\"og:title\" content=\"")
	t_st += len("meta property=\"og:title content=\"") + 1
	t_end = t_st
	while page[t_end] != '\"':
		t_end += 1
	return page[t_st : t_end]
	
def getimage(page):
	t_st = page.find("meta property=\"og:image\" content=\"")
	t_st += len("meta property=\"og:image\" content=\"")
	t_end = t_st
	while page[t_end] != '\"':
		t_end += 1
	return page[t_st : t_end]
	
def getfrom(string, after):
	t_st = string.find(after)
	t_st += len(after)
	return string[t_st : len(string)]

def oifuturoipanema():

	# carrega pagina de eventos para obter links para eventos
	#'''
	eventos = []
	page = requests.get( 'http://www.oifuturo.org.br/agenda/' )
	tree = html.fromstring( page.content )
	info = tree.xpath( '//article/a' )
	
	mes = ['Janeiro', 'janeiro', 'Fevereiro', 'fevereiro', 'Março', 'março', 'Abril', 'abril', 'Maio', 'maio', 'Junho', 'junho', 'Julho', 'julho', 'Agosto', 'agosto', 'Setembro', 'setembro', 'Outubro', 'outubro', 'Novembro', 'novembro', 'Dezembro', 'dezembro']
	dias = ['Segunda', 'segunda', 'terça', 'Terça', 'Quarta', 'quarta', 'Quinta', 'quinta', 'Sexta', 'sexta', 'Sábado', 'sábado', 'Domingo', 'domingo']
	
	event_title = []
	event_image = []
	event_local = []
	event_adress = []
	event_cep = []
	event_date = []
	event_age = []
	event_price = []
	event_period = []
	event_time = []
	event_info = []
	
	for i in xrange(len( info )):
		string = etree.tostring( info[ i ] )
		if re.search( '/evento/', string ):
			eventos.append( info[ i ].attrib['href'] )
			#print info[ i ].attrib['href']
			
	for i in xrange(len(eventos)):
		
		page = requests.get(eventos[i])
		tree = html.fromstring(page.content)
		
		page = page.content
		
		idx = page.find("meta property=\"og:description\" content=")
		
		if(idx == -1):		#Sinal de mudança no doc html
		
			print "Erro ao encontrar o padrao!"
			return -1
			
		else:
				
			lista = tree.xpath("//div[contains(@class, 'entry-content')]//*/text()")
			lista_aux = []
			final_list = []
			local_idx = 0
			
			for k in xrange(len(lista)):
				string = lista[k]

				if(len(string) > 0 and string[0] == '\n'):
					string = string[1 : len(string)]
					
				if(len(string) > 0 and string[len(string) - 1] == '\n'):
					string = string[1 : len(string) - 1]
				
				if string.encode('utf-8').find("Local:") != -1:
					local_idx = k
				
				#print string.encode('utf-8')
				lista_aux.append(string.encode('utf-8'))
				
			titulo = gettitle(page)
			imagem = getimage(page)
			
			local = endereco = cep = data = ""
			
			for x in xrange(local_idx, len(lista_aux)):
			
				if(lista_aux[x].find("Local: ") != -1):
					local = getfrom(lista_aux[x], "Local: ")
					
				elif(lista_aux[x].find("Endereço: ") != -1):
					endereco = getfrom(lista_aux[x], "Endereço: ")
					
				elif(lista_aux[x].find("CEP: ") != -1):
					cep = getfrom(lista_aux[x], "CEP: ")
					
				elif(lista_aux[x].find("Data: ") != -1):
					data = getfrom(lista_aux[x], "Data: ")
			
			classifi = entrada = periodo = horario = ""
			
			for x in xrange(0, local_idx):
				array = lista_aux[x].split('|')
				flag = False
				
				for y in xrange(0, len(array)):
					
					if(array[y].find("Classificação etária: ") != -1):
						classifi = getfrom(array[y], "Classificação etária: ")
						flag = True
						
					if(array[y].find("R$ ") != -1):
						entrada = getfrom(array[y], "R$ ")
						flag = True
						
					elif(array[y].find("Entrada: ") != -1):
						entrada = getfrom(array[y], "Entrada: ")
						flag = True
						
					elif(array[y].find("Entrada ") != -1):
						entrada = getfrom(array[y], "Entrada ")
						flag = True
						
					for z in mes:
						if(array[y].find(z) != -1):
							periodo = array[y]
							flag = True
							break
					
					for z in dias:
						if(array[y].find(z) != -1 and (array[y].find("venda") == -1 and array[y].find("Venda") == -1)):
							horario += array[y]
							flag = True
							break
				
				
				if(flag == False):
					final_list.append(lista_aux[x])
			
			
			if(len(classifi) == 0):
				classifi = "livre"
			if(len(entrada) == 0):
				entrada = "franca"
			
			pos = titulo.find("&#8211;")
			if(pos != -1):
				titulo = titulo[0 : pos] + '-' + titulo[pos + len("&#8211;") : len(titulo)]
			
			event_title.append(titulo)
			event_image.append(imagem)
			event_local.append(local)
			event_adress.append(endereco)
			event_cep.append(cep)
			event_date.append(data)
			event_age.append(classifi)
			event_price.append(entrada)
			event_period.append(periodo)
			event_time.append(horario)
			event_info.append(final_list)
			
	
	for i in xrange(len(eventos)):
		print event_title[i] + '\n'
		for j in xrange(len(event_info[i])):
			print '\t' + event_info[i][j]
		print event_local[i] + '\n'
		print event_date[i] + '\n'
		print event_period[i] + '\n'
		print event_time[i] + '\n'
		print "Faixa etária: " + event_age[i] + '\n'
		print "Entrada: " + event_price[i] + '\n'
		print event_adress[i] + '\n'
		print event_cep[i] + '\n'
		print event_image[i] + '\n'
		print '\n\n'
		
		
def main():
	oifuturoipanema()
	
main()

