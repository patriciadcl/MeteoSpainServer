# -*- coding: utf-8 -*-
class PredicionDia:
    def __init__(self, f_pronostico, prob_precipitacion, cota_nieve, estado_cielo, viento, racha_max, temperatura,
                 s_termica, humedad_rel, uv_max):
        self.__prob_precipitacion = prob_precipitacion
        self.__cota_nieve = cota_nieve
        self.__f_pronostico = f_pronostico
        self.__estado_cielo = estado_cielo
        self.__viento = viento
        self.__racha_max = racha_max
        self.__temperatura = temperatura
        self.__s_termica = s_termica
        self.__humedad_rel = humedad_rel
        self.__uv_max = uv_max

    @property
    def prob_precipitacion(self):
        return self.__prob_precipitacion

    @property
    def cota_nieve(self):
        return self.__cota_nieve

    @property
    def estado_cielo(self):
        return self.__estado_cielo

    @property
    def viento(self):
        return self.__viento

    @property
    def f_pronostico(self):
        return self.__f_pronostico

    @property
    def temperatura(self):
        return self.__temperatura

    @property
    def s_termica(self):
        return self.__s_termica

    @property
    def racha_max(self):
        return self.__racha_max

    @property
    def humedad_rel(self):
        return self.__humedad_rel

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


class PrediccionHoras(PredicionDia):
    def __init__(self, f_validez, orto, ocaso, estado_cielo, precipitacion, prob_precipitacion, prob_tormenta, nieve,
                 prob_nieve, viento, racha_max, temperatura, s_termica, humedad_rel):
        super().__init__(f_validez, prob_precipitacion, "ND", estado_cielo, viento, racha_max, temperatura, s_termica,
                         humedad_rel, "ND")
        self.__orto = orto
        self.__ocaso = ocaso
        self.__precipitacion = precipitacion
        self.__prob_tormenta = prob_tormenta
        self.__nieve = nieve
        self.__prob_nieve = prob_nieve

    @property
    def orto(self):
        return self.__orto

    @property
    def ocaso(self):
        return self.__ocaso

    @property
    def precipitacion(self):
        return self.__precipitacion

    @property
    def prob_tormenta(self):
        return self.__prob_tormenta

    @property
    def nieve(self):
        return self.__nieve

    @property
    def prob_nieve(self):
        return self.__prob_nieve

    @property
    def to_dict(self):
        propiedades = dict()
        for k, v in self.__dict__.items():
            key = k.split("__")[1]
            propiedades[key] = v
        return propiedades


class Municipio:
    def __init__(self, id_aemet, f_elaboracion, pred_diaria, pred_horaria):
        self.__id_aemet = id_aemet
        self.__f_elaboracion = f_elaboracion
        self.__pred_diaria = pred_diaria
        self.__pred_horaria = pred_horaria

    @property
    def id_aemet(self):
        return self.__id_aemet

    @property
    def f_elaboracion(self):
        return self.__f_elaboracion

    @property
    def pred_diaria(self):
        return self.__pred_diaria

    @property
    def pred_horaria(self):
        return self.__pred_horaria

    @pred_diaria.setter
    def pred_diaria(self, prediccion):
        self.__pred_diaria = prediccion

    @pred_horaria.setter
    def pred_horaria(self, prediccion):
        self.__pred_horaria = prediccion

    @property
    def to_dict(self):
        propiedades = dict()
        for k, v in self.__dict__.items():
            key = k.split("__")[1]
            if key == "pred_diaria":
                pred_diaria = list()
                for prediccion in v:
                    pred_diaria.append(prediccion.to_dict)
                propiedades[key] = pred_diaria
            elif key == "pred_horaria":
                pred_horaria = list()
                for prediccion in v:
                    pred_horaria.append(prediccion.to_dict)
                propiedades[key] = pred_horaria
            else:
                propiedades[key] = v
        return propiedades
