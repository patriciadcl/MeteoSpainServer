class Playa:
    def __init__(self, id, f_validez,estado_cielo,viento,oleaje,t_maxima,s_termica,t_agua,uv_max):
        self.__id = id
        self.__f_validez = f_validez
        self.__estado_cielo = estado_cielo
        self.__viento = viento
        self.__oleaje = oleaje
        self.__t_maxima = t_maxima
        self.__s_termica = s_termica
        self.__t_agua = t_agua
        self.__uv_max = uv_max

    @property
    def id(self):
        return self.__id

    @property
    def fecha_validez(self):
        return self.__f_validez

    @property
    def estado_cielo(self):
        return self.__estado_cielo

    @property
    def viento(self):
        return self.__viento

    @property
    def oleaje(self):
        return self.__oleaje

    @property
    def t_maxima(self):
        return self.__t_maxima

    @property
    def s_termica(self):
        return self.__s_termica

    @property
    def t_agua(self):
        return self.__t_agua

    @property
    def uv_max(self):
        return self.__uv_max

    @property
    def to_dict(self):
        diccionario = dict()
        for k, v in self.__dict__.items():
            key = k.split("__")[1]
            diccionario[key] = v
        return diccionario