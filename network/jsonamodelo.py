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
    def get_campos_pcev(cls,dia_json,periodo):
        prob_precipitacion = dict()
        cota_nieve = dict()
        estado_cielo = dict()
        viento = dict()
        racha_max = dict()
        for hora in periodo:
            index = periodo.index(hora)
            prob_precipitacion[hora] = dia_json["probPrecipitacion"][index]["value"]
            cota_nieve[hora] = dia_json["cotaNieveProv"][index]["value"]
            estado_cielo[hora] = dia_json["estadoCielo"][index]["value"]
            viento[hora] = {'velocidad': dia_json["viento"][index]["velocidad"],
                            'dir': dia_json["viento"][index]["direccion"]}
            racha_max[hora] = dia_json["rachaMax"][index]["value"]
        return prob_precipitacion,cota_nieve,estado_cielo,viento,racha_max

    @classmethod
    def get_maxmin_temp(cls, dia_json):
        temp_max = dia_json["temperatura"]["maxima"]
        temp_min = dia_json["temperatura"]["minima"]
        return temp_max, temp_min

    @classmethod
    def get_maxmin_sensa(cls, dia_json):
        sens_ter_max = dia_json["sensTermica"]["maxima"]
        sens_ter_min = dia_json["sensTermica"]["minima"]
        return sens_ter_max, sens_ter_min

    @classmethod
    def get_maxmin_hum(cls, dia_json):
        h_max = dia_json["humedadRelativa"]["maxima"]
        h_minima = dia_json["humedadRelativa"]["minima"]
        return h_max, h_minima

    @classmethod
    def get_campos_tsh(cls,dia_json,periodo):
        temperatura = dict()
        sens_termica = dict()
        humedad = dict()
        temperatura["maxima"],temperatura["minima"] = cls.get_maxmin_temp(dia_json)
        sens_termica["maxima"],sens_termica["minima"] = cls.get_maxmin_sensa(dia_json)
        humedad["maxima"],humedad["minima"] = cls.get_maxmin_hum(dia_json)
        for valor in periodo:
            index = periodo.index(valor)
            temperatura[valor] = dia_json["temperatura"]["dato"][index]["value"]
            sens_termica[valor] = dia_json["sensTermica"]["dato"][index]["value"]
            humedad[valor] = dia_json["humedadRelativa"]["dato"][index]["value"]

        return temperatura,sens_termica,humedad



    @classmethod
    def json_a_municipio(cls, cadena_json, es_diaria):
        try:
            js = json.loads(cadena_json)
        except:
            js = None
        id_aemet = js[0]["id"]
        f_elaboracion = cls.girar_fecha(js[0]["elaborado"])
        prediccion = js[0]["prediccion"]
        if "dia" in prediccion:
            dias_json = prediccion["dia"]
            dias = list()
            if es_diaria:
                for num_dia in range(2):
                    uv_max = dias_json[num_dia]["uvMax"]
                    f_validez = cls.girar_fecha(dias_json[num_dia]["fecha"])
                    prob_precipitacion, cota_nieve, estado_cielo, viento, racha_max = cls.get_campos_pcev(dias_json[num_dia],cls.periodo_horas)
                    temperatura,sens_termica,humedad = cls.get_campos_tsh(dias_json[num_dia],cls.periodo_horas_6)
                    dia = municipio.PredicionDia(f_validez, prob_precipitacion, cota_nieve, estado_cielo, viento, racha_max,
                                                 temperatura, sens_termica, humedad, uv_max)
                    dias.append(dia)
                for num_dia in range(2,4):
                    uv_max = dias_json[num_dia]["uvMax"]
                    f_validez = cls.girar_fecha(dias_json[num_dia]["fecha"])
                    prob_precipitacion, cota_nieve, estado_cielo, viento, racha_max = cls.get_campos_pcev(
                        dias_json[num_dia], cls.periodo_horas_12)
                    temperatura = dict()
                    sens_termica = dict()
                    humedad = dict()
                    temperatura["maxima"], temperatura["minima"] = cls.get_maxmin_temp(dias_json[num_dia])
                    sens_termica["maxima"], sens_termica["minima"] = cls.get_maxmin_sensa(dias_json[num_dia])
                    humedad["maxima"], humedad["minima"] = cls.get_maxmin_hum(dias_json[num_dia])
                    dia = municipio.PredicionDia(f_validez, prob_precipitacion, cota_nieve, estado_cielo, viento, racha_max,
                                                 temperatura, sens_termica, humedad, uv_max)

                    dias.append(dia)
                for num_dia in range(4, len(dias_json)):
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
                    hora = "00-24"
                    prob_precipitacion[hora] = dias_json[num_dia]["probPrecipitacion"][index]["value"]
                    cota_nieve[hora] = dias_json[num_dia]["cotaNieveProv"][index]["value"]
                    estado_cielo[hora] = dias_json[num_dia]["estadoCielo"][index]["value"]
                    viento[hora] = {'velocidad': dias_json[num_dia]["viento"][index]["velocidad"],
                                        'dir': dias_json[num_dia]["viento"][index]["direccion"]}
                    racha_max[hora] = dias_json[num_dia]["rachaMax"][index]["value"]
                    temperatura = dict()
                    sens_termica = dict()
                    humedad = dict()
                    temperatura["maxima"], temperatura["minima"] = cls.get_maxmin_temp(dias_json[num_dia])
                    sens_termica["maxima"], sens_termica["minima"] = cls.get_maxmin_sensa(dias_json[num_dia])
                    humedad["maxima"], humedad["minima"] = cls.get_maxmin_hum(dias_json[num_dia])
                    dia = municipio.PredicionDia(f_validez, prob_precipitacion, cota_nieve, estado_cielo, viento, racha_max,
                                                 temperatura, sens_termica, humedad, uv_max)
                    dias.append(dia)

            else:
                for num_dia in range(len(dias_json)):
                    f_validez = cls.girar_fecha(dias_json[num_dia]["fecha"])
                    orto = dias_json[num_dia]["orto"]
                    ocaso = dias_json[num_dia]["ocaso"]
                    precipitacion = dict()
                    nieve = dict()
                    estado_cielo = dict()
                    temperatura = dict()
                    sens_termica = dict()
                    humedad_relativa = dict()
                    prob_tormenta = dict()
                    prob_nieve = dict()
                    prob_precipitacion = dict()
                    viento = dict()
                    racha_max = dict()

                    # Estos campos tienen 10 valores
                    for contador in range(len(dias_json[num_dia]["estadoCielo"])):
                        periodo = dias_json[num_dia]["estadoCielo"][contador]["periodo"] + ":00"
                        estado_cielo[periodo] = dias_json[num_dia]["estadoCielo"][contador]["value"]
                        precipitacion[periodo] = dias_json[num_dia]["precipitacion"][contador]["value"]
                        nieve[periodo] = dias_json[num_dia]["nieve"][contador]["value"]
                        temperatura[periodo] = dias_json[num_dia]["temperatura"][contador]["value"]
                        sens_termica[periodo] = dias_json[num_dia]["sensTermica"][contador]["value"]
                        humedad_relativa[periodo] = dias_json[num_dia]["humedadRelativa"][contador]["value"]
                    # Estos campos tienen 4 valores
                    for contador in range(len(dias_json[num_dia]["probPrecipitacion"])):
                        periodo = dias_json[num_dia]["probPrecipitacion"][contador]["periodo"]
                        periodo = periodo[:2] + ":00-" + periodo[2:] + ":00"
                        prob_precipitacion[periodo] = dias_json[num_dia]["probPrecipitacion"][contador]["value"]
                        prob_nieve[periodo] = dias_json[num_dia]["probNieve"][contador]["value"]
                        prob_tormenta[periodo] = dias_json[num_dia]["probTormenta"][contador]["value"]

                    # viento y racha max es un caso especial ya que viene juntos en un array de 20 valores


                    size = int(len(dias_json[num_dia]["vientoAndRachaMax"]))
                    for contador in [i for i in range(size) if i%2 == 0]:
                        periodo = dias_json[num_dia]["vientoAndRachaMax"][contador]["periodo"]+ ":00"
                        viento_json = dias_json[num_dia]["vientoAndRachaMax"][contador]
                        print(contador)
                        viento[periodo] ={'velocidad': viento_json['velocidad'][0],
                         'dir': viento_json["direccion"][0]}
                        racha_json = dias_json[num_dia]["vientoAndRachaMax"][contador + 1]
                        racha_max[periodo] = racha_json["value"]

                    dia = municipio.PrediccionHoras(f_validez, orto, ocaso, estado_cielo, precipitacion, prob_precipitacion, prob_tormenta, nieve,
                    prob_nieve, viento, racha_max, temperatura, sens_termica, humedad_relativa)
                    dias.append(dia)

        return municipio.Municipio(id_aemet, f_elaboracion, dias)