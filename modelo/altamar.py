class Zona:
    def __init__(self,id_aemet,id_api,f_elaboracion,f_inicio,f_fin,texto,subzonas):
        self.__id_aemet = id_aemet
        self.__id_api = id_api
        self.__texto = texto
        self.__f_elaboracion = f_elaboracion
        self.__f_inicio = f_inicio
        self.__f_fin = f_fin
        self.__sub_zonas = subzonas

    @property
    def id_aemet(self):
        return self.__id_aemet

    @property
    def id_api(self):
        return self.__id_api

    @property
    def texto(self):
        return self.__texto

    @property
    def f_elaboracion(self):
        return self.__f_elaboracion

    @property
    def f_inicio(self):
        return self.__f_inicio

    @property
    def f_fin(self):
        return self.__f_fin

    @property
    def sub_zonas(self):
        return self.__sub_zonas

    @property
    def to_dict(self):
        diccionario = dict()
        for k, v in self.__dict__.items():
            key = k.split("__")[1]
            diccionario[key] = v
        return diccionario


class SubZona:

    def __init__(self,id_aemet,texto):
        self.__id_aemet = id_aemet
        self.__texto = texto

    @property
    def id_aemet(self):
        return self.__id_aemet

    @property
    def texto(self):
        return self.__texto

    @property
    def to_dict(self):
        diccionario = dict()
        for k, v in self.__dict__.items():
            key = k.split("__")[1]
            diccionario[key] = v
        return diccionario

