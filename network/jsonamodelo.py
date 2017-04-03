import json
import modelo.altamar as altamar
import modelo.costas as costas
import modelo.montaña as montana
import modelo.municipio as municipio


class JsonAModelo:

    periodo_horas = ("00-24", "00-12", "12-24", "00-06", "06-12", "12-18", '18-24')
    periodo_horas_6 = {"6","12","18","24"}
    direccion_viento = {"N":"Norte", "NE":"Nordeste", "E":"Este", "SE":"Sudeste", "S":"Sur", "SO":"Suroeste",
                        "O":"Oeste", "NO": "Noroeste", "C": "Calma"}


    @staticmethod
    def girar_fecha(fecha):
        new_fecha = str(fecha).split("-")
        new_fecha.reverse()
        return new_fecha[0] + "-" + new_fecha[1] + "-" + new_fecha[2]

    @classmethod
    def json_a_altamar(self,cadena_json):
        try:
            js = json.loads(cadena_json)
        except:
            js = None
        f_elaboracion = self.girar_fecha(str(js[0]['origen']['elaborado']))
        situacion = js[0]["situacion"]
        json_subzonas = js[0]["prediccion"]["zona"]
        subzonas = list()
        for json_subzona in json_subzonas:
            subzona = altamar.SubZona(str(json_subzona['id']), json_subzona['texto'])
            subzonas.append(subzona)
        id_aemet = situacion['id']
        f_inicio = self.girar_fecha(situacion['inicio'])
        f_fin = self.girar_fecha(situacion['fin'])
        texto = str(situacion["texto"])
        zona = altamar.Zona(id_aemet, "", f_elaboracion, f_inicio, f_fin, texto, subzonas)
        return zona

    @classmethod
    def json_a_costas(self,cadena_json):
        try:
            js = json.loads(cadena_json)
        except:
            js = None
        f_elaboracion = self.girar_fecha(str(js[0]['origen']['elaborado']))
        f_inicio = self.girar_fecha(str(js[0]['origen']['inicio']))
        f_fin = self.girar_fecha(str(js[0]['origen']['fin']))
        situacion = js[0]["situacion"]
        id_aemet = situacion['id'][1:]
        situacion = situacion["texto"]
        aviso = js[0]["aviso"]["texto"]
        tendencia = js[0]["tendencia"]["texto"]
        json_subzonas = js[0]["prediccion"]["zona"]
        subzonas = list()
        for json_subzona in json_subzonas:
            subzona = costas.SubZona(str(json_subzona["subzona"]['id']), json_subzona["subzona"]['texto'])
            subzonas.append(subzona)
        zona = costas.Zona(id_aemet, "", f_elaboracion, f_inicio, f_fin, situacion, aviso, tendencia, subzonas)
        return zona


    @classmethod
    def json_a_montana(self, cadena_json):
        try:
            js = json.loads(cadena_json)
        except:
            js = None
        id_api = js[0]["id"]
        prediccion = js[0]["seccion"][0]["apartado"]
        estado_cielo = prediccion[0]["texto"]
        precipitaciones = prediccion[1]["texto"]
        tormentas = prediccion[2]["texto"]
        temperaturas = prediccion[3]["texto"]
        viento = prediccion[4]["texto"]
        lugares = list()
        if len(js[0]["seccion"]) == 3:
            json_lugares = js[0]["seccion"][2]["lugar"]
            for json_lugar in json_lugares:
                minima = str(json_lugar["minima"])
                st_minima = str(json_lugar["stminima"])
                maxima = str(json_lugar["maxima"])
                st_maxima = str(json_lugar["stmaxima"])
                nombre = json_lugar["nombre"]
                altitud = json_lugar["altitud"]
                lugar = montana.Lugar(minima, st_minima, maxima, st_maxima, nombre, altitud)
                lugares.append(lugar)
        zona = montana.Montana(id_api, "", estado_cielo, precipitaciones, tormentas, temperaturas, viento, lugares)

        return zona

    @classmethod
    def json_a_municipio(self, cadena_json,es_diaria):
        try:
            js = json.loads(cadena_json)
        except:
            js = None
        el_municipio = None
        id_aemet = js[0]["id"]
        f_elaboracion = self.girar_fecha(js[0]["elaborado"])
        prediccion = js[0]["prediccion"]
        if es_diaria:

            dias_json = prediccion[0]["dia"]
            dias = list()
            for dia_json in dias_json:
                uv_max = dia_json["uvMax"]
                f_validez = self.girar_fecha(dia_json["fecha"])
                prob_precipitacion = dict()
                cota_nieve = dict()
                estado_cielo = dict()
                viento = dict()
                racha_max = dict()
                for hora in self.periodo_horas:
                    prob_precipitacion[hora] = dia_json["probPrecipitacion"][hora]
                    cota_nieve[hora] = dia_json["cotaNieveProv"][hora]
                    estado_cielo[hora] = dia_json["estadoCielo"][hora]
                    viento[hora] = dia_json["viento"][hora]
                    racha_max[hora] = dia_json["rachaMax"][hora]
                temperatura = dict()
                temperatura["maxima"] = dia_json["temperatura"]["maxima"]
                temperatura["minima"] = dia_json["temperatura"]["minima"]
                posicion_dato = 0
                for valor in self.periodo_horas_6:
                    temperatura[valor] = dia_json["temperatura"]["dato"][posicion_dato]["value"]
                    posicion_dato = posicion_dato + 1
                sens_termica = dict()
                sens_termica["maxima"] = dia_json["sensTermica"]["maxima"]
                sens_termica["minima"] = dia_json["sensTermica"]["minima"]
                posicion_dato = 0
                for valor in self.periodo_horas_6:
                    sens_termica[valor] = dia_json["humedadRelativa"]["dato"][posicion_dato]["value"]
                    posicion_dato = posicion_dato + 1
                humedad = dict()
                humedad["maxima"] = dia_json["humedadRelativa"]["maxima"]
                humedad["minima"] = dia_json["humedadRelativa"]["minima"]
                posicion_dato = 0
                for valor in self.periodo_horas_6:
                    humedad[valor] = dia_json["humedadRelativa"]["dato"][posicion_dato]["value"]
                    posicion_dato = posicion_dato + 1

                dia = municipio.PredicionDia(f_validez, prob_precipitacion, cota_nieve, estado_cielo, viento, racha_max,
                                             temperatura,sens_termica, humedad, uv_max)

                dias.append(dia)
            el_municipio = municipio.Municipio(id_aemet, f_elaboracion, dias)
        else:
            pass


        return el_municipio