#!/usr/bin/env python
# coding: utf-8

import os
import time
from pyspider.libs.base_handler import *

palavras_chave = ['calendario+eventos+rio+de+janeiro', 'calendario+eventos+são+paulo', 'calendario+eventos+curitiba', 'calendario+eventos+belo+horizonte']

timestamp = int(time.time())

class Handler(BaseHandler):
    
    crawl_config = {
    }

    @every(minutes=1)
    def on_start(self):
        for i in xrange(len(palavras_chave)):
            self.crawl('https://www.google.com.br/search?q=' + palavras_chave[i], callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('h3[class^="r"]').find('a').items():
            if(each.attr.href.find('search?') == -1):
                self.crawl(each.attr.href, callback=self.detail_page)
     
    def detail_page(self, response):

        out = open('./Crawler/' + response.doc('title').text().encode + '-' + str(timestamp), 'w')
        out.write(response.text.encode('utf-8'))
        out.close()

        return { #debug
            "url": response.url,
            "title": response.doc('title').text().encode('utf-8'),
            "html": response.text.encode('utf-8'),
        }