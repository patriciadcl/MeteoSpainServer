from datetime import *

dia_format = "%d-%m-%Y"
dia_hora_format = "%d-%m-%Y %H:%M"


def format_fecha(fecha):
    new_fecha = str(fecha).split("-")
    new_fecha.reverse()
    return new_fecha[0] + "-" + new_fecha[1] + "-" + new_fecha[2]


def get_hoy():
    return date.today().strftime(dia_format)


def get_dia_hora():
    return datetime.now().strftime(dia_hora_format)


def get_proximo_dia(dias):
    proximo_dia = date.today() + timedelta(days=dias)
    return proximo_dia.strftime(dia_format)


def es_ahora_mayor(fecha_comprobar, horas):
    ahora = get_dia_hora()
    ahora = datetime.strptime(ahora, dia_hora_format)
    dia_origen = datetime.strptime(fecha_comprobar, dia_hora_format)
    incremento = timedelta(seconds=horas*60)
    if (dia_origen + incremento) < ahora:
        return True
    else:
        return False


def es_mayor(fecha_inicial, fecha_final, horas):
    f_inicial = datetime.strptime(fecha_inicial, dia_hora_format)
    f_final = datetime.strptime(fecha_final, dia_hora_format)
    incremento = timedelta(seconds=horas * 60)
    if (f_inicial + incremento) < f_final:
        return True
    else:
        return False
