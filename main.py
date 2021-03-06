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

TIPOS_PETICION = {"altamar", "costa", "montaña", "municipio", "playa"}


@app.route('/')
def index():
    return "Bienvenido al servidor API de la aplicacion Meteo España para plataforma Android"


@app.route('/datos/<dato>')
def datos(dato):
    if dato not in utils.FICHEROS_JSON:
        response = str(aemet_api.get_response_error(aemet_api.COD_PET_INCORRECTA, utils.MENSAJE_ERROR_FICHEROS))
    else:
        response = utils.get_datos(dato)
    return response


@app.route('/predicciones/<tipo>/metadatos')
def metadatos(tipo):
    if tipo not in TIPOS_PETICION:
        response = str(aemet_api.get_response_error(aemet_api.COD_PET_INCORRECTA))
    else:
        response = utils.get_metadatos(tipo)
    return response


@app.route('/predicciones/altamar/<area>')
def altamar(area):
    if int(area) not in aemet_api.AREAS_ALTAMAR:
        response = str(aemet_api.get_response_error(aemet_api.COD_PET_INCORRECTA))
    else:
        response = utils.get_altamar(area)
    return response


@app.route('/predicciones/costa/<area>')
def costa(area):
    if int(area) not in aemet_api.AREAS_COSTA:
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


@app.route('/predicciones/municipio/<id_municipio>')
def municipo(id_municipio):
    response = utils.get_municipio(id_municipio)
    return response


@app.route('/predicciones/playa/<id_playa>')
def playa(id_playa):
    response = utils.get_playa(id_playa)
    return response


if __name__ == '__main__':
    app.run(debug=True)
