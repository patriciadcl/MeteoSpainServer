# -*- coding: utf-8 -*-
import json

from datetime import date, timedelta

from modelo import *

from network.utils import format_fecha


class JsonAModelo:

    PERIODO_HORAS = ["00-24", "00-12", "12-24", "00-06", "06-12", "12-18", '18-24']
    PERIODO_HORAS_6 = ["6", "12", "18", "24"]
    PERIODO_HORAS_6_CONVERSION = ["00-06", "06-12", "12-18", "18-24"]
    PERIODO_HORAS_12 = ["00-24", "00-12", "12-24"]

    @classmethod
    def json_a_altamar(cls, area, cadena_json):
        pred_altamar = None
        try:
            js = json.loads(cadena_json)
            f_elaboracion = format_fecha(str(js[0]['origen']['elaborado']))
            situacion = js[0]["situacion"]
            json_zonas = js[0]["prediccion"]["zona"]
            zonas = list()
            for json_zona in json_zonas:
                zona = altamar.Zona(str(json_zona['id']), json_zona['texto'])
                zonas.append(zona)
            id_aemet = situacion['id']
            f_inicio = format_fecha(situacion['inicio'])
            f_fin = format_fecha(situacion['fin'])
            texto = str(situacion["texto"])
            pred_altamar = altamar.Altamar(str(id_aemet), str(area), f_elaboracion, f_inicio, f_fin, texto, zonas)
        except Exception as exc:
            print("Exception ", format(exc))
        finally:
            return pred_altamar

    @classmethod
    def json_a_costa(cls, area, cadena_json):
        pred_costa = None
        try:
            js = json.loads(cadena_json)
            origen = js[0]['origen']
            f_elaboracion = format_fecha(str(origen['elaborado']))
            f_inicio = format_fecha(str(origen['inicio']))
            f_fin = format_fecha(str(origen['fin']))
            situacion = js[0]["situacion"]
            id_aemet = situacion['id'][1:]
            situacion = situacion["texto"]
            aviso = js[0]["aviso"]["texto"]
            tendencia = js[0]["tendencia"]["texto"]
            json_zonas = js[0]["prediccion"]["zona"]
            zonas = list()
            for json_zona in json_zonas:
                zona = costa.Zona(str(json_zona["subzona"]['id']), json_zona["subzona"]['texto'])
                zonas.append(zona)
            pred_costa = costa.Costa(str(id_aemet), str(area), f_elaboracion, f_inicio, f_fin, situacion,
                                     aviso, tendencia, zonas)
        except Exception as exc:
            print("Exception ", format(exc))
        return pred_costa

    @classmethod
    def json_a_montaña(cls, cadena_json, a_dia):
        pred_montaña = None
        try:
            js = json.loads(cadena_json)
            id_api = js[0]["id"]
            prediccion = js[0]["seccion"][0]["apartado"]
            estado_cielo = prediccion[0]["texto"]
            precipitaciones = prediccion[1]["texto"]
            tormentas = prediccion[2]["texto"]
            temperaturas = prediccion[3]["texto"]
            viento = prediccion[4]["texto"]
            zonas = list()
            if len(js[0]["seccion"]) == 3:
                json_lugares = js[0]["seccion"][2]["lugar"]
                for json_lugar in json_lugares:
                    minima = str(json_lugar["minima"])
                    st_minima = str(json_lugar["stminima"])
                    maxima = str(json_lugar["maxima"])
                    st_maxima = str(json_lugar["stmaxima"])
                    nombre = json_lugar["nombre"]
                    altitud = json_lugar["altitud"]
                    zona = montaña.Zona(minima, st_minima, maxima, st_maxima, nombre, altitud)
                    zonas.append(zona)
            dia = date.today()
            f_pronostico = dia + timedelta(days=a_dia)
            dia = format_fecha(str(dia))
            f_pronostico = format_fecha(f_pronostico)
            pred_montaña = montaña.Montaña(str(id_api), dia, f_pronostico, estado_cielo, precipitaciones, tormentas,
                                           temperaturas, viento, zonas)
        except Exception as exc:
            print("Exception ", format(exc))
        finally:
            return pred_montaña

    @classmethod
    def get_campos_pcev(cls, dia_json, periodo):
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
        return prob_precipitacion, cota_nieve, estado_cielo, viento, racha_max

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
    def get_campos_tsh(cls, dia_json):
        temperatura = dict()
        sens_termica = dict()
        humedad = dict()
        temperatura["maxima"], temperatura["minima"] = cls.get_maxmin_temp(dia_json)
        sens_termica["maxima"], sens_termica["minima"] = cls.get_maxmin_sensa(dia_json)
        humedad["maxima"], humedad["minima"] = cls.get_maxmin_hum(dia_json)
        periodo = cls.PERIODO_HORAS_6
        for valor in periodo:
            index = periodo.index(valor)
            valor_convertido = cls.PERIODO_HORAS_6_CONVERSION[index]
            temperatura[valor_convertido] = dia_json["temperatura"]["dato"][index]["value"]
            sens_termica[valor_convertido] = dia_json["sensTermica"]["dato"][index]["value"]
            humedad[valor_convertido] = dia_json["humedadRelativa"]["dato"][index]["value"]

        return temperatura, sens_termica, humedad

    @classmethod
    def json_a_municipio(cls, cadena_json, es_diaria):
        pred_municipio = None
        try:
            js = json.loads(cadena_json)
            id_aemet = str(js[0]["id"]).zfill(5)
            f_elaboracion = format_fecha(js[0]["elaborado"])
            prediccion = js[0]["prediccion"]
            prediccion_diaria = list()
            prediccion_horaria = list()
            if "dia" in prediccion:
                dias_json = prediccion["dia"]
                if es_diaria:
                    for num_dia in range(2):
                        uv_max = dias_json[num_dia]["uvMax"]
                        f_pronostico = format_fecha(dias_json[num_dia]["fecha"])
                        prob_precipitacion, cota_nieve, estado_cielo, viento, racha_max = cls.get_campos_pcev(
                            dias_json[num_dia], cls.PERIODO_HORAS)
                        temperatura, sens_termica, humedad = cls.get_campos_tsh(dias_json[num_dia])
                        dia = municipio.PredicionDia(f_pronostico, prob_precipitacion, cota_nieve, estado_cielo, viento,
                                                     racha_max, temperatura, sens_termica, humedad, uv_max)
                        prediccion_diaria.append(dia)
                    for num_dia in range(2, 4):
                        uv_max = dias_json[num_dia]["uvMax"]
                        f_pronostico = format_fecha(dias_json[num_dia]["fecha"])
                        prob_precipitacion, cota_nieve, estado_cielo, viento, racha_max = cls.get_campos_pcev(
                            dias_json[num_dia], cls.PERIODO_HORAS_12)
                        temperatura = dict()
                        sens_termica = dict()
                        humedad = dict()
                        temperatura["maxima"], temperatura["minima"] = cls.get_maxmin_temp(dias_json[num_dia])
                        sens_termica["maxima"], sens_termica["minima"] = cls.get_maxmin_sensa(dias_json[num_dia])
                        humedad["maxima"], humedad["minima"] = cls.get_maxmin_hum(dias_json[num_dia])
                        dia = municipio.PredicionDia(f_pronostico, prob_precipitacion, cota_nieve,
                                                     estado_cielo, viento, racha_max, temperatura,
                                                     sens_termica, humedad, uv_max)

                        prediccion_diaria.append(dia)
                    for num_dia in range(4, len(dias_json)):
                        uv_max = ""
                        if "uvMax" in dias_json[num_dia]:
                            uv_max = dias_json[num_dia]["uvMax"]
                        f_pronostico = format_fecha(dias_json[num_dia]["fecha"])
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
                        dia = municipio.PredicionDia(f_pronostico, prob_precipitacion, cota_nieve, estado_cielo, viento,
                                                     racha_max, temperatura, sens_termica, humedad, uv_max)
                        prediccion_diaria.append(dia)
                    pred_municipio = prediccion_diaria

                else:
                    for num_dia in range(len(dias_json)):
                        f_pronostico = format_fecha(dias_json[num_dia]["fecha"])
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
                        for contador in [i for i in range(size) if i % 2 == 0]:
                            periodo = dias_json[num_dia]["vientoAndRachaMax"][contador]["periodo"] + ":00"
                            viento_json = dias_json[num_dia]["vientoAndRachaMax"][contador]
                            viento[periodo] = {'velocidad': viento_json['velocidad'][0],
                                               'dir': viento_json["direccion"][0]}
                            racha_json = dias_json[num_dia]["vientoAndRachaMax"][contador + 1]
                            racha_max[periodo] = racha_json["value"]

                        dia = municipio.PrediccionHoras(f_pronostico, orto, ocaso, estado_cielo, precipitacion,
                                                        prob_precipitacion, prob_tormenta, nieve,
                                                        prob_nieve, viento, racha_max, temperatura, sens_termica,
                                                        humedad_relativa)
                        prediccion_horaria.append(dia)
                    pred_municipio = prediccion_horaria
        except Exception as exc:
            print("Exception ", format(exc))
        finally:
            return id_aemet, f_elaboracion, pred_municipio

    @classmethod
    def json_a_playa(cls, cadena_json):
        pred_playa = None
        try:
            js = json.loads(cadena_json)
            f1 = "am"
            f2 = "pm"
            id_aemet = js[0]["id"]
            f_elaboracion = format_fecha(js[0]["elaborado"])
            prediccion = js[0]["prediccion"]
            dias = list()
            if "dia" in prediccion:
                dias_json = prediccion["dia"]
                for num_dia in range(len(dias_json)):
                    dia = dias_json[num_dia]
                    fecha = str(dias_json[num_dia]["fecha"])
                    fecha = fecha[0:4] + "-" + fecha[4:6] + "-" + fecha[6:]
                    f_pronostico = format_fecha(fecha)
                    estado_cielo = {f1: dia["estadoCielo"]["f1"], f2: dia["estadoCielo"]["f2"]}
                    viento = {f1: dia["viento"]["f1"], f2: dia["viento"]["f2"]}
                    oleaje = {f1: dia["oleaje"]["f1"], f2: dia["oleaje"]["f2"]}
                    t_maxima = dia["tMaxima"]["valor1"]
                    s_termica = dia["sTermica"]["valor1"]
                    t_agua = dia["tAgua"]["valor1"]
                    uv_max = dia["uvMax"]["valor1"]
                    dia = playa.Dia(f_pronostico, estado_cielo, viento, oleaje, t_maxima, s_termica, t_agua, uv_max)
                    dias.append(dia)
            pred_playa = playa.Playa(str(id_aemet), f_elaboracion, dias)
        except Exception as exc:
            print("Exception ", format(exc))
        finally:
            return pred_playa
