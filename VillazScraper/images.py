from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import shutil
import pathlib
import sys

class Images(object):
    """
    Clase Images encargada de buscar las imágenes vinculadas a un inmueble y generar un dataframe con la dirección
    de las mismas y descargar los ficheros a una ruta específica.
    """

    def __init__(self, driver:webdriver, code):
        """
        Constructor de Images
        :param driver: webdriver de selenium a utilizar para encontrar las imagenes.
        :param code: Código del inmueble sobre el que se buscan las imagenes
        """
        self.driver = driver
        self.code = code

    def get_images(self) -> pd.DataFrame:
        """
        Retorna un dataframe con un listado de todas las imágenes que existen en la página de detalle del inmueble.
        El dataframe tiene dos columnas.
        url -> URL donde se encuentra la imagen.
        code -> Código del inmueble al que pertece la imagen.
        :return: pd.DataFrame
        """
        div_more_photos = self.driver.find_element_by_id("show-more-photos-button")
        div_more_photos.find_element_by_tag_name("a").click()

        images = WebDriverWait(self.driver, 2).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@id="main-multimedia"]//img'))
        )
        images = pd.DataFrame(data=[image.get_attribute('data-ondemand-img') for image in images], columns=['url'])
        images['code'] = self.code
        return images

    @staticmethod
    def download_images(df, save_location='../images'):
        """
        Descarga las imagenes de las viviendas a partir de las urls generadas en el dataframe de imagenes.
        :param df: Dataframe con los datos de las urls de las imagenes y el código de la entrada a la que pertenecen.
        :param save_location: Localización base donde se almacenarán las imágenes, por defecto es en local, pero
        se podría indicar un almacenamiento en S3, HDFS, etc.
        :return:
        """
        for entries in df.values:
            image_name = entries[0].split('/')[-1]
            print("Downloading: {0}".format(entries[0]))
            result = requests.get(entries[0], stream=True)
            if result.status_code == 200:
                path = '../{0}/{1}'.format(save_location, entries[1])
                if not pathlib.Path(path).exists():
                    pathlib.Path(path).mkdir()
                with open('{0}/{1}'.format(path, image_name), 'wb') as f:
                    result.raw.decode_content = True
                    shutil.copyfileobj(result.raw, f)


if __name__ == '__main__':
    Images.download_images(pd.read_csv(sys.argv[0]))