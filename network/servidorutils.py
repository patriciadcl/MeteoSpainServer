# -*- coding: utf-8 -*-
import json

import os

import network.aemetapi as api

import network.utils as utils

from network.jsonamodelo import JsonAModelo
from modelo.municipio import Municipio



class ServidorUtils:
    base_dir = None
    aemet_api = None
    meteo_ddbb = None
    incremento_horas = 2
    FICHEROS_JSON = ("areas_altamar", "areas_costa", "areas_montañas", "cc_aa", "estado_cielo", "estados_playa",
                     "municipios", "playas", "provincias", "provincias_costas", "subzonas_costas")
    MENSAJE_ERROR_FICHEROS = "Los datos que se pueden obtener son : " + ", ".join(FICHEROS_JSON)

    @classmethod
    def __init__(cls, base_dir, dd_bb, horas):
        cls.base_dir = base_dir
        cls.aemet_api = api.AemetAPI()
        cls.meteo_ddbb = dd_bb
        cls.incremento_horas = horas

    @classmethod
    def get_datos(cls, dato):
        response = None
        try:
            if dato is not "municipios":
                json_file = os.path.join(cls.base_dir, "json", dato + ".json")
                with open(json_file, "r", encoding='utf-8') as f_open:
                    contenido = f_open.read()
                    js = json.loads(contenido)
                    response = dict(estado=cls.aemet_api.COD_RESPONSE_OK, datos=js)
        except Exception as ex:
            response = cls.aemet_api.get_response_error(cls.aemet_api.COD_PET_INCORRECTA, texto=format(ex))
        finally:
            return str(response)

    @classmethod
    def get_datos_municipios(cls, cod_provincia):
        datos = None
        en_ddbb, response_ddbb = cls.meteo_ddbb.get_datos_municipios(cod_provincia)
        if en_ddbb:
            print("datos municipios from db")
            response_estado = cls.aemet_api.COD_RESPONSE_OK
            datos = response_ddbb
        else:
            response_estado = cls.aemet_api.COD_PET_INCORRECTA
        response = dict(estado=response_estado, datos=datos)
        return str(response)


    @classmethod
    def get_altamar(cls, area):
        # Predicción para un periodo de 24 horas de las condiciones meteorológicas para el área
        # marítima pasada por parámetro. Actualizacion una vez 24h
        # comprobamos si la tenemos en la base de datos
        hoy = utils.get_hoy()
        en_ddbb, response_ddbb = cls.meteo_ddbb.get_pred_altamar(area, hoy, hoy)
        if en_ddbb:
            print("altamar from db")
            response_estado = cls.aemet_api.COD_RESPONSE_OK
            datos = response_ddbb
        else:
            print("altamar from aemet")
            url = cls.aemet_api.url_altamar(str(area))
            response_estado, response_datos = cls.aemet_api.get_prediccion(url)
            if response_estado == cls.aemet_api.COD_RESPONSE_OK:
                altamar = JsonAModelo.json_a_altamar(area, response_datos)
                datos = altamar.to_dict
                print("Insertado ", cls.meteo_ddbb.insert_pred_altamar(area, altamar.f_elaboracion, altamar.f_inicio,
                                                                  json.dumps(datos)))
            else:
                datos = response_datos
        response = dict(estado=response_estado, datos=datos)
        return str(response)

    @classmethod
    def get_costa(cls, area):
        # Predicción para un periodo de 24 horas de las condiciones meteorológicas para la zona
        # costera pasada por parámetro. Actualizacion una vez 24h
        # comprobamos si la tenemos en la base de datos
        hoy = utils.get_hoy()
        en_ddbb, response_ddbb = cls.meteo_ddbb.get_pred_costa(area, hoy, hoy)
        if en_ddbb:
            print("costa from db")
            response_estado = cls.aemet_api.COD_RESPONSE_OK
            datos = response_ddbb
        else:
            print("costa from aemet")
            url = cls.aemet_api.url_costa(str(area))
            response_estado, response_datos = cls.aemet_api.get_prediccion(url)
            if response_estado == cls.aemet_api.COD_RESPONSE_OK:
                costa = JsonAModelo.json_a_costa(area, response_datos)
                datos = costa.to_dict
                print("Insertado ",
                      cls.meteo_ddbb.insert_pred_costa(area, costa.f_elaboracion, costa.f_inicio, json.dumps(datos)))
            else:
                datos = response_datos
        response = dict(estado=response_estado, datos=datos)
        return str(response)

    @classmethod
    def get_montaña(cls, area, dia):
        # Predicción meteorológica para la zona montañosa que se pasa como parámetro (area) con
        # validez para el día (día). Periodicidad de actualización: continuamente
        # comprobamos si la tenemos en la base de datos
        hoy = utils.get_hoy()
        f_pronostico = utils.get_proximo_dia(dia)
        en_ddbb, response_ddbb = cls.meteo_ddbb.get_pred_montaña(area, hoy, f_pronostico, cls.incremento_horas)
        if en_ddbb:
            print("montaña from db")
            response_estado = cls.aemet_api.COD_RESPONSE_OK
            datos = response_ddbb
        else:
            print("montaña from aemet")
            url = cls.aemet_api.url_montaña(area, str(dia))
            response_estado, response_datos = cls.aemet_api.get_prediccion(url)
            if response_estado == cls.aemet_api.COD_RESPONSE_OK:
                montaña = JsonAModelo.json_a_montaña(response_datos, dia)
                datos = montaña.to_dict
                print("Insertado ", cls.meteo_ddbb.insert_pred_montaña(area, montaña.f_elaboracion,
                                                                       montaña.f_pronostico, json.dumps(datos)))
            else:
                datos = response_datos
        response = dict(estado=response_estado, datos=datos)
        return str(response)

    @classmethod
    def get_municipo(cls, id_municipio):
        # Predicción diaria válida para 7 días para todos los municipios de España.
        # Actualizacion una vez 24h
        hoy = utils.get_hoy()
        en_ddbb, response_ddbb = cls.meteo_ddbb.get_pred_municipio(id_municipio, hoy, cls.incremento_horas)
        if en_ddbb:
            print("municipio from db")
            response_estado = cls.aemet_api.COD_RESPONSE_OK
            prediccion = response_ddbb
        else:
            print("municipio from aemet")
            url = cls.aemet_api.url_municipio_dia(str(id_municipio))
            response_estado, response_datos = cls.aemet_api.get_prediccion(url)
            if response_estado == cls.aemet_api.COD_RESPONSE_OK:
                id_aemet, f_elaboracion, pred_diaria = JsonAModelo.json_a_municipio(response_datos, True)
                pred_municipio = Municipio(id_aemet,f_elaboracion,pred_diaria,pred_diaria)
                url = cls.aemet_api.url_municipio_horas(str(id_municipio))
                response_estado, response_datos = cls.aemet_api.get_prediccion(url)
                if response_estado == cls.aemet_api.COD_RESPONSE_OK:
                    id_aemet, f_elaboracion, pred_horaria = JsonAModelo.json_a_municipio(response_datos, False)
                    pred_municipio.pred_horaria = pred_horaria
                    prediccion = pred_municipio.to_dict
                    print("Insertado ", cls.meteo_ddbb.insert_pred_municipio(id_municipio, pred_municipio.f_elaboracion,
                                                                             hoy, json.dumps(prediccion)))
                else:
                    prediccion = response_datos
            else:
                prediccion = response_datos
            print("municipio from aemet")

        response = dict(estado=response_estado, datos=prediccion)
        return str(response)

    @classmethod
    def get_playa(cls, id_playa):
        """ La predicción diaria de la playa que se pasa como parámetro. Establece el estado de 
        nubosidad para unas horas determinadas, las 11 y las 17 hora oficial. 
        Se analiza también si se espera precipitación en el entorno de esas horas, 
        entre las 08 y las 14 horas y entre las 14 y 20 horas. Actualizacion una vez 24h"""
        # comprobamos si la tenemos en la base de datos
        hoy = utils.get_hoy()
        en_ddbb, response_ddbb = cls.meteo_ddbb.get_pred_playa(id_playa, hoy, hoy)
        if en_ddbb:
            print("playa from bbdd")
            response_estado = cls.aemet_api.COD_RESPONSE_OK
            datos = response_ddbb
        else:
            print("playa from aemet")
            url = cls.aemet_api.url_playa(str(id_playa).zfill(7))
            response_estado, response_datos = cls.aemet_api.get_prediccion(url)
            if response_estado == cls.aemet_api.COD_RESPONSE_OK:
                playa = JsonAModelo.json_a_playa(response_datos)
                datos = playa.to_dict
                print("Insertado ", cls.meteo_ddbb.insert_pred_playa(id_playa, playa.f_elaboracion, hoy,
                                                                     json.dumps(datos)))
            else:
                datos = response_datos
        response = dict(estado=response_estado, datos=datos)
        return str(response)

    @classmethod
    def in_ficheros(cls, fichero):
        return fichero in cls.FICHEROS_JSON
