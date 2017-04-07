import network.aemetapi as api
import network.jsonamodelo as amodelo

from flask import Flask

app = Flask(__name__)

aemet_api = api.AemetAPI()


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
            montaña = amodelo.JsonAModelo.json_a_montaña(response_datos,dia)
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
