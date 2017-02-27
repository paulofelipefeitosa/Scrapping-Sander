#!/usr/bin/env python
# coding: utf-8

import re
import os
import time
import requests
import webbrowser
from urlparse import urlparse, parse_qs
from lxml import html, etree

def removeEOF(urls):

   for i in xrange(len(urls)):

      if(urls[i][len(urls[i]) - 1] == '\n'):

         urls[i] = urls[i][0 : (len(urls[i]) - 1)]

def removeLinksVisited(urls, linksUsados, linksDescartados):

   k = 0
   while(k < len(urls)):
      flag = True

      for x in linksUsados:
         if(x.find(urls[k]) != -1 or urls[k].find(x) != -1):
            flag = False
            break

      for x in linksDescartados:
         if(x.find(urls[k]) != -1 or urls[k].find(x) != -1):
            flag = False
            break

      if(flag == False):
         urls.pop(k)
      else:
         k += 1

def getLinks(info, start):
   lista = []

   for i in xrange(len( info )):
      string = etree.tostring( info[ i ] )
      url = info[ i ].attrib['href']
   
      if url.startswith(start):
         url = parse_qs(urlparse(url).query)['q']
         lista.append(url[0])

   return lista

def getMorePages(page, totalPages):
   # Extrai as proximas paginas de pesquisa do google, vai até a décima página (Valor especificado em totalPages).
   lista = []

   info = page.xpath('//tr[@valign="top"]/td/a')
   for i in xrange(0, totalPages):
      url = 'https://www.google.com.br' + info[i].attrib['href']
      lista.append(url)

   return lista
   

def google_crawler():
   
   palavras_chave = ['calendario+eventos', 'eventos+culturais', 'teatro']
   cidades = ['rio+de+janeiro', 'são+paulo']

   listaSites = open('lista_sites.txt', 'a+')
   listaSitesD = open('lista_descart.txt', 'a+')
   
   linksUsados = listaSites.readlines()
   linksDescartados = listaSitesD.readlines()

   removeEOF(linksUsados)
   removeEOF(linksDescartados)

   timestamp = int(time.time())

   for j in xrange(len(palavras_chave)):
      for l in xrange(len(cidades)):

         raw = requests.get('https://www.google.com.br/search?q=' + palavras_chave[j] + '+' + cidades[l]).text
         page = html.fromstring(raw)

         urlsPages = getMorePages(page, 3)
         urlsPages.insert(0, 'https://www.google.com.br/search?q=' + palavras_chave[j] + '+' + cidades[l])

         for i in xrange(len(urlsPages)):

            raw = requests.get(urlsPages[i]).text
            page = html.fromstring(raw)

            info = page.xpath( '//h3[@class="r"]/a' )
            urls = getLinks(info, "/url?")

            removeLinksVisited(urls, linksUsados, linksDescartados)

            for k in xrange(len(urls)):

               webbrowser.open(urls[k], new=2)

               action = raw_input('Do you want this website? (y or n, z to stop): ')

               if(action == 'y'):
                  
                  listaSites.write('\n' + urls[k])
                  linksUsados.append(urls[k])

                  ppage = requests.get(urls[k], allow_redirects=False).content
                  
                  out = open('./Crawler/' + urlparse(urls[k]).netloc + '-' + str(timestamp), 'w')
                  out.write(ppage)
                  out.close()

               elif(action == 'n'):

                  listaSitesD.write('\n' + urls[k])
                  linksDescartados.append(urls[k])

               elif(action == 'z'):
                  break

   listaSites.close()
   listaSitesD.close()
            

def main():
   google_crawler()

main()
