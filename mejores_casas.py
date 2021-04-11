#! usr/bin/env python
# -*- coding: utf-8 -*-
# created in 21K08 (01:24:31) by gonthalo

# Compara las casas descargadas por el scraper y selecciona las mejores


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

if __name__ == "__main__":
	casas = get_saved_houses('VillazScraper/arfima.csv')
	# print (casas)
	best = sorted(casas.keys(), key = lambda x: chachicidad(casas[x]))
	for code in best[5:10]:
		print (chachicidad(casas[code]), casas[code])


