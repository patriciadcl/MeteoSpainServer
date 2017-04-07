import requests
import json


class AemetAPI:

    DATOS_AEMET = dict(
        AEMET_API_KEY="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwYXRyaWNpYWRjbEBnbWFpbC5jb20iLCJqdGkiOiI3" +
                      "MGU3ZjQ5Yy05ZGY1LTQ3ZDEtYTViMy05YjBmOWJhNDFkMmMiLCJleHAiOjE0OTY5MzQxNjMsI" +
                      "mlzcyI6IkFFTUVUIiwiaWF0IjoxNDg5MTU4MTYzLCJ1c2VySWQiOiI3MGU3ZjQ5Yy05ZGY1LT" +
                      "Q3ZDEtYTViMy05YjBmOWJhNDFkMmMiLCJyb2xlIjoiIn0.qyhEVJ3tiUyq7UzDRHmXGHS8Icx" +
                      "zZoej1V3KnSN9XpU",
        URL_BASE="https://opendata.aemet.es/opendata/api/prediccion", PATH_MONTAÑA="/especifica/montaña/pasada/area",
        PATH_MONTAÑA_DIA="/dia", PATH_MUNICIPIO="/especifica/municipio", PATH_MUNICIPIO_DIARIA="/diaria",
        PATH_MUNICIPIO_HORARIA="/horaria", PATH_PLAYA="/especifica/playa", PATH_MARITIMA="/maritima",
        PATH_ALTAMAR="/altamar/area", PATH_COSTERA="/costera/costa")

    COD_RESPONSE_OK = 200
    COD_RESPONSE_ERROR = dict(no_autorizado=["401", "No Autorizado"], incorrecta=["404", "Peticion incorrecta"],
                              conexiones=["429", "Demasiadas conexiones"])
    AREAS_ALTAMAR = (0, 1, 2)
    DIAS_MONTAÑA = (0, 1, 2, 3)
    AREAS_COSTA = (40, 41, 42, 43, 44, 45, 46, 47)

    @classmethod
    def get_prediccion(cls, url):

        querystring = {
            "api_key": cls.DATOS_AEMET["AEMET_API_KEY"]}

        headers = {
            'cache-control': "no-cache"
        }
        aemet_response = requests.request("GET", url, headers=headers, params=querystring, verify=False)

        json_response = json.loads(aemet_response.text)

        estado = json_response["estado"]

        if estado == cls.COD_RESPONSE_OK:
            return estado, cls.get_prediccion_datos(json_response["datos"])
        else:
            return estado, json_response["descripcion"]

    @staticmethod
    def get_prediccion_datos(url):

        headers = {
            'cache-control': "no-cache"
        }
        aemet_datos = requests.request("GET", url, headers=headers, verify=False)

        return aemet_datos.text

    @classmethod
    def url_montaña(cls, id_area, dia):
        address = cls.DATOS_AEMET["PATH_MONTAÑA"] + "/" + id_area + cls.DATOS_AEMET["PATH_MONTAÑA_DIA"] + "/" + dia
        url = cls.DATOS_AEMET["URL_BASE"] + address
        return url

    @classmethod
    def url_municipio_dia(cls, id_municipio):
        url = cls.DATOS_AEMET["URL_BASE"] + cls.DATOS_AEMET["PATH_MUNICIPIO"] + \
              cls.DATOS_AEMET["PATH_MUNICIPIO_DIARIA"] + "/" + id_municipio
        return url

    @classmethod
    def url_municipio_horas(cls, id_municipio):
        url = cls.DATOS_AEMET["URL_BASE"] + cls.DATOS_AEMET["PATH_MUNICIPIO"] + \
              cls.DATOS_AEMET["PATH_MUNICIPIO_HORARIA"] + "/" + id_municipio
        return url

    @classmethod
    def url_playa(cls, id_playa):
        url = cls.DATOS_AEMET["URL_BASE"] + cls.DATOS_AEMET["PATH_PLAYA"] + "/" + id_playa
        return url

    @classmethod
    def url_altamar(cls, id_altamar):
        url = cls.DATOS_AEMET["URL_BASE"] + cls.DATOS_AEMET["PATH_MARITIMA"] + \
              cls.DATOS_AEMET["PATH_ALTAMAR"] + "/" + id_altamar
        return url

    @classmethod
    def url_costa(cls, id_costa):
        url = cls.DATOS_AEMET["URL_BASE"] + cls.DATOS_AEMET["PATH_MARITIMA"] + \
              cls.DATOS_AEMET["PATH_COSTERA"] + "/" + id_costa
        return url
