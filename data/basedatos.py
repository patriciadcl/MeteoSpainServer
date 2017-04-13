# -*- coding: utf-8 -*-
import os

import psycopg2

import network.utils as utils

from configparser import ConfigParser


class BaseDatos:
    
    TABLAS_DB = ["areas_altamar", "areas_costa", "areas_montaña", "municipios", "playas"]
    base_dir = os.path.dirname(os.path.realpath('__file__'))
    params_db = None

    @classmethod
    def __init__(cls, update=False):
        cls.params_db = cls.config()
        if update:
            print("Actualizando las base de datos")
            cls.drop_tables()
            cls.create_tables()

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
                cur.close()
                # commit the changes
        except (Exception, psycopg2.DatabaseError) as error:
            print(format(error))
        finally:
            if conexion:
                conexion.close()
                print("Conexion cerrada")

    def get_altamar(self, area_altamar, f_elaboracion, f_pronostico):
        sql = "SELECT prediccion FROM areas_altamar WHERE id = %s and " + \
              "f_elaboracion  = %s and f_pronostico = %s;"
        sql_delete = "DELETE FROM areas_altamar WHERE id = %s;"
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
        sql = "INSERT INTO areas_altamar(id,f_pronostico, f_elaboracion,prediccion) " + \
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
        sql = "SELECT prediccion FROM areas_costa WHERE id = %s and f_elaboracion = %s and " + \
              "f_pronostico = %s;"
        sql_delete = "DELETE FROM areas_costa WHERE id = %s;"
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
        sql = "INSERT INTO areas_costa(id,f_elaboracion,f_pronostico,prediccion) " + \
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
        sql = "SELECT f_insercion,prediccion FROM areas_montaña WHERE id = %s and f_elaboracion = %s and " + \
              " f_pronostico = %s;"
        sql_delete = "DELETE FROM areas_montaña WHERE id = %s;"
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
        sql = "INSERT INTO areas_montaña(id,f_insercion, f_elaboracion, f_pronostico,prediccion) " + \
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
        sql = "SELECT f_insercion, prediccion FROM municipios WHERE id = %s and f_elaboracion = %s and " + \
              "f_pronostico = %s and pred_horaria = %s;"
        sql_delete = "DELETE FROM municipios WHERE id = %s and pred_horaria = %s;"
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
        sql = "INSERT INTO municipios(id,f_insercion, f_elaboracion,f_pronostico,pred_horaria,prediccion) " + \
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
        sql = "SELECT prediccion FROM playas WHERE id = %s and f_elaboracion = %s and " + \
              "f_pronostico = %s;"
        sql_delete = "DELETE FROM playas WHERE id = %s;"
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
        sql = "INSERT INTO playas(id,f_elaboracion, f_pronostico,prediccion) VALUES(%s,%s,%s,%s) RETURNING id;"
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
