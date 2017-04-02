class ComunidadAutonoma:
    def __init__(self,f_elaboracion,f_validez, fenomenos, prediccion):
        self.__f_elaboracion = f_elaboracion
        self.__f_validez = f_validez
        self.__fenomenos = fenomenos
        self.__prediccion = prediccion

    @property
    def f_validez(self):
        return self.__f_validez

    @property
    def f_elaboracion(self):
        return self.__f_elaboracion

    @property
    def fenomenos(self):
        return self.__fenomenos

    @property
    def prediccion(self):
        return self.__prediccion

    @property
    def to_dict(self):
        diccionario = dict()
        for k, v in self.__dict__.items():
            key = k.split("__")[1]
            diccionario[key] = v
        return diccionario