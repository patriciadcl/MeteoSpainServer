import network.aemetapi as api
import json
from network.jsonamodelo import JsonAModelo
from datetime import date, timedelta


class ServidorUtils:
    base_dir = None
    aemet_api = None
    meteo_ddbb = None

    @classmethod
    def __init__(cls, base_dir, dd_bb):
        cls.base_dir = base_dir
        cls.aemet_api = api.AemetAPI()
        cls.meteo_ddbb = dd_bb

    @classmethod
    def get_datos(cls, json_file):
        response = None
        try:
            with open(json_file, "r", encoding='utf-8') as f_open:
                contenido = f_open.read()
                js = json.loads(contenido)
                response = dict(estado=cls.aemet_api.COD_RESPONSE_OK, datos=js)
        except Exception as ex:
            response = cls.aemet_api.get_response_error(cls.aemet_api.COD_PET_INCORRECTA,
                                                        datos=format(ex))
        finally:
            return str(response)

    @classmethod
    def get_altamar(cls, area):
        # comprobamos si la tenemos en la base de datos
        hoy = cls.rotar_fecha(date.today())
        en_ddbb, response_ddbb = cls.meteo_ddbb.get_altamar(area, hoy, hoy)
        if en_ddbb:
            response_estado = cls.aemet_api.COD_RESPONSE_OK
            datos = response_ddbb
        else:
            url = cls.aemet_api.url_altamar(str(area))
            response_estado, response_datos = cls.aemet_api.get_prediccion(url)
            if response_estado == cls.aemet_api.COD_RESPONSE_OK:
                altamar = JsonAModelo.json_a_altamar(area, response_datos)
                datos = altamar.to_dict
                print("Insertado ", cls.meteo_ddbb.insert_altamar(area, altamar.f_elaboracion, altamar.f_inicio,
                                                                  json.dumps(datos)))
            else:
                datos = cls.aemet_api.e
        response = dict(estado=response_estado, datos=datos)
        return str(response)

    @classmethod
    def get_costa(cls, area):
        # comprobamos si la tenemos en la base de datos
        hoy = cls.rotar_fecha(date.today())
        en_ddbb, response_ddbb = cls.meteo_ddbb.get_costa(area, hoy, hoy)
        if en_ddbb:
            response_estado = cls.aemet_api.COD_RESPONSE_OK
            datos = response_ddbb
        else:
            url = cls.aemet_api.url_costa(str(area))
            response_estado, response_datos = cls.aemet_api.get_prediccion(url)
            if response_estado == cls.aemet_api.COD_RESPONSE_OK:
                costa = JsonAModelo.json_a_costa(area, response_datos)
                datos = costa.to_dict
                print("Insertado ", cls.meteo_ddbb.insert_costa(area, costa.f_elaboracion, costa.f_inicio,
                                                                  json.dumps(datos)))
            else:
                datos = response_datos
        response = dict(estado=response_estado, datos=datos)
        return str(response)

    @classmethod
    def get_montaña(cls, area, dia):
        # comprobamos si la tenemos en la base de datos
        hoy = cls.rotar_fecha(date.today())
        f_pronostico = date.today() + timedelta(days=dia)
        f_pronostico = cls.rotar_fecha(str(f_pronostico))
        en_ddbb, response_ddbb = cls.meteo_ddbb.get_montaña(area, hoy, f_pronostico)
        if en_ddbb:
            response_estado = cls.aemet_api.COD_RESPONSE_OK
            datos = response_ddbb
        else:
            url = cls.aemet_api.url_montaña(area, str(dia))
            response_estado, response_datos = cls.aemet_api.get_prediccion(url)
            if response_estado == cls.aemet_api.COD_RESPONSE_OK:
                montaña = JsonAModelo.json_a_montaña(response_datos, dia)
                datos = montaña.to_dict
                print("Insertado ", cls.meteo_ddbb.insert_montaña(area, montaña.f_elaboracion,
                                                                  montaña.f_pronostico, json.dumps(datos)))
            else:
                datos = response_datos
        response = dict(estado=response_estado, datos=datos)
        return str(response)

    @classmethod
    def get_municipo_diaria(cls, id_municipio):
        # comprobamos si la tenemos en la base de datos
        hoy = cls.rotar_fecha(date.today())
        en_ddbb, response_ddbb = cls.meteo_ddbb.get_muni_diaria(id_municipio, hoy)
        if en_ddbb:
            response_estado = cls.aemet_api.COD_RESPONSE_OK
            datos = response_ddbb
        else:
            url = cls.aemet_api.url_municipio_dia(str(id_municipio))
            response_estado, response_datos = cls.aemet_api.get_prediccion(url)
            if response_estado == cls.aemet_api.COD_RESPONSE_OK:
                municipio = JsonAModelo.json_a_municipio(response_datos, True)
                datos = municipio.to_dict
                print("Insertado ", cls.meteo_ddbb.ins_muni_diaria(id_municipio, municipio.f_elaboracion,
                                                                  hoy, json.dumps(datos)))
            else:
                datos = response_datos
        response = dict(estado=response_estado, datos=datos)
        return str(response)

    @classmethod
    def get_municipo_horaria(cls, id_municipio):
        # comprobamos si la tenemos en la base de datos
        hoy = cls.rotar_fecha(date.today())
        en_ddbb, response_ddbb = cls.meteo_ddbb.get_muni_horaria(id_municipio, hoy)
        if en_ddbb:
            response_estado = cls.aemet_api.COD_RESPONSE_OK
            datos = response_ddbb
        else:
            url = cls.aemet_api.url_municipio_horas(str(id_municipio))
            response_estado, response_datos = cls.aemet_api.get_prediccion(url)
            if response_estado == cls.aemet_api.COD_RESPONSE_OK:
                municipio = JsonAModelo.json_a_municipio(response_datos, False)
                datos = municipio.to_dict
                print("Insertado ", cls.meteo_ddbb.ins_muni_horaria(id_municipio, municipio.f_elaboracion,
                                                                   hoy, json.dumps(datos)))
            else:
                datos = response_datos
        response = dict(estado=response_estado, datos=datos)
        return str(response)

    @classmethod
    def get_playa(cls, id_playa):
        # comprobamos si la tenemos en la base de datos
        hoy = cls.rotar_fecha(date.today())
        en_ddbb, response_ddbb = cls.meteo_ddbb.get_playa(id_playa, hoy, hoy)
        if en_ddbb:
            response_estado = cls.aemet_api.COD_RESPONSE_OK
            datos = response_ddbb
        else:
            url = cls.aemet_api.url_playa(str(id_playa).zfill(7))
            response_estado, response_datos = cls.aemet_api.get_prediccion(url)
            if response_estado == cls.aemet_api.COD_RESPONSE_OK:
                playa = JsonAModelo.json_a_playa(response_datos)
                datos = playa.to_dict
                print("Insertado ", cls.meteo_ddbb.insert_playa(id_playa, playa.f_elaboracion,
                                                                    hoy, json.dumps(datos)))
            else:
                datos = response_datos
        response = dict(estado=response_estado, datos=datos)
        return str(response)

    @staticmethod
    def rotar_fecha(fecha):
        new_fecha = str(fecha).split("-")
        new_fecha.reverse()
        return new_fecha[0] + "-" + new_fecha[1] + "-" + new_fecha[2]
