# -*- coding: utf-8 -*-
import os

import network.aemetapi as api

import network.servidorutils as servidor

from data.basedatos import BaseDatos

from flask import Flask

app = Flask(__name__)

aemet_api = api.AemetAPI()

base_dir = os.path.dirname(os.path.realpath('__file__'))

meteoserver_ddbb = BaseDatos()

utils = servidor.ServidorUtils(base_dir, meteoserver_ddbb, 2)


@app.route('/')
def index():
    return "Bienvenido al servidor API de la aplicacion Meteo España para plataforma Android"


@app.route('/datos/provincia/<int:cod_provincia>/municipios')
def datos_municipios(cod_provincia):
    if 1 < cod_provincia < 53:
        response = utils.get_datos_municipios(cod_provincia)
    else:
        response = str(aemet_api.get_response_error(aemet_api.COD_PET_INCORRECTA))
    return response


@app.route('/datos/<dato>')
def datos(dato):
    if dato not in utils.FICHEROS_JSON:
        response = str(aemet_api.get_response_error(aemet_api.COD_PET_INCORRECTA, utils.MENSAJE_ERROR_FICHEROS))
    else:
        response = utils.get_datos(dato)
    return response


@app.route('/predicciones/altamar/<int:area>')
def altamar(area):
    if area not in aemet_api.AREAS_ALTAMAR:
        response = str(aemet_api.get_response_error(aemet_api.COD_PET_INCORRECTA))
    else:
        response = utils.get_altamar(area)
    return response


@app.route('/predicciones/costa/<int:area>')
def costa(area):
    if area not in aemet_api.AREAS_COSTA:
        response = str(aemet_api.get_response_error(aemet_api.COD_PET_INCORRECTA))
    else:
        response = utils.get_costa(area)
    return response


@app.route('/predicciones/montaña/<area>/dia/<int:dia>')
def montaña(area, dia):
    if dia not in aemet_api.DIAS_MONTAÑA:
        response = str(aemet_api.get_response_error(aemet_api.COD_PET_INCORRECTA))
    else:
        response = utils.get_montaña(area, dia)
    return response


@app.route('/predicciones/municipio/diaria/<int:id_municipio>')
def municipo_diaria(id_municipio):
    response = utils.get_municipo_diaria(id_municipio)
    return response


@app.route('/predicciones/municipio/horaria/<int:id_municipio>')
def municipo_horaria(id_municipio):
    response = utils.get_municipo_horaria(id_municipio)
    return response


@app.route('/predicciones/playa/<int:id_playa>')
def playa(id_playa):
    response = utils.get_playa(id_playa)
    return response


if __name__ == '__main__':
    app.run(debug=True)
