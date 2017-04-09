import psycopg2
import os
from configparser import ConfigParser

class BaseDatos:

    base_dir = os.path.dirname(os.path.realpath('__file__'))
    tablas = ["areas_altamar","areas_costa","areas_montaña","municipios","playas"]
    param_db = None

    @classmethod
    def __init__(cls, update = False):
        cls.param_db = cls.config()
        if update:
            print("Actualizando las base de datos")
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
    def connect(cls):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = cls.config()
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            # create a cursor
            cur = conn.cursor()
            # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version();')
            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)
            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        except Exception as exc:
            print("Error ", format(exc))
        return conn

    @classmethod
    def create_tables(cls):
        """ create tables in the PostgreSQL database"""
        #drop_table = " DROP TABLE IF EXISTS {0}"
        create_table = """
                CREATE TABLE {0} (
                id VARCHAR(255) NOT NULL,
                f_insercion VARCHAR(255) NOT NULL,
                f_elaboracion VARCHAR(255) NOT NULL,
                f_pronostico VARCHAR(255),
                prediccion JSON NOT NULL
            )"""
        try:
            with psycopg2.connect(**cls.param_db) as conn:
                # conn = psycopg2.connect(**params)
                cur = conn.cursor()
                # # create table one by one
                # for tabla in cls.tablas:
                #     print("Eliminando la tabla ", tabla)
                #     command = drop_table.format(tabla)
                #     print(command)
                #     cur.execute(command)
                # # close communication with the PostgreSQL database server
                # #cur.close()
                # # commit the changes
                # conn.commit()
                # create table one by one
                for tabla in cls.tablas:
                    print("Creando la tabla ", tabla)
                    command = create_table.format(tabla)
                    print(command)
                    cur.execute(command)
                    print(cur.fetchone())
                # close communication with the PostgreSQL database server
                cur.close()
                # commit the changes
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(format(error))

    def get_altamar(self, area, fecha):
        """ query data from the vendors table """
        esta_ddbb = False
        resultado = None
        try:
            with psycopg2.connect(**self.param_db) as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM areas_altamar WHERE id = %s and f_elaboracion = %s",
                            (str(area), str(fecha)))
                row = cur.fetchone()
                if row:
                    esta_ddbb = True
                    resultado = row[3]
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return esta_ddbb, resultado

    def insert_altamar(self, area, f_insercion, f_elaboracion, prediccion):
        """ query data from the vendors table """
        sql = """INSERT INTO areas_altamar(id,f_insercion,f_elaboracion,prediccion)
                     VALUES(%s,%s,%s,%s) RETURNING id;"""
        id_altamar = None
        try:
            with psycopg2.connect(**self.param_db) as conn:
                cur = conn.cursor()
                cur.execute(sql,(area,f_insercion,f_elaboracion,prediccion))
                id_altamar = cur.fetchone()[0]
                # commit the changes to the database
                conn.commit()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return id_altamar

    def get_costa(self, area, fecha):
        """ query data from the vendors table """
        sql = "SELECT * FROM areas_costa WHERE id = %s and f_elaboracion = %s"
        esta_ddbb = False
        resultado = None
        try:
            with psycopg2.connect(**self.param_db) as conn:
                cur = conn.cursor()
                cur.execute(sql,
                            (str(area),str(fecha)))
                row = cur.fetchone()
                if row:
                    esta_ddbb = True
                    resultado = row[3]
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return esta_ddbb, resultado

    def insert_costa(self, area, f_insercion, f_elaboracion, prediccion):
        """ query data from the vendors table """
        sql = """INSERT INTO areas_costa(id,f_insercion,f_elaboracion,prediccion)
                     VALUES(%s,%s,%s,%s) RETURNING id;"""
        id_costa = None
        try:
            with psycopg2.connect(**self.param_db) as conn:
                cur = conn.cursor()
                cur.execute(sql,(area,f_insercion,f_elaboracion,prediccion))
                id_costa = cur.fetchone()[0]
                # commit the changes to the database
                conn.commit()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return id_costa

    def get_montaña(self,area, f_elaboracion, f_pronostico):
        """ query data from the vendors table """
        sql = "SELECT * FROM areas_montaña WHERE id = %s and f_elaboracion = %s and f_pronostico = %s"
        esta_ddbb = False
        resultado = None
        try:
            with psycopg2.connect(**self.param_db) as conn:
                cur = conn.cursor()
                cur.execute(sql,
                            (str(area), str(f_elaboracion), str(f_pronostico)))
                row = cur.fetchone()
                if row:
                    esta_ddbb = True
                    resultado = row[3]
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return esta_ddbb, resultado

    def insert_montaña(self, area, f_insercion, f_elaboracion, f_prediccion, prediccion):
        """ query data from the vendors table """
        sql = """INSERT INTO areas_montaña(id,f_insercion,f_elaboracion,f_prediccion,prediccion)
                     VALUES(%s,%s,%s,%s) RETURNING id;"""
        id_montaña = None
        try:
            with psycopg2.connect(**self.param_db) as conn:
                cur = conn.cursor()
                cur.execute(sql,(area, f_insercion, f_elaboracion, f_prediccion, prediccion))
                id_montaña = cur.fetchone()[0]
                # commit the changes to the database
                conn.commit()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return id_montaña