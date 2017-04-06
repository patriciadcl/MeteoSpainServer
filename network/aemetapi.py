import json
import sys


class AemetAPI:

    url_base = ""
    api_key = ""
    path_montaña = ""
    path_montaña_dia = ""
    path_municipio = ""
    path_municipio_dia = ""
    path_municipio_hora = ""
    path_playa = ""
    path_maritima = ""
    path_altamar = ""
    path_costa = ""

    @classmethod
    def __init__(cls, archivo_aemet):
        try:
            f_open = open(archivo_aemet, encoding="utf-8")
            cadena_json = ""
            for line in f_open:
                cadena_json += line
            js = json.loads(cadena_json)
        except Exception as inst:
            print(inst.args)
            js = None

        if js:
            cls.url_base = js["URL_BASE"]
            cls.api_key = js["AEMET_API_KEY"]
            cls.path_montaña = js["PATH_MONTANA"]
            cls.path_montaña_dia = js["PATH_MONTANA_DIA"]
            cls.path_municipio = js["PATH_MUNICIPIO"]
            cls.path_municipio_dia = js["PATH_MUNICIPIO_DIARIA"]
            cls.path_municipio_hora = js["PATH_MUNICIPIO_HORARIA"]
            cls.path_maritima = js["PATH_MARITIMA"]
            cls.path_altamar = js["PATH_ALTAMAR"]
            cls.path_costa = js["PATH_COSTA"]
            cls.path_playa = js["PATH_PLAYA"]

    @classmethod
    def url_montaña(cls, id_area, dia):
        address = cls.path_montaña + "/" + id_area + cls.path_montaña_dia + "/" + dia
        url = cls.url_base + address
        return url

    @classmethod
    def url_municipio_dia(cls, id_municipio):
        url = cls.url_base + cls.path_municipio + cls.path_municipio_dia + "/" + id_municipio
        return url

    @classmethod
    def url_municipio_horas(cls, id_municipio):
        url = cls.url_base + cls.path_municipio + cls.path_municipio_hora + "/" + id_municipio
        return url

    @classmethod
    def url_playa(cls, id_playa):
        url = cls.url_base + cls.path_playa + "/" + id_playa
        return url

    @classmethod
    def url_altamar(cls, id_altamar):
        url = cls.url_base + cls.path_altamar + "/" + id_altamar
        return url

    @classmethod
    def url_costa(cls, id_costa):
        url = cls.url_base + cls.path_costa + "/" + id_costa
        return url
