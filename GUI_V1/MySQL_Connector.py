#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mysql.connector
import logging
import time
import cv2 
import numpy as np

class MySQL:
    '''
    Clase DroneFacade-Admin

    Empleada para la lectura/escritura de datos desde/hacia las base 
    de datos relacional de MariaDB.

    Incluye metodos de Conexión y Desconexión a la DB TG_1.
    '''
    def __init__(self):
        super().__init__()

        self._usuario = "root"
        #############################################
        #Dirección IP del servidor 
        #############################################
        self._host = "localhost"
        #############################################
        self._contraseña = "1234"
        self._DB = "TG_1"

        self._departamento_id = 1
        self._municipio_id = 1
        self._mision_id = 3
        self._fecha = None

    def conectar(self):
        '''
        Metodo de conexión: 

        Crear u obtiene un objeto tipo MySQLConnection de conexión a un
        servidor MySQL con el que se trabaja a lo largo de los metodos que
        ejecutan sentencias SQL.

        Retorna - 
        status (Resultado de la operación) >>> True or False
        err (si aplica) >>> mysql.connector.Error 
        '''
        try:
            self.conexion = mysql.connector.connect(
                host = self._host,
                user = self._usuario,
                passwd = self._contraseña,
                database = self._DB
                
            )
            self.cursor = self.conexion.cursor()
        except mysql.connector.Error as err:  
            return False, err
        else:
            return True, None
    
    def desconectar(self):
        '''
        Metodo desconexión: 

        Cierra la conexión del objeto MySQLConnection del servidor MySQL. 

        Retorna - 
        status (Resultado de la operación) >>> True or False
        err (si aplica) >>> mysql.connector.Error 
        '''
        try:
            self.conexion.close()
        except AttributeError or mysql.connector.Error as err:   
            return False, err
        else:
            return True, None
    
    def _set_departamento(self, departamento : str):
        '''
        [Privado]        
        Metodo para la carga departamento: 

        empleado por set_mision para         
        la carga de información al servidor MySQL. 
        '''
        sql = f"INSERT IGNORE INTO departamentos (nombre) VALUES ('{departamento}')"
        self.cursor.execute(sql)
        self.conexion.commit()
        sql = f"SELECT id FROM departamentos WHERE nombre = '{departamento}'"
        self.cursor.execute(sql)
        self._departamento_id = self.cursor.fetchone()[0]

    def get_departamento(self):
        '''       
        Metodo para la lectura del departamento_id: 

        empleado por para la busqueda de información en el servidor MySQL. 
        '''
        return self._departamento_id
    
    def _set_municipio(self, municipio : str):
        '''
        [Privado]
        Metodo para la carga municipio: 

        empleado por set_mision para         
        la carga de información al servidor MySQL. 
        '''
        sql = "INSERT IGNORE INTO municipios (nombre, departamentos_id) VALUES (%s,%s)"
        val = (municipio,self._departamento_id)
        self.cursor.execute(sql,val)
        self.conexion.commit()
        sql = f"SELECT id FROM municipios WHERE nombre = '{municipio}'"
        self.cursor.execute(sql)
        self._municipio_id = self.cursor.fetchone()[0]

    def get_municipio(self):
        '''        
        Metodo para la lectura del municipio_id: 

        empleado por para la busqueda de información en el servidor MySQL. 
        '''
        return self._municipio_id

    def set_mision(self, info_obj : object):
        '''      
        Metodo para la carga de información de la misión: 

        info_obj >> tipo Datos() (REQUERIDO) Carga y actualiza la información presente en el servidor MySQL.

        Si se comparte el nombre de la misión y la fecha para valores presente en el servidor, se procede a actualizar la información.
        
        Ejemplo: 
        >>> info_obj_1  
        >>> fecha = 01/01/2020 y nombre misión = Misión 1

        SI "Misión 1" para el dia "01/01/2020" existe en el servidor => se actualizan sus campos,
        en otro caso se incluye un campo para registar como nueva misión.   

        Retorna - 
        status (Resultado de la operación) >>> True or False
        err (si aplica) >>> mysql.connector.Error     
        '''
        self._set_departamento(info_obj.departamento)
        self._set_municipio(info_obj.municipio)
        sql = "INSERT INTO mision (municipios_id, nombre_mision, nombre_fachada, fecha, descripcion, nombre_usuario, email_usuario, camara_id, camara_fx, camara_fy, camara_cx, camara_cy, camara_k1, camara_k2, camara_cv_v, camara_cv_h, coordenadas, fachada_alto, fachada_ancho, estado_mision) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (self._municipio_id,info_obj.nombre_de_la_mision,info_obj.nombre_de_la_fachada,info_obj.fecha,info_obj.descripcion,info_obj.nombre_de_usuario,info_obj.correo_usuario,
                info_obj.camara_id, info_obj.camara_fx, info_obj.camara_fy,info_obj.camara_cx,info_obj.camara_cy,info_obj.camara_k1,info_obj.camara_k2,info_obj.camara_cv_v,info_obj.camara_cv_h,
                info_obj.coordenadas,info_obj.fachada_alto,info_obj.fachada_ancho,info_obj.estado_mision) 
        try:
            self.cursor.execute(sql,val)
            self.conexion.commit()
        except:
            try:
                sql = "UPDATE mision SET municipios_id=%s, nombre_fachada=%s, descripcion=%s, nombre_usuario=%s, email_usuario=%s, camara_id=%s, camara_fx=%s, camara_fy=%s, camara_cx=%s, camara_cy=%s, camara_k1=%s, camara_k2=%s, camara_cv_v=%s, camara_cv_h=%s, coordenadas=%s, fachada_alto=%s, fachada_ancho=%s, estado_mision=%s WHERE nombre_mision =%s AND fecha =%s"
                val = (self._municipio_id,info_obj.nombre_de_la_fachada,info_obj.descripcion,info_obj.nombre_de_usuario,info_obj.correo_usuario,
                    info_obj.camara_id, info_obj.camara_fx, info_obj.camara_fy,info_obj.camara_cx,info_obj.camara_cy,info_obj.camara_k1,info_obj.camara_k2,info_obj.camara_cv_v,info_obj.camara_cv_h,
                    info_obj.coordenadas,info_obj.fachada_alto,info_obj.fachada_ancho,info_obj.estado_mision,info_obj.nombre_de_la_mision,info_obj.fecha) 
                self.cursor.execute(sql,val)
                self.conexion.commit()    
            except TypeError or mysql.connector.Error as err:  
                return False, err
        else:
            sql = f"SELECT id FROM mision WHERE nombre_mision = '{info_obj.nombre_de_la_mision}' AND fecha = '{info_obj.fecha}'"
            self.cursor.execute(sql)
            self._mision_id = self.cursor.fetchone()[0]
            self._fecha = info_obj.fecha
            return True, None
        
    def _get_mision_id(self):
        '''     
        Metodo para la lectura del mision_id: 

        empleado por para la busqueda de información en el servidor MySQL. 
        '''
        return self._mision_id

    def get_mision(self, mision_id = None, parameter = None):
        '''   
        Metodo para leer la tabla misión: 

        captura la información presente en el servidor MySQL.

        '''
        if mision_id == None : mision_id = self._mision_id
        sql = f"SELECT * FROM mision JOIN municipios ON mision.id = '{mision_id}' and municipios.id = '{self._municipio_id}'"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def set_registro(self,registro: list):
        '''      
        Metodo para la carga del registro fotográfico: 

        registro >> tipo list() (REQUERIDO) Carga la información de imagenes capturadas en el servidor MySQL.

        Extensión de la imagén >>> .jpg
        Lectura >> cv2.IMREAD_COLOR
        Espacio de color >>> cv2.COLOR_BGR2RGB
        '''  
        try:
            for imagen in registro:
                is_success, im_buf_arr = cv2.imencode(".jpg", imagen)
                byte_im = im_buf_arr.tostring()
                sql = "INSERT INTO registro_fotografico (mision_id, imagen_entrada) VALUES (%s, %s)"
                val = (self._mision_id,byte_im)
                self.cursor.execute(sql,val)
            self.conexion.commit()
        except mysql.connector.Error as err:
            return False, err
        else:
            return True, err


    def get_registro(self, mision_id = None):
        '''      
        Metodo para la lectura del registro fotográfico: 

        Lee la información de imagenes capturadas presentes en el servidor MySQL.

        Retorna -

        Lista (incluye todo el registro)>> list()
        Lectura >> cv2.IMREAD_COLOR
        Espacio de color >>> cv2.COLOR_BGR2RGB
        ''' 
        if mision_id == None : mision_id = self._mision_id
        sql = f"SELECT imagen_entrada FROM registro_fotografico WHERE mision_id = '{mision_id}'"
        self.cursor.execute(sql)
        byte_im_array = self.cursor.fetchall()
        registro = []
        for byte_im in byte_im_array:
            nparr = np.fromstring(byte_im[0], np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            registro.append(img_np)
        return registro

    def set_resutados(self, imagen_salida, info_obj: object):
        '''      
        Metodo para la lectura del registro fotográfico: 

        Lee la información de imagenes capturadas presentes en el servidor MySQL.

        Retorna 
        ''' 
        is_success, im_buf_arr = cv2.imencode(".jpg", imagen_salida)
        byte_im = im_buf_arr.tostring()        
        try:        
            sql = "INSERT INTO resultados (mision_id, fecha, imagen_salida, sizeimg_entrada, sizeimg_salida, paremtro_rd) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (self._mision_id,info_obj.fecha, byte_im, info_obj.sizeimg_entrada, info_obj.sizeimg_salida,info_obj.parametro_rd)
            self.cursor.execute(sql,val)
            self.conexion.commit()
        except mysql.connector.Error as err:
            return False, err
        else:            
            return True, None
    
    def get_resultados(self, mision_id = None):
        '''      
        Metodo para la lectura de resultados: 

        Lee la información de resultados presentes en el servidor MySQL.

        Retorna -

        Lista (fecha, Imagen de salida ...)>> list()

        Imagen: lectura >> cv2.IMREAD_COLOR
        Imagen: Espacio de color >>> cv2.COLOR_BGR2RGB
        '''
        if mision_id == None : mision_id = self._mision_id
        sql = f"SELECT fecha, imagen_salida, sizeimg_entrada, sizeimg_salida, paremtro_rd FROM resultados WHERE mision_id = '{mision_id}'"
        self.cursor.execute(sql)
        resultados = self.cursor.fetchall()
        salida = list(resultados[0])
        nparr = np.fromstring(salida[1], np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print(img_np)
        salida[1] = img_np
        return salida

    def carga_telemetria(self):
        info = object
        sql = f"SELECT id FROM mision WHERE nombre_mision = '{info.nombre_de_la_mision}' AND nombre_usuario = '{info.nombre_de_usuario}"

        try:
            logging.info("Leyendo misión...")
            self.cursor.execute(sql)
            id_mision=cursor.fetchall()

            sql = "INSERT INTO telemetria (_mision_id, hora, sensor_1, sensor_2, sensor_3, sensor_4, sensor_5) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            val = (id_mision, info.hora, info.sensor_1, info.sensor_2, info.sensor_3, info.sensor_4, info.sensor_5)
            try:
                logging.info("Añadiendo datos de telemetria...")
                self.cursor.execute(sql, val)
                self.conexion.commit()
            except mysql.connector.Error as err:   
                logging.warning("Algo ocurrio: {}".format(err))    

        except mysql.connector.Error as err:   
            logging.warning("Algo ocurrio: {}".format(err))
        else:
            logging.info("Carga exitosa!")    
        
    def carga_resultados(self):
        info = object
        sql = f"SELECT id FROM mision WHERE nombre_mision = '{info.nombre_de_la_mision}' AND nombre_usuario = '{info.nombre_de_usuario}'"

        try:
            logging.info("Leyendo misión...")
            self.cursor.execute(sql)
            id_mision=cursor.fetchall()

            sql = "INSERT INTO resultados (_mision_id, imagen_salida, sizeimg_entrada, sizeimg_salida, parametro_rd) VALUES (%s,%s,%s,%s,%s)"
            val = (id_mision, info.imagen_salida,info.size_im_entrada,info.size_im_salida,info.parametro_p_1)
            try:
                logging.info("Añadiendo datos de resultados...")
                self.cursor.execute(sql, val)
                self.conexion.commit()
            except mysql.connector.Error as err:   
                logging.warning("Algo ocurrio: {}".format(err))    

        except mysql.connector.Error as err:   
            logging.warning("Algo ocurrio: {}".format(err))
        else:
            logging.info("Carga exitosa!")    


         




            
        
