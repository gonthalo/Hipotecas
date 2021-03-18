
class Vivienda(object):
    """
    Clase Vivienda
    """

    code = None
    link = None
    address = None
    barrio = None
    distrito = None
    ciudad = None
    lat = None
    lon = None
    price = None
    area = None
    has_elevator = None
    floor = None
    exterior = None
    rooms = None

    def __init__(self, dictionary=None):
        """
        Inicializa la clase vivienda a partir de un diccionario
        :param dictionary:
        """

        if dictionary:
            self.code = dictionary['code'] if 'code' in dictionary else None
            self.link = dictionary['link'] if 'link' in dictionary else None
            self.address = dictionary['address'] if 'address' in dictionary else None
            self.barrio = dictionary['barrio'] if 'barrio' in dictionary else None
            self.distrito = dictionary['distrito'] if 'distrito' in dictionary else None
            self.ciudad = dictionary['ciudad'] if 'ciudad' in dictionary else None
            self.lat = dictionary['lat'] if 'lat' in dictionary else None
            self.lon = dictionary['lon'] if 'lon' in dictionary else None
            self.price = dictionary['price'] if 'price' in dictionary else None
            self.area = dictionary['area'] if 'area' in dictionary else None
            self.has_elevator = dictionary['has_elevator'] if 'has_elevator' in dictionary else None
            self.floor = dictionary['floor'] if 'floor' in dictionary else None
            self.exterior = dictionary['exterior'] if 'exterior' in dictionary else None
            self.rooms = dictionary['rooms'] if 'rooms' in dictionary else None

    def to_dict(self):
        """
        Retorna un diccionario con los datos de la vivienda.
        :return:
        """
        return {'code': self.code,
                'link': self.link,
                'address': self.address,
                'barrio': self.barrio,
                'distrito': self.distrito,
                'ciudad': self.ciudad,
                'lat': self.lat,
                'lon': self.lon,
                'price': self.price,
                'area': self.area,
                'has_elevator': self.has_elevator,
                'floor': self.floor,
                'exterior': self.exterior,
                'rooms': self.rooms}