import network.aemetapi as api
import requests
from bottle import get

_predicciones = set()


@get('/predicciones/altamar/<area>')
def get_altamar(area):

    url = api.AemetAPI.url_altamar(area)
    # querystring = {
    #     "api_key": api.AemetAPI.DATOS_AEMET["AEMET_API_KEY"]}
    #
    # headers = {
    #     'cache-control': "no-cache"
    # }
    #
    # aemet_response = requests.request("GET", url, headers=headers, params=querystring)

    return "Altamar " + area


@get('/predicciones/costa/<area>')
def get_costa(area):
    return "Costa " + area


@get('/predicciones/montaña/<area>/dia/<dia>')
def get_montaña(area, dia):
    return "Montaña " + area + "Dia " + dia


@get('/predicciones/municipio/diaria/<municipio>')
def get_municipo_diaria(municipio):
    return "Municipio " + municipio


@get('/predicciones/municipio/horaria/<municipio>')
def get_municipo_horaria(municipio):
    return "Municipio " + municipio


@get('/predicciones/playa/<playa>')
def get_playa(playa):
    return "Playa " + playa
