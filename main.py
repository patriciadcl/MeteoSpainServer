# import bottle
# from bottle import run
# import predicciones
#
# if __name__ == '__main__':
#     run(host='localhost', port=8080)
#
# app = application = bottle.default_app()
import network.aemetapi as api
import requests
from flask import Flask

app = Flask(__name__)


@app.route('/predicciones/altamar/<area>', methods=['GET'])
def get_altamar(area):

    url = api.AemetAPI.url_altamar(area)
    querystring = {
        "api_key": api.AemetAPI.DATOS_AEMET["AEMET_API_KEY"]}

    headers = {
        'cache-control': "no-cache"
    }

    aemet_response = requests.request("GET", url, headers=headers, params=querystring)

    return "Altamar " + aemet_response.text


@app.route('/predicciones/costa/<area>', methods=['GET'])
def get_costa(area):
    return "Costa " + area


@app.route('/predicciones/montaña/<playa>/dia/<dia>', methods=['GET'])
def get_montaña(area, dia):
    return "Montaña " + area + "Dia " + dia


@app.route('/predicciones/municipio/diaria/<municipio>', methods=['GET'])
def get_municipo_diaria(municipio):
    return "Municipio " + municipio


@app.route('/predicciones/municipio/horaria/<municipio>', methods=['GET'])
def get_municipo_horaria(municipio):
    return "Municipio " + municipio


@app.route('/predicciones/playa/<playa>', methods=['GET'])
def get_playa(playa):
    return "Playa " + playa

if __name__ == '__main__':
    app.run(debug=True)