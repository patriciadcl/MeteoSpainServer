class Ozono:
    def __init__(self,f_validez, estacion, indicativo, dato):
        self.__f_validez = f_validez
        self.__estacion = estacion
        self.__indicativo = indicativo
        self.__dato = dato

    @property
    def f_validez(self):
        return self.__f_validez

    @property
    def estacion(self):
        return self.__estacion

    @property
    def indicativo(self):
        return self.__indicativo

    @property
    def dato(self):
        return self.__dato

    @property
    def to_dict(self):
        diccionario = dict()
        for k, v in self.__dict__.items():
            key = k.split("__")[1]
            diccionario[key] = v
        return diccionario