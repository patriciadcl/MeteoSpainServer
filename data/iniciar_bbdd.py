# -*- coding: utf-8 -*-
import os

import psycopg2

from configparser import ConfigParser


TABLAS_DB = ["pred_altamar", "pred_costa", "pred_montaña", "pred_municipio", "pred_playa"]
base_dir = os.path.dirname(os.path.realpath('__file__'))


def config(filename='basedatos.ini', section='postgresql'):
    # archivo = os.path.join(base_dir, "data", filename)
    archivo = filename
    print(archivo)
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(archivo)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def drop_tables():
    """ drop tables in the PostgreSQL database"""
    drop_table = "DROP TABLE IF EXISTS {0};"
    conexion = None
    try:
        with psycopg2.connect(**params_db) as conexion:
            cur = conexion.cursor()
            for tabla in TABLAS_DB:
                print("Eliminando la tabla ", tabla)
                command = drop_table.format(tabla)
                cur.execute(command)
            cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(format(error))
    finally:
        if conexion:
            conexion.close()


def create_tables():
    """ create tables in the PostgreSQL database"""
    create_table = """
               CREATE TABLE {0} (
               id VARCHAR(255) NOT NULL,
               f_insercion VARCHAR(255),
               f_elaboracion VARCHAR(255) NOT NULL,
               f_pronostico VARCHAR(255) NOT NULL,
               prediccion JSON NOT NULL
           );"""

    conexion = None
    try:
        with psycopg2.connect(**params_db) as conexion:
            cur = conexion.cursor()
            for tabla in TABLAS_DB:
                print("Creando la tabla ", tabla)
                command = create_table.format(tabla)
                cur.execute(command)
            cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(format(error))
    finally:
        if conexion:
            conexion.close()

params_db = config()
drop_tables()
create_tables()
