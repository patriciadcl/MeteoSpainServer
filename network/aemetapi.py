# -*- coding: utf-8 -*-
import json

import requests


class AemetAPI:

    AEMET_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwYXRyaWNpYWRjbEBnbWFpbC5" +\
                    "jb20iLCJqdGkiOiJlMTlkMTFmYy05ZjY3LTRhODUtYTRjNC0wY2E2NDI" +\
                    "zMDkyZGEiLCJleHAiOjE1MDg3NjE3NjksImlzcyI6IkFFTUVUIiwiaWF" +\
                    "0IjoxNTAwOTg1NzY5LCJ1c2VySWQiOiJlMTlkMTFmYy05ZjY3LTRhODUt" +\
                    "YTRjNC0wY2E2NDIzMDkyZGEiLCJyb2xlIjoiIn0.JftnuJlo0F6ypgi7" +\
                    "-1pWRlBeP6f5L14HIA7rI1px_Cg"
    URL_BASE = "https://opendata.aemet.es/opendata/api/prediccion"
    PATH_MONTAÑA = "/especifica/montaña/pasada/area"
    PATH_MONTAÑA_DIA = "/dia"
    PATH_MUNICIPIO = "/especifica/municipio"
    PATH_MUNICIPIO_DIARIA = "/diaria"
    PATH_MUNICIPIO_HORARIA = "/horaria"
    PATH_PLAYA = "/especifica/playa"
    PATH_MARITIMA = "/maritima"
    PATH_ALTAMAR = "/altamar/area"
    PATH_COSTERA = "/costera/costa"

    COD_RESPONSE_OK = 200
    COD_PET_INCORRECTA = 404
    COD_NO_AUTORIZADO = 401
    COD_CONEXIONES = 429
    COD_RESPONSE_ERROR_MESSAGE = {COD_NO_AUTORIZADO: "No Autorizado",
                                  COD_PET_INCORRECTA: "Peticion incorrecta",
                                  COD_CONEXIONES: "Demasiadas conexiones"}
    AREAS_ALTAMAR = (0, 1, 2)
    DIAS_MONTAÑA = (0, 1, 2, 3)
    AREAS_COSTA = (40, 41, 42, 43, 44, 45, 46, 47)

    aemet_api_key = None

    @classmethod
    def __init__(cls, base_dir):

        cls.aemet_api = api.AemetAPI()
        cls.meteo_ddbb = dd_bb
        cls.incremento_horas = horas

    @classmethod
    def get_response_error(cls, cod_error, texto=None):
        response = None
        if cod_error in cls.COD_RESPONSE_ERROR_MESSAGE.keys():
            mensaje = texto if texto else cls.COD_RESPONSE_ERROR_MESSAGE[cod_error]
            response = dict(estado=cod_error, datos=mensaje)
        return response

    @classmethod
    def get_prediccion(cls, url):

        querystring = {
            "api_key": cls.AEMET_API_KEY}

        headers = {
            'cache-control': "no-cache"
        }
        try:
            aemet_response = requests.request("GET", url, headers=headers, params=querystring, verify=False)
            json_response = json.loads(aemet_response.text)
            estado = json_response["estado"]
            if estado == cls.COD_RESPONSE_OK:
                return estado, cls.get_prediccion_datos(json_response["datos"])
            else:
                return estado, json_response["descripcion"]
        except Exception as exc:
            print("EXCEPTION: ", format(exc))

    @staticmethod
    def get_prediccion_datos(url):

        headers = {
            'cache-control': "no-cache"
        }
        try:
            aemet_datos = requests.request("GET", url, headers=headers, verify=False)
            return aemet_datos.text
        except Exception as exc:
            print("EXCEPTION: ", format(exc))

    @classmethod
    def url_montaña(cls, id_area, dia):
        path = cls.PATH_MONTAÑA + "/" + id_area + cls.PATH_MONTAÑA_DIA + "/" + dia
        url = cls.URL_BASE + path
        return url

    @classmethod
    def url_municipio_dia(cls, id_municipio):
        url = cls.URL_BASE + cls.PATH_MUNICIPIO + \
              cls.PATH_MUNICIPIO_DIARIA + "/" + id_municipio
        return url

    @classmethod
    def url_municipio_horas(cls, id_municipio):
        url = cls.URL_BASE + cls.PATH_MUNICIPIO + \
              cls.PATH_MUNICIPIO_HORARIA + "/" + id_municipio
        return url

    @classmethod
    def url_playa(cls, id_playa):
        url = cls.URL_BASE + cls.PATH_PLAYA + "/" + id_playa
        return url

    @classmethod
    def url_altamar(cls, id_altamar):
        url = cls.URL_BASE + cls.PATH_MARITIMA + \
              cls.PATH_ALTAMAR + "/" + id_altamar
        return url

    @classmethod
    def url_costa(cls, id_costa):
        url = cls.URL_BASE + cls.PATH_MARITIMA + \
              cls.PATH_COSTERA + "/" + id_costa
        return url
