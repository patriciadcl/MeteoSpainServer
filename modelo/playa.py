# -*- coding: utf-8 -*-
class Dia:

    def __init__(self, f_pronostico, estado_cielo, viento, oleaje, t_maxima, s_termica, t_agua, uv_max):
        self.__f_pronostico = f_pronostico
        self.__estado_cielo = estado_cielo
        self.__viento = viento
        self.__oleaje = oleaje
        self.__t_maxima = t_maxima
        self.__s_termica = s_termica
        self.__t_agua = t_agua
        self.__uv_max = uv_max

    @property
    def f_pronostico(self):
        return self.__f_pronostico

    @property
    def estado_cielo(self):
        return self.__estado_cielo

    @property
    def viento(self):
        return self.__viento

    @property
    def oleaje(self):
        return self.__oleaje

    @property
    def t_maxima(self):
        return self.__t_maxima

    @property
    def s_termica(self):
        return self.__s_termica

    @property
    def t_agua(self):
        return self.__t_agua

    @property
    def uv_max(self):
        return self.__uv_max

    @property
    def to_dict(self):
        propiedades = dict()
        for k, v in self.__dict__.items():
            key = k.split("__")[1]
            propiedades[key] = v
        return propiedades


class Playa:
    def __init__(self, id_aemet, f_elaboracion, dias):
        self.__id_aemet = id_aemet
        self.__f_elaboracion = f_elaboracion
        self.__dias = dias

    @property
    def id_aemet(self):
        return self.__id_aemet

    @property
    def f_elaboracion(self):
        return self.__f_elaboracion

    @property
    def prediccion(self):
        return self.__dias

    @property
    def to_dict(self):
        propiedades = dict()
        for k, v in self.__dict__.items():
            key = k.split("__")[1]
            if key == "dias":
                dias = list()
                for dia in v:
                    dias.append(dia.to_dict)
                propiedades[key] = dias
            else:
                propiedades[key] = v
        return propiedades
