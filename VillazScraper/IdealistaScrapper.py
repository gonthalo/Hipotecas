"""
Altered from the github https://github.com/Villaz/idealistaScraper
by gonthalo :J in   february 2021?
"""
from selenium import webdriver
from selenium import common
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from vivienda import Vivienda
from map import Map
from images import Images
from datetime import datetime
import argparse
import time, sys

#                       ╔═╗┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐   ╦┌┬─┐┌─┐┌─┐┬  ┬┌─┐┌┬┐┌─┐
#                       ╚═╗│  ├┬┘├─┤├─┘├┤ ├┬┘   ║ │ │├┤ ├─┤│  │└─┐ │ ├─┤
#                       ╚═╝└─┘┴└─┴ ┴┴  └─┘┴└─   ╩ ┴─┘└─┘┴ ┴┴─┘┴└─┘ ┴ ┴ ┴
#
#
#
#
# Fields in list scraper = price,area,has_elevator,floor,exterior,rooms
# Fields in detail scrapper = address,barrio,distrito,ciudad,lat,lon
# Hay gente q no se aclara entre castellano e ingles... :v
#
#
#
#
#

BASE_URL = 'https://www.idealista.com/'

class IdealistaScrapper:
	"""
	Clase encargada de scrapear la página de Idealista
	"""

	info = None

	def __init__(self, tipo, location, name = None):
		"""
		Inicializador de la clase IdealistaScrapper.
		Dentro del método se inicializa la url con el tipo de vivienda y la localizacion donde se
		desea realiizar el scraping.
		En base a estos parámetros se generan los ficheros de salida.
		:param tipo: Tipo de activo a capturar, vivienda, garaje, trastero, etc.
		:param location: Localización donde se desea buscar.
		"""
		today = datetime.now().strftime('%Y%m%d')
		if location[-1] == '/':
			self.url = "{0}{1}/{2}".format(BASE_URL, tipo, location)
		else:
			self.url = "{0}areas/{1}/{2}".format(BASE_URL, tipo, location)
		if name == None:
			name = "{0}_{1}_{2}".format(today, tipo, location)
		self.file_name = name + ".csv"
		self.file_images_name = name + "_images.csv"

	def get_saved_houses(self): # Lee la info de casas ya descargada del archivo correspondiente. La 
		f = open(self.file_name, 'r')
		lines = [el.split(';') for el in f.read().split('\n')]
		fields = lines[0]
		aux = fields.index('code')
		dic = {it[aux]:{fields[ii]:it[ii] for ii in range(len(fields))} for it in lines[1:]}
		return dic

	def scrapeamiento(self, deeper: bool=True):
		"""
		"deeper" indica si buscar en detalle o solo el listado.
		"""
		# Se realiza el scraping de las páginas de listado
		driver = self._scrap_list_pages(self.url)
		# Si el parametro de deeper es true buscamos los detalles de cada activo
		if deeper:
			#Crear matriz d datos y guardar --> .csv
			entries = [Vivienda(i) for i in self.info.to_dict(orient='records')]#Vivienda(i) for i in
			houses = self.get_saved_houses()
			available = []
			for casa in entries:
				entry = casa.to_dict()
				code = entry['code']
				available.append(code)
				if code in houses.keys():
					for key in entry.keys():
						if entry[key] != entry[key]:
							entry[key] = ''
						entry[key] = str(entry[key])
						if entry[key] != 'None' and entry[key] != houses[code][key]:
							print ('Updating data in house', code, ':   ', key, 'is now', entry[key])
							houses[code][key] = entry[key]
					continue
				print ('found new house:', code)
				vivienda, images = self.get_detailed_info_from_entry(driver, casa)
				# with open(self.file_name, 'a') as f:
				# 	pd.DataFrame(data=[vivienda.to_dict()]).to_csv(f, header=f.tell() == 0, index=False, mode='a')
				if images is not None:
					with open(self.file_images_name, 'a') as f:
						images.to_csv(f, header=f.tell() == 0, index=False, mode='a')
				# import pdb; pdb.set_trace()
				entry = casa.to_dict()
				houses[code] = {key:str(entry[key]) for key in entry.keys()}
			aux = [el for el in houses.keys()]
			for code in aux:
				if code not in available:
					print ('House no longer available:', code)
					houses.pop(code)
			with open(self.file_name, 'w') as f:
				header = 'code;link;address;barrio;distrito;ciudad;lat;lon;price;area;has_elevator;floor;exterior;rooms'
				# print (houses)
				# import pdb; pdb.set_trace()
				f.write(header+'\n'+ '\n'.join([';'.join([houses[key][field] for field in header.split(';')]) for key in houses.keys()]))

		else:
			exit()
			self.info.to_csv(self.file_name, header=True, index=False)
		driver.quit()

	def _scrap_list_pages(self, url: str, driver = None):
		"""
		Realiza el scrapeo de la página de listado.
		:param url: URL sobre la que realizar el scraping.
		:return: None
		"""

		if driver == None:
			driver = webdriver.Firefox(executable_path=r'/home/gonthalo/.jaquersoft/Hipotecas/geckodriver')
			driver.get(url)
			driver.implicitly_wait(10)# Por defecto se esperan 10 segundos para cargar los componentes.
			# time.sleep(140)
			driver.set_page_load_timeout(20)# Si a los 20 segundos no se ha finalizado la larga se produce un timeout
		else:
			driver.get(url)
		# print (html)
		while "https://geo.captcha-delivery.com/captcha" in driver.page_source:
			time.sleep(20)
		# Cada activo se encuentra dentro del tag article con class item, encontramos todos los existentes
		# y los recorremos leyendo la informacion que contienen.
		articles = driver.find_elements_by_xpath("//article[contains(@class, 'item')]")
		info = [self._extract_top_information(article) for article in articles]
		info = [i.to_dict() for i in info]
		self.info = pd.DataFrame(data=info) if self.info is None else pd.concat([self.info, pd.DataFrame(data=info)])
		# Buscamos la página en la que nos encontramos, si no existe la clase pagination, o
		# no existe el elemento con clase next es que hemos llegado al final de las páginas.
		# En este caso se lanza una excepción y se finaliza la captura.
		# Con el fin de evitar en cierta medida el banneo por parte del proveedor, cada scrapeo de página
		# se realiza con una instancia diferente del navegador, por ello una vez finalizado se llama a driver.quit()
		try:
			pagination = driver.find_element_by_class_name('pagination')
			url = pagination.find_element_by_class_name('next').find_element_by_tag_name('a').get_attribute('href')
			# driver.quit()
			self._scrap_list_pages(url, driver)
		except NoSuchElementException:
			print("Finished")
		finally:
			return driver

	def _extract_top_information(self, article: WebElement) -> Vivienda:
		"""
		Extrae la información de cada activo a partir de los datos encontrados en la pagina de listado
		:param article: elemento articulo que se desea scrapear.
		:return:
		"""
		info = article.find_element_by_class_name('item-info-container')

		vivienda = Vivienda()
		vivienda.link = info.find_element_by_class_name('item-link').get_attribute('href')
		vivienda.code = vivienda.link.split('/')[-2]
		vivienda.price = info.find_element_by_class_name('item-price').text.replace('€', '').replace('.', '')

		for detail in info.find_elements_by_class_name('item-detail'):
			type_detail = detail.find_element_by_tag_name('small').text
			value = detail.text.replace(type_detail, '').rstrip()
			if type_detail == 'hab.':
				vivienda.rooms = value
			elif type_detail == 'm²':
				vivienda.area = value
			elif 'bajo' in value:
				vivienda.floor = -1
			elif 'planta' in value:
				if value == 'Entreplanta':
					vivienda.floor = 0.5
				else:
					vivienda.floor = int(value.replace('ª planta', ''))

			if 'exterior' in detail.text:
				vivienda.exterior = True
			if 'interior' in detail.text:
				vivienda.exterior = False
			if 'con ascensor' in detail.text:
				vivienda.has_elevator = True
			if 'sin ascensor' in detail.text:
				vivienda.has_elevator = False
		return vivienda

	def get_detailed_info_from_entry(self, driver, vivienda: Vivienda):
		"""
		Extrae información especifica de cada vivienda a partir de la página de detalle.
		:param vivienda: vivienda sobre la que capturar sus datos ampliados.
		:return: Tupla con primer elemento de vivienda y segundo elemento como un dataframe de imagenes.
		"""
		images = None
		# Creamos un nuevo driver para impedir que idealista nos bloquee al pensar que somos un bot.
		# driver = webdriver.Firefox(executable_path=r'/home/gonthalo/.jaquersoft/Hipotecas/geckodriver')
		try:
			driver.get(vivienda.link)
			driver.implicitly_wait(4)
			time.sleep(2)
			while "https://geo.captcha-delivery.com/captcha" in driver.page_source:
				time.sleep(20)
			# driver.set_page_load_timeout(20)
			ubication = driver.find_element_by_id('mapWrapper')
			ubication_data = [i.text for i in ubication.find_elements_by_tag_name('li')]
			vivienda.address = ubication_data[0]
			vivienda.barrio = ubication_data[1]
			vivienda.distrito = ubication_data[2]
			vivienda.ciudad = ubication_data[3]
			vivienda.lat, vivienda.lon = Map(driver).get_lat_lon()
			images = Images(driver, vivienda.code).get_images()
		except common.exceptions.WebDriverException as ex:
			print(ex)
			print(vivienda.link)
			return None, images
		finally:
			return vivienda, images


if __name__ == '__main__':
	# element = driver.find_element_by_id("qa_adfilter_price")
	# element.click()
	# xaux = element.find_element_by_css_selector("li[data-value='150000']")
	# xaux.click()
	#https://www.idealista.com/areas/venta-viviendas/con-precio-hasta_150000,metros-cuadrados-mas-de_60/?shape=%28%28cz%7BuF%7CltUckBuWg%7BAgnFpYqwDpbEefChg%40bvE%7BNliIem%40be%40%29%29
	dic = {'arfima':'con-precio-hasta_150000,metros-cuadrados-mas-de_60/?shape=((cz{uF|ltUckBuWg{AgnFpYqwDpbEefChg%40bvE{NliIem%40be%40))'}
	parser = argparse.ArgumentParser(description='Scrapeo idealista')
	# parser.add_argument('transaccion', help="Tipo de transaccion a buscar", choices=['venta', 'alquiler'])
	# parser.add_argument('tipologia', help='Tipologia a buscar', choices=['viviendas'])
	parser.add_argument('--zona', help='Zona a buscar', default='arfima')#'oviedo-asturias')
	parser.add_argument('--full', help='Busqueda superficial o detalle', default=True)
	args = parser.parse_args()
	# import pdb; pdb.set_trace()
	zona_objetivo = args.zona+'/' if args.zona not in dic.keys() else dic[args.zona]
	i = IdealistaScrapper('venta-viviendas',zona_objetivo, name = args.zona)
	# i.get_saved_houses()

	i.scrapeamiento(args.full)
	# print (i.get_saved_houses())