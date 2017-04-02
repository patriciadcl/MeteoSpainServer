import json
import modelo.altamar as altamar
import modelo.costas as costas


class JsonAModelo:

    @staticmethod
    def girar_fecha(fecha):
        new_fecha = str(fecha).split("-")
        new_fecha.reverse()
        return new_fecha[0] + "-" + new_fecha[1] + "-" + new_fecha[2]

    @classmethod
    def get_altamar(self,cadena_json):
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
    def get_costas(self,cadena_json):
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
