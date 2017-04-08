import network.aemetapi as api
import network.jsonamodelo as amodelo
import json


class ServidorUtils:
    
    base_dir = None
    aemet_api = None
        
    @classmethod
    def __init__(cls,  base_dir):
        cls.base_dir = base_dir
        cls.aemet_api = api.AemetAPI()

    @classmethod
    def get_datos(cls, json_file):
        try:
            f_open = open(json_file, "r", encoding='utf-8')
            contenido = f_open.read()
            js = json.loads(contenido)
            response = dict(estado=cls.aemet_api.COD_RESPONSE_OK, datos=js)
            return str(response)
        except Exception as ex:
            response = dict(estado=cls.aemet_api.COD_RESPONSE_ERROR["incorrecta"][0],
                            datos=format(ex))
            return str(response)

    @classmethod
    def get_altamar(cls, area):
        # TODO: Comprobar si esta en la base de datos
        url = cls.aemet_api.url_altamar(str(area))
        response_estado, response_datos = cls.aemet_api.get_prediccion(url)
        if response_estado == cls.aemet_api.COD_RESPONSE_OK:
            altamar = amodelo.JsonAModelo.json_a_altamar(response_datos)
            datos = altamar.to_dict
        else:
            datos = response_datos
        response = dict(estado=response_estado, datos=datos)
        return str(response)

    @classmethod
    def get_costa(cls, area):
        # TODO: Comprobar si esta en la base de datos
        url = cls.aemet_api.url_costa(str(area))
        response_estado, response_datos = cls.aemet_api.get_prediccion(url)
        if response_estado == cls.aemet_api.COD_RESPONSE_OK:
            costa = amodelo.JsonAModelo.json_a_costas(response_datos)
            datos = costa.to_dict
        else:
            datos = response_datos
        response = dict(estado=response_estado, datos=datos)
        return str(response)

    @classmethod
    def get_montaña(cls, area, dia):
        # TODO: Comprobar si esta en la base de datos
        url = cls.aemet_api.url_montaña(area, str(dia))
        response_estado, response_datos = cls.aemet_api.get_prediccion(url)
        if response_estado == cls.aemet_api.COD_RESPONSE_OK:
            montaña = amodelo.JsonAModelo.json_a_montaña(response_datos, dia)
            datos = montaña.to_dict
        else:
            datos = response_datos
        response = dict(estado=response_estado, datos=datos)
        return str(response)

    @classmethod
    def get_municipo_diaria(cls, id_municipio):
        # TODO: Comprobar si esta en la base de datos
        url = cls.aemet_api.url_municipio_dia(str(id_municipio))
        response_estado, response_datos = cls.aemet_api.get_prediccion(url)
        if response_estado == cls.aemet_api.COD_RESPONSE_OK:
            municipio = amodelo.JsonAModelo.json_a_municipio(response_datos, True)
            datos = municipio.to_dict
        else:
            datos = response_datos
        response = dict(estado=response_estado, datos=datos)
        return str(response)

    @classmethod
    def get_municipo_horaria(cls, id_municipio):
        # TODO: Comprobar si esta en la base de datos
        url = cls.aemet_api.url_municipio_horas(str(id_municipio))
        response_estado, response_datos = cls.aemet_api.get_prediccion(url)
        if response_estado == cls.aemet_api.COD_RESPONSE_OK:
            municipio = amodelo.JsonAModelo.json_a_municipio(response_datos, False)
            datos = municipio.to_dict
        else:
            datos = response_datos
        response = dict(estado=response_estado, datos=datos)
        return str(response)

    @classmethod
    def get_playa(cls, id_playa):
        # TODO: Comprobar si esta en la base de datos
        url = cls.aemet_api.url_playa(str(id_playa).zfill(7))
        response_estado, response_datos = cls.aemet_api.get_prediccion(url)
        if response_estado == cls.aemet_api.COD_RESPONSE_OK:
            playa = amodelo.JsonAModelo.json_a_playa(response_datos)
            datos = playa.to_dict
        else:
            datos = response_datos
        response = dict(estado=response_estado, datos=datos)
        return str(response)