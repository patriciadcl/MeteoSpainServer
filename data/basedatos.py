# -*- coding: utf-8 -*-
import os

import psycopg2

import network.utils as utils

from configparser import ConfigParser


class BaseDatos:
    
    TABLAS_DB = ["pred_altamar", "pred_costa", "pred_montaña", "pred_municipio", "pred_playa"]
    TABLA_MUNICIPIOS = "datos_municipio"
    base_dir = os.path.dirname(os.path.realpath('__file__'))
    params_db = None

    @classmethod
    def __init__(cls, update=False):
        cls.params_db = cls.config()
        if update:
            print("Actualizando las base de datos")
            cls.drop_tables()
            cls.create_tables()
            cls.fill_municipios_table()

    @classmethod
    def config(cls, filename='basedatos.ini', section='postgresql'):
        archivo = os.path.join(cls.base_dir, "data", filename)
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

    @classmethod
    def drop_tables(cls):
        """ drop tables in the PostgreSQL database"""
        drop_table = "DROP TABLE IF EXISTS {0};"
        conexion = None
        try:
            with psycopg2.connect(**cls.params_db) as conexion:
                cur = conexion.cursor()
                for tabla in cls.TABLAS_DB:
                    print("Eliminando la tabla ", tabla)
                    command = drop_table.format(tabla)
                    cur.execute(command)
                # close communication with the PostgreSQL database server
                # Eliminamos los datos municipios
                print("Eliminando la tabla ", cls.TABLA_MUNICIPIOS)
                command = drop_table.format(cls.TABLA_MUNICIPIOS)
                cur.execute(command)
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(format(error))
        finally:
            if conexion:
                conexion.close()
                print("Conexion cerrada")

    @classmethod
    def create_tables(cls):
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
        create_table_muni = """ CREATE TABLE {0} ( 
                cod VARCHAR(255) NOT NULL,
                nombre VARCHAR(255) NOT NULL,
                cod_provincia VARCHAR(255) NOT NULL,
                latitud VARCHAR(255) NOT NULL,
                longitud VARCHAR(255) NOT NULL
                );"""
        conexion = None
        try:
            with psycopg2.connect(**cls.params_db) as conexion:
                cur = conexion.cursor()
                # create table one by one
                for tabla in cls.TABLAS_DB:
                    print("Creando la tabla ", tabla)
                    command = create_table.format(tabla)
                    cur.execute(command)
                # close communication with the PostgreSQL database server
                command = create_table_muni.format(cls.TABLA_MUNICIPIOS)
                cur.execute(command)
                cur.close()
                # commit the changes
        except (Exception, psycopg2.DatabaseError) as error:
            print(format(error))
        finally:
            if conexion:
                conexion.close()
                print("Conexion cerrada")

    @classmethod
    def fill_municipios_table(cls, filename='municipios.csv'):
        archivo = os.path.join(cls.base_dir, "data", filename)
        with open(archivo, "r", encoding='utf-8') as f_open:
            for linea in f_open:
                cod, nombre, cod_provincia, latitud, longitud = linea.split(";")
                cls.ins_datos_municipio(cod, nombre, cod_provincia, latitud, longitud)

    @classmethod
    def ins_datos_municipio(cls, cod, nombre, cod_provincia, latitud, longitud):
        sql = "INSERT INTO datos_municipio(cod,nombre,cod_provincia,latitud,longitud) " + \
              "VALUES(%s,%s,%s,%s,%s) RETURNING cod;"
        cod_municipio = None
        try:
            with psycopg2.connect(**cls.params_db) as conn:
                cur = conn.cursor()
                cur.execute(sql, (str(cod), str(nombre), str(cod_provincia), str(latitud), str(longitud)))
                cod_municipio = cur.fetchone()[0]
                # commit the changes to the database
                conn.commit()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return cod_municipio

    def get_datos_municipios(self, cod_provincia):
        sql = "SELECT cod, nombre, cod_provincia, latitud, longitud FROM datos_municipio WHERE cod_provincia = %s " + \
              "ORDER BY nombre DESC;"
        esta_ddbb = False
        resultado = None
        try:
            with psycopg2.connect(**self.params_db) as conn:
                cur = conn.cursor()
                cur.execute(sql, (str(cod_provincia)))
                rows = cur.fetchall()
                contador = 0
                cadena = None
                for row in rows:
                    cadena = cadena + "{ cod:" + str(row[0]) + ", nombre:" + str(row[1]) + ", cod_provincia:" + \
                             str(row[2]) + ", latitud:" + str(row[3]) + ", longitud:" + str(row[3]) + "}"
                    contador += 1
                    if 0 < contador < len(rows):
                        cadena += ","
                cur.close()
                if len(cadena) > 0:
                    esta_ddbb = True
                    resultado = "[" + cadena + "]"
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return esta_ddbb, resultado

    def get_altamar(self, area_altamar, f_elaboracion, f_pronostico):
        sql = "SELECT prediccion FROM pred_altamar WHERE id = %s and " + \
              "f_elaboracion  = %s and f_pronostico = %s;"
        sql_delete = "DELETE FROM pred_altamar WHERE id = %s;"
        esta_ddbb = False
        resultado = None
        try:
            with psycopg2.connect(**self.params_db) as conn:
                cur = conn.cursor()
                cur.execute(sql, (str(area_altamar), str(f_elaboracion), str(f_pronostico)))
                row = cur.fetchone()
                if row:
                    esta_ddbb = True
                    resultado = row[0]
                else:
                    # si no devuelve ningun dato actual, eliminamos los datos antinguos de esta id
                    cur.execute(sql_delete, (str(area_altamar),))
                    print("Rows deleted: ", cur.rowcount)
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return esta_ddbb, resultado

    def insert_altamar(self, area_altamar, f_elaboracion, f_pronostico, prediccion):
        sql = "INSERT INTO pred_altamar(id,f_pronostico, f_elaboracion,prediccion) " + \
              "VALUES(%s,%s,%s,%s) RETURNING id;"
        id_altamar = None
        try:
            with psycopg2.connect(**self.params_db) as conn:
                cur = conn.cursor()
                cur.execute(sql, (area_altamar, f_pronostico, f_elaboracion, prediccion))
                id_altamar = cur.fetchone()[0]
                # commit the changes to the database
                conn.commit()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return id_altamar

    def get_costa(self, area_costa, f_elaboracion, f_pronostico):
        sql = "SELECT prediccion FROM pred_costa WHERE id = %s and f_elaboracion = %s and " + \
              "f_pronostico = %s;"
        sql_delete = "DELETE FROM pred_costa WHERE id = %s;"
        esta_ddbb = False
        resultado = None
        try:
            with psycopg2.connect(**self.params_db) as conn:
                cur = conn.cursor()
                cur.execute(sql, (str(area_costa), f_pronostico, f_elaboracion))
                row = cur.fetchone()
                if row:
                    esta_ddbb = True
                    resultado = row[0]
                else:
                    # si no devuelve ningun dato actual, eliminamos los datos antinguos de esta id
                    cur.execute(sql_delete, (str(area_costa),))
                    print("Rows deleted: ", cur.rowcount)
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return esta_ddbb, resultado

    def insert_costa(self, area_costa, f_elaboracion, f_pronostico, prediccion):
        sql = "INSERT INTO pred_costa(id,f_elaboracion,f_pronostico,prediccion) " + \
              "VALUES(%s,%s,%s,%s) RETURNING id;"
        id_costa = None
        try:
            with psycopg2.connect(**self.params_db) as conn:
                cur = conn.cursor()
                cur.execute(sql, (area_costa, f_elaboracion, f_pronostico, prediccion))
                id_costa = cur.fetchone()[0]
                # commit the changes to the database
                conn.commit()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return id_costa

    def get_montaña(self, area_montaña, f_elaboracion, f_pronostico, horas):
        sql = "SELECT f_insercion,prediccion FROM pred_montaña WHERE id = %s and f_elaboracion = %s and " + \
              " f_pronostico = %s;"
        sql_delete = "DELETE FROM pred_montaña WHERE id = %s;"
        esta_ddbb = False
        resultado = None
        try:
            with psycopg2.connect(**self.params_db) as conn:
                cur = conn.cursor()
                cur.execute(sql, (str(area_montaña), f_elaboracion, f_pronostico))
                row = cur.fetchone()
                if row and not utils.es_ahora_mayor(row[0], horas):
                    esta_ddbb = True
                    resultado = row[1]
                else:
                    # si no devuelve ningun dato actual, eliminamos los datos antinguos de esta id
                    cur.execute(sql_delete, (str(area_montaña),))
                    print("Rows deleted: ", cur.rowcount)
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return esta_ddbb, resultado

    def insert_montaña(self, area_montaña, f_elaboracion, f_pronostico, prediccion):
        """ query data from the vendors table """
        sql = "INSERT INTO pred_montaña(id,f_insercion, f_elaboracion, f_pronostico,prediccion) " + \
              "VALUES(%s,%s,%s,%s,%s) RETURNING id;"
        id_montaña = None
        try:
            with psycopg2.connect(**self.params_db) as conn:
                cur = conn.cursor()
                cur.execute(sql, (area_montaña, utils.get_dia_hora(), f_elaboracion, f_pronostico, prediccion))
                id_montaña = cur.fetchone()[0]
                # commit the changes to the database
                conn.commit()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return id_montaña

    def get_municipio(self, id_municipio, fecha, horas, es_horaria=False):
        sql = "SELECT f_insercion, prediccion FROM pred_municipio WHERE id = %s and f_elaboracion = %s and " + \
              "f_pronostico = %s and pred_horaria = %s;"
        sql_delete = "DELETE FROM pred_municipio WHERE id = %s and pred_horaria = %s;"
        esta_ddbb = False
        resultado = None
        try:
            with psycopg2.connect(**self.params_db) as conn:
                cur = conn.cursor()
                cur.execute(sql, (str(id_municipio), fecha, fecha, es_horaria))
                row = cur.fetchone()
                if row and not utils.es_ahora_mayor(row[0], horas):
                    esta_ddbb = True
                    resultado = row[1]
                else:
                    # si no devuelve ningun dato actual, eliminamos los datos antinguos de esta id
                    cur.execute(sql_delete, (str(id_municipio), es_horaria))
                    print("Rows deleted: ", cur.rowcount)
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return esta_ddbb, resultado

    def get_muni_diaria(self, id_municipio, fecha, horas):
        return self.get_municipio(id_municipio, fecha, horas, False)

    def get_muni_horaria(self, id_municipio, fecha, horas):
        return self.get_municipio(id_municipio, fecha, horas, True)

    def ins_municipio(self, id_municipio, f_elaboracion, f_pronostico, prediccion, es_horaria=False):
        sql = "INSERT INTO pred_municipio(id,f_insercion, f_elaboracion,f_pronostico,pred_horaria,prediccion) " + \
              "VALUES(%s,%s,%s,%s,%s,%s) RETURNING id;"
        id_muni = None
        try:
            with psycopg2.connect(**self.params_db) as conn:
                cur = conn.cursor()
                cur.execute(sql,
                            (id_municipio, utils.get_dia_hora(), f_elaboracion, f_pronostico, es_horaria, prediccion))
                id_muni = cur.fetchone()[0]
                # commit the changes to the database
                conn.commit()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return id_muni

    def ins_muni_diaria(self, id_municipio, f_elaboracion, f_pronostico, prediccion):
        return self.ins_municipio(id_municipio, f_elaboracion, f_pronostico, prediccion, False)

    def ins_muni_horaria(self, id_municipio, f_elaboracion, f_pronostico, prediccion):
        return self.ins_municipio(id_municipio, f_elaboracion, f_pronostico, prediccion, True)

    def get_playa(self, id_playa, f_elaboracion, f_pronostico):
        """ query data from the vendors table """
        sql = "SELECT prediccion FROM pred_playa WHERE id = %s and f_elaboracion = %s and " + \
              "f_pronostico = %s;"
        sql_delete = "DELETE FROM pred_playa WHERE id = %s;"
        esta_ddbb = False
        resultado = None
        try:
            with psycopg2.connect(**self.params_db) as conn:
                cur = conn.cursor()
                cur.execute(sql, (str(id_playa), f_elaboracion, f_pronostico))
                row = cur.fetchone()
                if row:
                    esta_ddbb = True
                    resultado = row[0]
                else:
                    # si no devuelve ningun dato actual, eliminamos los datos antinguos de esta id
                    cur.execute(sql_delete, (str(id_playa),))
                    print("Rows deleted: ", cur.rowcount)
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return esta_ddbb, resultado

    def insert_playa(self, id_playa, f_elaboracion, f_pronostico, prediccion):
        sql = "INSERT INTO pred_playa(id,f_elaboracion, f_pronostico,prediccion) VALUES(%s,%s,%s,%s) RETURNING id;"
        idplaya = None
        try:
            with psycopg2.connect(**self.params_db) as conn:
                cur = conn.cursor()
                cur.execute(sql, (id_playa, f_elaboracion, f_pronostico, prediccion))
                idplaya = cur.fetchone()[0]
                # commit the changes to the database
                conn.commit()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return idplaya

    def insert_datos_municipio(self, cod, nombre, cod_provincia, latitud, longitud):
        sql = "INSERT INTO datos_municipio(cod, nombre, cod_provincia, latitud, longitud) VALUES(%s,%s,%s,%s,%s) RETURNING id;"
        idplaya = None
        try:
            with psycopg2.connect(**self.params_db) as conn:
                cur = conn.cursor()
                cur.execute(sql, (cod, nombre, cod_provincia, latitud, longitud))
                idplaya = cur.fetchone()[0]
                # commit the changes to the database
                conn.commit()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return idplaya