# -*- coding: utf-8 -*-
import os

import psycopg2

import network.utils as utils

from configparser import ConfigParser


class BaseDatos:
    
    TABLAS_DB = ["pred_altamar", "pred_costa", "pred_montaña", "pred_municipio", "pred_playa"]
    base_dir = os.path.dirname(os.path.realpath('__file__'))
    params_db = None

    @classmethod
    def __init__(cls):
        cls.params_db = cls.config()

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

    def get_pred_altamar(self, area_altamar, f_elaboracion, f_pronostico):
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

    def insert_pred_altamar(self, area_altamar, f_elaboracion, f_pronostico, prediccion):
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

    def get_pred_costa(self, area_costa, f_elaboracion, f_pronostico):
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

    def insert_pred_costa(self, area_costa, f_elaboracion, f_pronostico, prediccion):
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

    def get_pred_montaña(self, area_montaña, f_elaboracion, f_pronostico, horas):
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

    def insert_pred_montaña(self, area_montaña, f_elaboracion, f_pronostico, prediccion):
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

    def get_pred_municipio(self, id_municipio, fecha, horas):
        sql = "SELECT f_insercion, prediccion FROM pred_municipio WHERE id = %s and f_elaboracion = %s and " + \
              "f_pronostico = %s;"
        sql_delete = "DELETE FROM pred_municipio WHERE id = %s;"
        esta_ddbb = False
        resultado = None
        try:
            with psycopg2.connect(**self.params_db) as conn:
                cur = conn.cursor()
                cur.execute(sql, (str(id_municipio), fecha, fecha))
                row = cur.fetchone()
                if row and not utils.es_ahora_mayor(row[0], horas):
                    esta_ddbb = True
                    resultado = row[1]
                else:
                    # si no devuelve ningun dato actual, eliminamos los datos antinguos de esta id
                    cur.execute(sql_delete, (str(id_municipio),))
                    print("Rows deleted: ", cur.rowcount)
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return esta_ddbb, resultado

    def insert_pred_municipio(self, id_municipio, f_elaboracion, f_pronostico, prediccion):
        sql = "INSERT INTO pred_municipio(id,f_insercion, f_elaboracion,f_pronostico,prediccion) " + \
              "VALUES(%s,%s,%s,%s,%s) RETURNING id;"
        id_muni = None
        try:
            with psycopg2.connect(**self.params_db) as conn:
                cur = conn.cursor()
                cur.execute(sql, (id_municipio, utils.get_dia_hora(), f_elaboracion, f_pronostico,  prediccion))
                id_muni = cur.fetchone()[0]
                # commit the changes to the database
                conn.commit()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return id_muni

    def get_pred_playa(self, id_playa, f_elaboracion, f_pronostico):
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

    def insert_pred_playa(self, id_playa, f_elaboracion, f_pronostico, prediccion):
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
