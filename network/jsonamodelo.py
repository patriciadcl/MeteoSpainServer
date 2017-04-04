import json
import modelo.altamar as altamar
import modelo.costas as costas
import modelo.montaña as montana
import modelo.municipio as municipio


class JsonAModelo:
    periodo_horas = ("00-24", "00-12", "12-24", "00-06", "06-12", "12-18", '18-24')
    periodo_horas_6 = ("6", "12", "18", "24")
    periodo_horas_12 = ("00-24", "00-12", "12-24")
    direccion_viento = {"N": "Norte", "NE": "Nordeste", "E": "Este", "SE": "Sudeste", "S": "Sur", "SO": "Suroeste",
                        "O": "Oeste", "NO": "Noroeste", "C": "Calma"}

    @staticmethod
    def girar_fecha(fecha):
        new_fecha = str(fecha).split("-")
        new_fecha.reverse()
        return new_fecha[0] + "-" + new_fecha[1] + "-" + new_fecha[2]

    @classmethod
    def json_a_altamar(self, cadena_json):
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
    def json_a_costas(cls, cadena_json):
        try:
            js = json.loads(cadena_json)
        except:
            js = None
        f_elaboracion = cls.girar_fecha(str(js[0]['origen']['elaborado']))
        f_inicio = cls.girar_fecha(str(js[0]['origen']['inicio']))
        f_fin = cls.girar_fecha(str(js[0]['origen']['fin']))
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
    def json_a_montana(cls, cadena_json):
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
    def json_a_municipio(cls, cadena_json, es_diaria):
        try:
            js = json.loads(cadena_json)
        except:
            js = None
        el_municipio = None
        id_aemet = js[0]["id"]
        f_elaboracion = cls.girar_fecha(js[0]["elaborado"])
        prediccion = js[0]["prediccion"]
        if es_diaria:
            dias_json = prediccion["dia"]
            dias = list()
            for num_dia in range(2):
                print("Dia: ",num_dia)
                uv_max = dias_json[num_dia]["uvMax"]
                f_validez = cls.girar_fecha(dias_json[num_dia]["fecha"])
                prob_precipitacion = dict()
                cota_nieve = dict()
                estado_cielo = dict()
                viento = dict()
                racha_max = dict()
                for hora in cls.periodo_horas:
                    index = cls.periodo_horas.index(hora)
                    print("index",index)
                    prob_precipitacion[hora] = dias_json[num_dia]["probPrecipitacion"][index]["value"]
                    cota_nieve[hora] = dias_json[num_dia]["cotaNieveProv"][index]["value"]
                    estado_cielo[hora] = dias_json[num_dia]["estadoCielo"][index]["value"]
                    viento[hora] = {'velocidad':dias_json[num_dia]["viento"][index]["velocidad"],
                                        'dir':dias_json[num_dia]["viento"][index]["direccion"]}
                    racha_max[hora] = dias_json[num_dia]["rachaMax"][index]["value"]
                temperatura = dict()
                sens_termica = dict()
                humedad = dict()
                temperatura["maxima"] = dias_json[num_dia]["temperatura"]["maxima"]
                temperatura["minima"] = dias_json[num_dia]["temperatura"]["minima"]
                sens_termica["maxima"] = dias_json[num_dia]["sensTermica"]["maxima"]
                sens_termica["minima"] = dias_json[num_dia]["sensTermica"]["minima"]
                humedad["maxima"] = dias_json[num_dia]["humedadRelativa"]["maxima"]
                humedad["minima"] = dias_json[num_dia]["humedadRelativa"]["minima"]
                for valor in cls.periodo_horas_6:
                    index = cls.periodo_horas_6.index(valor)
                    temperatura[valor] = dias_json[num_dia]["temperatura"]["dato"][index]["value"]
                    sens_termica[valor] = dias_json[num_dia]["sensTermica"]["dato"][index]["value"]
                    humedad[valor] = dias_json[num_dia]["humedadRelativa"]["dato"][index]["value"]
                dia = municipio.PredicionDia(f_validez, prob_precipitacion, cota_nieve, estado_cielo, viento, racha_max,
                                             temperatura, sens_termica, humedad, uv_max)

                dias.append(dia)
            for num_dia in range(2,4):
                print("Dia: ",num_dia)
                uv_max = dias_json[num_dia]["uvMax"]
                f_validez = cls.girar_fecha(dias_json[num_dia]["fecha"])
                prob_precipitacion = dict()
                cota_nieve = dict()
                estado_cielo = dict()
                viento = dict()
                racha_max = dict()
                for hora in cls.periodo_horas_12:
                    index = cls.periodo_horas_12.index(hora)
                    print("index",index)
                    prob_precipitacion[hora] = dias_json[num_dia]["probPrecipitacion"][index]["value"]
                    cota_nieve[hora] = dias_json[num_dia]["cotaNieveProv"][index]["value"]
                    estado_cielo[hora] = dias_json[num_dia]["estadoCielo"][index]["value"]
                    viento[hora] = {'velocidad':dias_json[num_dia]["viento"][index]["velocidad"],
                                        'dir':dias_json[num_dia]["viento"][index]["direccion"]}
                    racha_max[hora] = dias_json[num_dia]["rachaMax"][index]["value"]
                temperatura = dict()
                sens_termica = dict()
                humedad = dict()
                temperatura["maxima"] = dias_json[num_dia]["temperatura"]["maxima"]
                temperatura["minima"] = dias_json[num_dia]["temperatura"]["minima"]
                sens_termica["maxima"] = dias_json[num_dia]["sensTermica"]["maxima"]
                sens_termica["minima"] = dias_json[num_dia]["sensTermica"]["minima"]
                humedad["maxima"] = dias_json[num_dia]["humedadRelativa"]["maxima"]
                humedad["minima"] = dias_json[num_dia]["humedadRelativa"]["minima"]
                dia = municipio.PredicionDia(f_validez, prob_precipitacion, cota_nieve, estado_cielo, viento, racha_max,
                                             temperatura, sens_termica, humedad, uv_max)

                dias.append(dia)
            for num_dia in range(4, len(dias_json)):
                print("Dia: ", num_dia)
                uv_max = ""
                if "uvMax" in dias_json[num_dia]:
                    uv_max = dias_json[num_dia]["uvMax"]
                f_validez = cls.girar_fecha(dias_json[num_dia]["fecha"])
                prob_precipitacion = dict()
                cota_nieve = dict()
                estado_cielo = dict()
                viento = dict()
                racha_max = dict()
                index = 0
                print("index", index)
                prob_precipitacion[hora] = dias_json[num_dia]["probPrecipitacion"][index]["value"]
                cota_nieve[hora] = dias_json[num_dia]["cotaNieveProv"][index]["value"]
                estado_cielo[hora] = dias_json[num_dia]["estadoCielo"][index]["value"]
                viento[hora] = {'velocidad': dias_json[num_dia]["viento"][index]["velocidad"],
                                    'dir': dias_json[num_dia]["viento"][index]["direccion"]}
                racha_max[hora] = dias_json[num_dia]["rachaMax"][index]["value"]
                temperatura = dict()
                sens_termica = dict()
                humedad = dict()
                temperatura["maxima"] = dias_json[num_dia]["temperatura"]["maxima"]
                temperatura["minima"] = dias_json[num_dia]["temperatura"]["minima"]
                sens_termica["maxima"] = dias_json[num_dia]["sensTermica"]["maxima"]
                sens_termica["minima"] = dias_json[num_dia]["sensTermica"]["minima"]
                humedad["maxima"] = dias_json[num_dia]["humedadRelativa"]["maxima"]
                humedad["minima"] = dias_json[num_dia]["humedadRelativa"]["minima"]
                dia = municipio.PredicionDia(f_validez, prob_precipitacion, cota_nieve, estado_cielo, viento, racha_max,
                                             temperatura, sens_termica, humedad, uv_max)

                dias.append(dia)
            el_municipio = municipio.Municipio(id_aemet, f_elaboracion, dias)
        else:
            pass

        return el_municipio
