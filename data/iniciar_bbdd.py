# -*- coding: utf-8 -*-
import os

import psycopg2

from configparser import ConfigParser


TABLAS_DB = ["pred_altamar", "pred_costa", "pred_montaña", "pred_municipio", "pred_playa"]
TABLA_MUNICIPIOS = "datos_municipio"
base_dir = os.path.dirname(os.path.realpath('__file__'))


def config(filename='basedatos.ini', section='postgresql'):
    archivo = os.path.join(base_dir, "data", filename)
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
            # close communication with the PostgreSQL database server
            # Eliminamos los datos municipios
            print("Eliminando la tabla ", TABLA_MUNICIPIOS)
            command = drop_table.format(TABLA_MUNICIPIOS)
            cur.execute(command)
            cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(format(error))
    finally:
        if conexion:
            conexion.close()
            print("Conexion cerrada")


def create_tables():
    """ create tables in the PostgreSQL database"""
    create_table = """
               CREATE TABLE {0} (
               id VARCHAR(255) NOT NULL,
               f_insercion VARCHAR(255),
               f_elaboracion VARCHAR(255) NOT NULL,
               f_pronostico VARCHAR(255) NOT NULL,
               pred_horaria BOOLEAN,
               prediccion JSON NOT NULL
           );"""
    create_table_muni = """ 
               CREATE TABLE {0} ( 
               cod VARCHAR(255) NOT NULL,
               nombre VARCHAR(255) NOT NULL,
               cod_provincia VARCHAR(255) NOT NULL,
               latitud VARCHAR(255) NOT NULL,
               longitud VARCHAR(255) NOT NULL
               );"""
    conexion = None
    try:
        with psycopg2.connect(**params_db) as conexion:
            cur = conexion.cursor()
            # create table one by one
            for tabla in TABLAS_DB:
                print("Creando la tabla ", tabla)
                command = create_table.format(tabla)
                cur.execute(command)
            # close communication with the PostgreSQL database server
            command = create_table_muni.format(TABLA_MUNICIPIOS)
            print(command)
            cur.execute(command)
            cur.close()
            # commit the changes
    except (Exception, psycopg2.DatabaseError) as error:
        print(format(error))
    finally:
        if conexion:
            conexion.close()
            print("Conexion cerrada")


def fill_municipios_table(filename='municipios.csv'):
    sql = "INSERT INTO datos_municipio(cod,nombre,cod_provincia,latitud,longitud) " + \
          "VALUES(%s,%s,%s,%s,%s) RETURNING cod;"
    archivo = os.path.join(base_dir, "data", filename)
    with open(archivo, "r", encoding='utf-8') as f_open:
        with psycopg2.connect(**params_db) as conn:
            cur = conn.cursor()
            for linea in f_open:
                print(linea)
                campos = linea.split(";")
                try:
                    cur.execute(sql, (str(campos[0]), str(campos[1]), str(campos[2]), str(campos[3]), str(campos[4])))
                    cod_municipio = cur.fetchone()[0]
                    if cod_municipio == str(campos[0]):
                        print("Insertado ", str(campos[0]))
                    else:
                        print("No Insertado ", str(campos[0]))
                    # commit the changes to the database
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
            cur.close()


params_db = config()
drop_tables()
create_tables()
fill_municipios_table()
