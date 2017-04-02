class Lugar:
    def __init__(self, minima, st_minima, maxima, st_maxima, nombre, altitud):
        self.__minima = minima
        self.__st_minima = st_minima
        self.__maxima = maxima
        self.__st_maxima = st_maxima
        self.__nombre = nombre
        self.__altitud = altitud

    @property
    def minima(self):
        return self.__minima

    @property
    def st_minima(self):
        return self.__st_minima

    @property
    def maxima(self):
        return self.__maxima

    @property
    def st_maxima(self):
        return self.__st_maxima

    @property
    def nombre(self):
        return self.__nombre

    @property
    def altitud(self):
        return self.__altitud


    @property
    def to_dict(self):
        diccionario = dict()
        for k, v in self.__dict__.items():
            key = k.split("__")[1]
            diccionario[key] = v
        return diccionario

class Montaña:
    def __init__(self, id_api, estado_cielo, precipitaciones, tormentas, temperaturas, viento,s_termica):
        self.__id_api = id_api
        self.__estado_cielo = estado_cielo
        self.__precipitaciones = precipitaciones
        self.__tormentas = tormentas
        self.__temperaturas = temperaturas
        self.__viento = viento
        self.__s_termica = s_termica

    @property
    def id_api(self):
        return self.__id_api

    @property
    def estado_cielo(self):
        return self.__estado_cielo

    @property
    def precipitaciones(self):
        return self.__precipitaciones

    @property
    def tormentas(self):
        return self.__tormentas

    @property
    def temperaturas(self):
        return self.__temperaturas

    @property
    def viento(self):
        return self.__viento

    @property
    def s_termica(self):
        return self.__s_termica

    @property
    def to_dict(self):
        diccionario = dict()
        for k, v in self.__dict__.items():
            key = k.split("__")[1]
            diccionario[key] = v
        return diccionario

