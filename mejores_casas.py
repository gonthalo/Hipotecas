#! usr/bin/env python
# -*- coding: utf-8 -*-
# created in 21K08 (01:24:31) by gonthalo

# Compara las casas descargadas por el scraper y selecciona las mejores

import urllib.request
import os, sys, time
from datetime import datetime

blacklist = ['92648039', '92561450', '89928575', '94120994', '88780582', '93615963', '94584179', '94967410', '95040565', '95045839']

def date2day():
	now = datetime.now()
	return '%02d%s%02d-%02d:%02d'%(now.year%100, 'FGHJKMNQUVXZ'[now.month-1], now.day, now.hour, now.minute)

def chachicidad(casa):
	px = int(casa['price'])
	size = int(casa['area'])
	return px/size


def get_saved_houses(file_name): # Lee la info de casas ya descargada del archivo correspondiente. La 
	f = open(file_name, 'r')
	lines = [el.split(';') for el in f.read().split('\n')]
	fields = lines[0]
	aux = fields.index('code')
	dic = {it[aux]:{fields[ii]:it[ii] for ii in range(len(fields))} for it in lines[1:]}
	return dic

def parse_images(objetivo, best):
	f = open('VillazScraper/%s_images.csv'%objetivo)
	txt = f.read().split('\n')[1:]
	f.close()
	for casa in best:
		if not os.path.exists('%s/%s'%(objetivo,casa)):
			if not os.path.exists(objetivo):
				os.mkdir(objetivo)
			os.mkdir('%s/%s'%(objetivo,casa))
			imgs = []
			ii = 0
			for line in txt[:-1]:
				url, code = line.split(',')
				if code == casa:
					ii += 1
					r = urllib.request.urlopen(url)
					with open("%s/%s/%s-%03d.jpg"%(objetivo,casa,casa,ii), "wb") as f:
						f.write(r.read())

def generate_report(objetivo = 'arfima2'):
	casas = get_saved_houses('VillazScraper/%s.csv'%objetivo)
	best = sorted(casas.keys(), key = lambda x: chachicidad(casas[x]))
	best = [el for el in best if el not in blacklist]
	if not os.path.exists(objetivo+'history/'):
		os.mkdir(objetivo+'history/')
	f = open(objetivo+'history/'+date2day()+'.txt', 'w')
	f.write('\n'.join([el+'\t'+str(casas[el]['price']) for el in best]))
	f.close()
	f = open('template.tex', 'r')
	txt = f.read()
	f.close()
	x = txt.index('%% INSERTAR LINEAS')
	txt.replace('%% INSERTAR LINEAS', '')
	lineas = ''
	parse_images(objetivo, best[:10])
	for code in best[:10]:
		lineas = lineas + '\\hyperlink{casa%s}{%s} & %s & %s & %.2f & %s \\\\\\hline\n'%(code, code, casas[code]['price'], casas[code]['area'], chachicidad(casas[code]), casas[code]['barrio'])
		# print (chachicidad(casas[code]), casas[code])
	txt = txt[:x] + lineas + txt[x:]
	x = txt.index('%% REPORTE DE CADA CASA')
	y = txt.index('%% FIN DEL REPORTE DE CADA CASA')
	reportecillo = txt[x:y]
	txt = txt[:x] + txt[y:]
	reportes = ''
	for code in best[:10]:
		if len(casas[code]['address']) < 3:
			casas[code]['address'] = '[...]'
		pagina = reportecillo
		pagina = pagina.replace('Direccion', casas[code]['address'])
		pagina = pagina.replace('Barrio', casas[code]['barrio'])
		pagina = pagina.replace('Distrito', casas[code]['distrito'])
		pagina = pagina.replace('123456', casas[code]['price'])
		pagina = pagina.replace('789', casas[code]['area'])
		pagina = pagina.replace('4321', '%.2f'%chachicidad(casas[code]))
		pagina = pagina.replace('Esta kelly es la puta hostia!', casas[code]['anuncio'].replace('&', ''))
		pagina = pagina.replace('92058112', code)
		for a,b,c in os.walk('%s/%s'%(objetivo,code)):
			pass
		n_images = len(c)
		if n_images == 0:
			pagina = pagina.replace('%% IMAGENES DE LA CASA', 'No hay imagenes disponibles')
		else:
			imagenes = ''
			for ii in range(min(6,n_images)):
				imagenes = imagenes + '\n\\includegraphics[width=0.32\\textwidth]{'+objetivo+'/%s/%s-%03d.jpg}'%(code,code,ii+1)
			pagina = pagina.replace('%% IMAGENES DE LA CASA', imagenes)
		reportes = reportes + pagina
	txt = txt[:x] + reportes + txt[x:]
	f = open('report_%s.tex'%objetivo, 'w')
	f.write(txt)
	f.close()

if __name__ == "__main__":
	print (date2day())
	generate_report(objetivo = 'arfima2')


