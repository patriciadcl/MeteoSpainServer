import json
import modelo.altamar as altamar
import modelo.costas as costas
import modelo.montaña as montana


class JsonAModelo:

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
    def json_a_montana(self, cadena_json, f_pronostico):
        try:
            js = json.loads(cadena_json)
        except:
            js = None
        id_api = js[0]["id"]
        prediccion = js[0]["seccion"][0]["apartado"]
        estado_cielo = prediccion[0]["texto"]
        tormentas = prediccion[1]["texto"]
        temperaturas = prediccion[2]["texto"]
        viento = prediccion[3]["texto"]
        precipitaciones = prediccion[4]["texto"]
        json_lugares = js[0]["seccion"][2]["lugar"]
        if len(json_lugares) > 0:
            lugares = list()
            for json_lugar in json_lugares:
                minima = str(json_lugar["minima"])
                st_minima = str(json_lugar["stminima"])
                maxima = str(json_lugar["maxima"])
                st_maxima = str(json_lugar["stmaxima"])
                nombre = json_lugar["nombre"]
                altitud = json_lugar["altitud"]
                lugar = montana.Lugar( minima, st_minima, maxima, st_maxima, nombre, altitud)
                lugares.append(lugar)
        zona = montana.Montana(id_api, self.girar_fecha(f_pronostico), estado_cielo, precipitaciones, tormentas, temperaturas, viento, lugares)

        return zona
