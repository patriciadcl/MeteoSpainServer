# -*- coding: utf-8 -*-

import network.aemetapi as api
import network.jsonamodelo as amodelo
import os
import json

from flask import Flask, request

app = Flask(__name__)

aemet_api = api.AemetAPI()

base_dir = os.path.dirname(os.path.realpath('__file__'))


@app.route('/datos/areas_altamar', methods=['GET'])
@app.route('/datos/areas_costeras', methods=['GET'])
@app.route('/datos/areas_montaña', methods=['GET'])
@app.route('/datos/estado_cielo', methods=['GET'])
@app.route('/datos/estados_playa', methods=['GET'])
@app.route('/datos/cc_aa', methods=['GET'])
@app.route('/datos/municipios', methods=['GET'])
@app.route('/datos/playas', methods=['GET'])
@app.route('/datos/provincias_costas', methods=['GET'])
@app.route('/datos/provincias', methods=['GET'])
@app.route('/datos/subzonas_costas', methods=['GET'])
def get_datos():

    file = os.path.split(request.path)
    json_file = os.path.join(base_dir, "json", file[1] + ".json")
    try:
        f_open = open(json_file, "r", encoding='utf-8')
        contenido = f_open.read()
        js = json.loads(contenido)
        response = dict(estado=aemet_api.COD_RESPONSE_OK, datos=js)
        return str(response)
    except Exception as ex:
        response = dict(estado=aemet_api.COD_RESPONSE_ERROR["incorrecta"][0],
                        datos=format(ex))
        return str(response)


@app.route('/predicciones/altamar/<int:area>', methods=['GET'])
def get_altamar(area):
    if area not in aemet_api.AREAS_ALTAMAR:
        response = dict(estado=aemet_api.COD_RESPONSE_ERROR["incorrecta"][0],
                        datos=aemet_api.COD_RESPONSE_ERROR["incorrecta"][1])
    else:
        # TODO: Comprobar si esta en la base de datos
        # Este informe me parece que se hace una vez al dia, comprobar
        url = aemet_api.url_altamar(str(area))
        response_estado, response_datos = aemet_api.get_prediccion(url)
        if response_estado == aemet_api.COD_RESPONSE_OK:
            altamar = amodelo.JsonAModelo.json_a_altamar(response_datos)
            datos = altamar.to_dict
        else:
            datos = response_datos
        response = dict(estado=response_estado, datos=datos)
    return str(response)


@app.route('/predicciones/costa/<int:area>', methods=['GET'])
def get_costa(area):
    if area not in aemet_api.AREAS_COSTA:
        response = dict(estado=aemet_api.COD_RESPONSE_ERROR["incorrecta"][0],
                        datos=aemet_api.COD_RESPONSE_ERROR["incorrecta"][1])
    else:
        # TODO: Comprobar si esta en la base de datos
        # Este informe me parece que se hace una vez al dia, comprobar
        url = aemet_api.url_costa(str(area))
        response_estado, response_datos = aemet_api.get_prediccion(url)
        if response_estado == aemet_api.COD_RESPONSE_OK:
            costa = amodelo.JsonAModelo.json_a_costas(response_datos)
            datos = costa.to_dict
        else:
            datos = response_datos
        response = dict(estado=response_estado, datos=datos)
    return str(response)


@app.route('/predicciones/montaña/<area>/dia/<int:dia>', methods=['GET'])
def get_montaña(area, dia):
    if dia not in aemet_api.DIAS_MONTAÑA:
        response = dict(estado=aemet_api.COD_RESPONSE_ERROR["incorrecta"][0],
                        datos=aemet_api.COD_RESPONSE_ERROR["incorrecta"][1])
    else:
        # TODO: Comprobar si esta en la base de datos
        # Este informe me parece que se hace una vez al dia, comprobar
        url = aemet_api.url_montaña(area, str(dia))
        response_estado, response_datos = aemet_api.get_prediccion(url)
        if response_estado == aemet_api.COD_RESPONSE_OK:
            montaña = amodelo.JsonAModelo.json_a_montaña(response_datos, dia)
            datos = montaña.to_dict
        else:
            datos = response_datos
        response = dict(estado=response_estado, datos=datos)
    return str(response)


@app.route('/predicciones/municipio/diaria/<int:id_municipio>', methods=['GET'])
def get_municipo_diaria(id_municipio):
    # TODO: Comprobar si esta en la base de datos
    url = aemet_api.url_municipio_dia(str(id_municipio))
    response_estado, response_datos = aemet_api.get_prediccion(url)
    if response_estado == aemet_api.COD_RESPONSE_OK:
        municipio = amodelo.JsonAModelo.json_a_municipio(response_datos, True)
        datos = municipio.to_dict
    else:
        datos = response_datos
    response = dict(estado=response_estado, datos=datos)
    return "Municipio " + str(response)


@app.route('/predicciones/municipio/horaria/<int:id_municipio>', methods=['GET'])
def get_municipo_horaria(id_municipio):
    # TODO: Comprobar si esta en la base de datos
    url = aemet_api.url_municipio_horas(str(id_municipio))
    response_estado, response_datos = aemet_api.get_prediccion(url)
    if response_estado == aemet_api.COD_RESPONSE_OK:
        municipio = amodelo.JsonAModelo.json_a_municipio(response_datos, False)
        datos = municipio.to_dict
    else:
        datos = response_datos
    response = dict(estado=response_estado, datos=datos)
    return str(response)


@app.route('/predicciones/playa/<int:id_playa>', methods=['GET'])
def get_playa(id_playa):
    # TODO: Comprobar si esta en la base de datos
    url = aemet_api.url_playa(str(id_playa).zfill(7))
    response_estado, response_datos = aemet_api.get_prediccion(url)
    if response_estado == aemet_api.COD_RESPONSE_OK:
        playa = amodelo.JsonAModelo.json_a_playa(response_datos)
        datos = playa.to_dict
    else:
        datos = response_datos
    response = dict(estado=response_estado, datos=datos)
    return str(response)


if __name__ == '__main__':
    app.run(debug=True)
