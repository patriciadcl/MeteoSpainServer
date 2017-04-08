import network.aemetapi as api
import network.servidorutils as servidor
import os

from flask import Flask, request
from data.basedatos import connect

app = Flask(__name__)

aemet_api = api.AemetAPI()

base_dir = os.path.dirname(os.path.realpath('__file__'))

utils = servidor.ServidorUtils(base_dir)

meteospain_db = None


@app.route('/datos/areas_altamar')
@app.route('/datos/areas_costeras')
@app.route('/datos/areas_montaña')
@app.route('/datos/estado_cielo')
@app.route('/datos/estados_playa')
@app.route('/datos/cc_aa')
@app.route('/datos/municipios')
@app.route('/datos/playas')
@app.route('/datos/provincias_costas')
@app.route('/datos/provincias')
@app.route('/datos/subzonas_costas')
def datos():
    file = os.path.split(request.path)
    json_file = os.path.join(base_dir, "json", file[1] + ".json")
    response = utils.get_datos(json_file)
    return response


@app.route('/predicciones/altamar/<int:area>')
def altamar(area):
    if area not in aemet_api.AREAS_ALTAMAR:
        response = str(dict(estado=aemet_api.COD_RESPONSE_ERROR["incorrecta"][0],
                            datos=aemet_api.COD_RESPONSE_ERROR["incorrecta"][1]))
    else:
        response = utils.get_altamar(area)
    return response


@app.route('/predicciones/costa/<int:area>')
def costa(area):
    if area not in aemet_api.AREAS_COSTA:
        response = str(dict(estado=aemet_api.COD_RESPONSE_ERROR["incorrecta"][0],
                            datos=aemet_api.COD_RESPONSE_ERROR["incorrecta"][1]))
    else:
        response = utils.get_costa(area)
    return response


@app.route('/predicciones/montaña/<area>/dia/<int:dia>')
def montaña(area, dia):
    if dia not in aemet_api.DIAS_MONTAÑA:
        response = str(dict(estado=aemet_api.COD_RESPONSE_ERROR["incorrecta"][0],
                            datos=aemet_api.COD_RESPONSE_ERROR["incorrecta"][1]))
    else:
        response = utils.get_montaña(area,dia)
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
    connect()
    app.run(debug=True)
