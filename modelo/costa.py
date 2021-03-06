# -*- coding: utf-8 -*-
class Costa:
    def __init__(self, id_aemet, id_api, f_elaboracion, f_inicio, f_fin, situacion, aviso, tendencia, zonas):
        self.__id_aemet = id_aemet
        self.__id_api = id_api
        self.__situacion = situacion
        self.__aviso = aviso
        self.__tendencia = tendencia
        self.__f_elaboracion = f_elaboracion
        self.__f_inicio = f_inicio
        self.__f_fin = f_fin
        self.__zonas = zonas

    @property
    def id_aemet(self):
        return self.__id_aemet

    @property
    def id_api(self):
        return self.__id_api

    @property
    def situacion(self):
        return self.__situacion

    @property
    def aviso(self):
        return self.__aviso

    @property
    def tendencia(self):
        return self.__tendencia

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
    def zonas(self):
        return self.__zonas

    @property
    def to_dict(self):
        propiedades = dict()
        for k, v in self.__dict__.items():
            key = k.split("__")[1]
            if key == "zonas":
                zonas = list()
                for zona in v:
                    zonas.append(zona.to_dict)
                propiedades[key] = zonas
            else:
                propiedades[key] = v
        return propiedades


class Zona:
    def __init__(self, id_aemet, texto):
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
        propiedades = dict()
        for k, v in self.__dict__.items():
            key = k.split("__")[1]
            propiedades[key] = v
        return propiedades
