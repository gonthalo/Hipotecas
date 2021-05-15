# from selenium import webdriver
# from selenium import common
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.common.exceptions import NoSuchElementException
# import pandas as pd
# from vivienda import Vivienda
# from map import Map
# from images import Images
# from datetime import datetime
# import argparse
# import time, sys

# driver = webdriver.Firefox(executable_path=r'/home/gonthalo/.jaquersoft/Hipotecas/geckodriver')
# driver.get('https://www.idealista.com')
# driver.implicitly_wait(10)
# driver.get('https://www.idealista.com/areas/venta-viviendas/?shape=((cz{uF|ltUckBuWg{AgnFpYqwDpbEefChg%40bvE{NliIem%40be%40))')


import urllib.request

url = "https://img3.idealista.com/blur/WEB_DETAIL-L-P/0/id.pro.es.image.master/15/c3/a2/876430301.jpg"

r = urllib.request.urlopen(url)
with open("wind_turbine.jpg", "wb") as f:
	f.write(r.read())