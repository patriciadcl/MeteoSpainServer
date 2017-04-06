class AemetAPI:

    DATOS_AEMET = dict(
        AEMET_API_KEY="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwYXRyaWNpYWRjbEBnbWFpbC5jb20iLCJqdGkiOiI3" +
                      "MGU3ZjQ5Yy05ZGY1LTQ3ZDEtYTViMy05YjBmOWJhNDFkMmMiLCJleHAiOjE0OTY5MzQxNjMsI" +
                      "mlzcyI6IkFFTUVUIiwiaWF0IjoxNDg5MTU4MTYzLCJ1c2VySWQiOiI3MGU3ZjQ5Yy05ZGY1LT" +
                      "Q3ZDEtYTViMy05YjBmOWJhNDFkMmMiLCJyb2xlIjoiIn0.qyhEVJ3tiUyq7UzDRHmXGHS8Icx" +
                      "zZoej1V3KnSN9XpU",
        URL_BASE="https://opendata.aemet.es/opendata/api/prediccion", PATH_MONTAÑA="/especifica/montaña/pasada/area",
        PATH_MONTAÑA_DIA="/dia", PATH_MUNICIPIO="/especifica/municipio", PATH_MUNICIPIO_DIARIA="/diaria",
        PATH_MUNICIPIO_HORARIA="/horaria", PATH_PLAYA="/especifica/playa", PATH_MARITIMA="/maritima",
        PATH_ALTAMAR="/altamar/area", PATH_COSTA="/costera/costa")
    

    @classmethod
    def url_montaña(cls, id_area, dia):
        address = cls.DATOS_AEMET["PATH_MONTAÑA"] + "/" + id_area + cls.DATOS_AEMET["PATH_MONTAÑA_DIA"] + "/" + dia
        url = cls.DATOS_AEMET["URL_BASE"] + address
        return url

    @classmethod
    def url_municipio_dia(cls, id_municipio):
        url = cls.DATOS_AEMET["URL_BASE"] + cls.DATOS_AEMET["PATH_MUNICIPIO"] + \
              cls.DATOS_AEMET["PATH_MUNICIPIO_DIARIA"] + "/" + id_municipio
        return url

    @classmethod
    def url_municipio_horas(cls, id_municipio):
        url = cls.DATOS_AEMET["URL_BASE"] + cls.DATOS_AEMET["PATH_MUNICIPIO"] + \
              cls.DATOS_AEMET["PATH_MUNICIPIO_HORARIA"] + "/" + id_municipio
        return url

    @classmethod
    def url_playa(cls, id_playa):
        url = cls.DATOS_AEMET["URL_BASE"] + cls.DATOS_AEMET["PATH_PLAYA"] + "/" + id_playa
        return url

    @classmethod
    def url_altamar(cls, id_altamar):
        url = cls.DATOS_AEMET["URL_BASE"] +  cls.DATOS_AEMET["PATH_MARITIMA"] + \
              cls.DATOS_AEMET["PATH_ALTAMAR"] + "/" + id_altamar
        return url

    @classmethod
    def url_costa(cls, id_costa):
        url = cls.DATOS_AEMET["URL_BASE"] + cls.DATOS_AEMET["PATH_COSTERA"] + "/" + id_costa
        return url
