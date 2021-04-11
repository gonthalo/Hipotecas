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

driver = webdriver.Firefox(executable_path=r'/home/gonthalo/.jaquersoft/Hipotecas/geckodriver')
driver.get('https://www.idealista.com')
driver.implicitly_wait(10)
driver.get('https://www.idealista.com/areas/venta-viviendas/?shape=((cz{uF|ltUckBuWg{AgnFpYqwDpbEefChg%40bvE{NliIem%40be%40))')