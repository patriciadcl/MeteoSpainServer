import network.aemetapi as api

class Servidor:
    def __init__(self) -> None:
        super().__init__()
        self._archivo_armet = "datos_api.json"
        self._aemet_api = api.AemetAPI(self._archivo_armet)
