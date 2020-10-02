import mysql.connector
import logging
import time
#from ClassDatos import mainDatos

class MySQL:
    '''
    Esta clase es usada para la lectura/escritura de datos desde/hacia las base 
    de datos MySQL de MariaDB. Para esto se hace uso de la libreria para python 
    mysql-connector en su versión (2.2.9).
    '''

    #--------------------------------------------------------------------------
    # Creación de atributos para la conexión
    #--------------------------------------------------------------------------
    def __init__(self):
        super().__init__()

        self.usuario = "jetsonnano"
        #############################################
        #Dirección IP del servidor 
        #############################################
        self.host = "192.168.0.7"
        #############################################
        self.contraseña = "Jetson3744"
        self.DB = "TG_1"


    #--------------------------------------------------------------------------
    # Este metodo se emplea para establecer la conexión con la base de datos
    #--------------------------------------------------------------------------
    def conectar(self):
        try:
            logging.info("Estableciendo conexión con el servidor...")
            self.conexion = mysql.connector.connect(
                host = self.host,
                user = self.usuario,
                passwd = self.contraseña
            )
            self.cursor = self.conexion.cursor()
        except mysql.connector.Error as err:   
            logging.warning("Algo ocurrio: {}".format(err))
        else:
            logging.info("Conexión exitosa!")
    

    #--------------------------------------------------------------------------
    # Este metodo se emplea para realizar la desconexión con la base de datos
    #--------------------------------------------------------------------------    
    def desconectar(self):
        try:
            logging.info("Cerrando conexión con el servidor...")
            self.conexion.close()

        except mysql.connector.Error as err:   
            logging.warning("Algo ocurrio: {}".format(err))
        else:
            logging.info("Desconexión exitosa!")

    #--------------------------------------------------------------------------
    # Este metodo se emplea para realizar la carga de la etapa de CONFIGURACIÓN
    #-------------------------------------------------------------------------        
    def carga_configuracion(self):
        info = mainDatos()
        sql = f"SELECT id FROM departamentos WHERE departamento = '{info.departamento_seleccionado}'"
        try:
            logging.info("Cargando departamento...")
            self.cursor.execute(sql)
            id_departamento=cursor.fetchall()
            
            sql = f"SELECT id FROM municipios WHERE municipio = '{info.municipio_seleccionado}'"
            try:
                logging.info("Cargando municipio...")
                self.cursor.execute(sql)
                id_municipio=cursor.fetchall()
            
            except mysql.connector.Error as err:   
                logging.warning("Algo ocurrio: {}".format(err))

            sql = f"UPDATE municipio SET departamento_id = '{id_departamento[0]}' WHERE id = '{id_municipio[0]}'"
            try:
                logging.info("Cargando municipio...")
                self.cursor.execute(sql)
                self.conexion.commit()

                sql = "INSERT INTO mision (municipio_id, nombre_mision, nombre_fachada, fecha, descripcion, nombre_usuario, email_usuario, camara_id, camara_fx, camara_fy, camara_cx, camara_cy, camara_k1, camara_k2, camara_cv_v, camara_cv_h, coordenadas, fachada_alto, fachada_ancho, estado_mision) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (id_municipio,info.nombre_de_la_mision,info.nombre_de_la_fachada,info.fecha,info.descripcion,info.nombre_de_usuario,info.email_usuario,
                        info.camara_id, info.camara_fx, info.camara_fy,info.camara_cx,info.camara_cy,info.camara_k1,info.camara_k2,info.camara_cv_v,info.camara_cv_h,
                        info.coordenadas,info.fachada_alto,info.fachada_ancho,indo.estado_mision) 

                try:
                    logging.info("Cargado datos de usario...")
                    self.cursor.execute(sql, val)
                    self.conexion.commit()
                except mysql.connector.Error as err:   
                    logging.warning("Algo ocurrio: {}".format(err))                            
            
            except mysql.connector.Error as err:   
                logging.warning("Algo ocurrio: {}".format(err))
                     
        except mysql.connector.Error as err:   
            logging.warning("Algo ocurrio: {}".format(err))
        else:
            logging.info("Carga exitosa!")


    #--------------------------------------------------------------------------
    # Este metodo se emplea para realizar la carga de la TELEMETRIA
    #-------------------------------------------------------------------------        
    def carga_telemetria(self):
        info = mainDatos()
        sql = f"SELECT id FROM mision WHERE nombre_mision = '{info.nombre_de_la_mision}' AND nombre_usuario = '{info.nombre_de_usuario}"

        try:
            logging.info("Leyendo misión...")
            self.cursor.execute(sql)
            id_mision=cursor.fetchall()

            sql = "INSERT INTO telemetria (mision_id, hora, sensor_1, sensor_2, sensor_3, sensor_4, sensor_5) VALUES (%s,%s,%s,%s,%s,%s,%s)"
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


    #--------------------------------------------------------------------------
    # Este metodo se emplea para realizar la carga del REGISTRO FOTOGRÁFICO
    #-------------------------------------------------------------------------        
    def carga_registo_fotografico(self):
        info = mainDatos()
        sql = f"SELECT id FROM mision WHERE nombre_mision = '{info.nombre_de_la_mision}' AND nombre_usuario = '{info.nombre_de_usuario}"

        try:
            logging.info("Leyendo misión...")
            self.cursor.execute(sql)
            id_mision=cursor.fetchall()

            for imagen in info.registro_imagenes:

                sql = "INSERT INTO registro_fotografico (mision_id, imagen_entrada) VALUES (%s,%s)"
                val = (id_mision, imagen)
                try:
                    logging.info("Añadiendo datos registro fotografico...")
                    self.cursor.execute(sql, val)
                    self.conexion.commit()
                except mysql.connector.Error as err:   
                    logging.warning("Algo ocurrio: {}".format(err))    

        except mysql.connector.Error as err:   
            logging.warning("Algo ocurrio: {}".format(err))
        else:
            logging.info("Carga exitosa!")    


    #--------------------------------------------------------------------------
    # Este metodo se emplea para realizar la carga de RESULTADOS
    #-------------------------------------------------------------------------        
    def carga_resultados(self):
        info = mainDatos()
        sql = f"SELECT id FROM mision WHERE nombre_mision = '{info.nombre_de_la_mision}' AND nombre_usuario = '{info.nombre_de_usuario}'"

        try:
            logging.info("Leyendo misión...")
            self.cursor.execute(sql)
            id_mision=cursor.fetchall()

            sql = "INSERT INTO resultados (mision_id, imagen_salida, sizeimg_entrada, sizeimg_salida, parametro_rd) VALUES (%s,%s,%s,%s,%s)"
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

    def buscar_departamento(self):
        sql = "SELECT * FROM departamentos"
        resultado_busqueda = " "
        try:
            logging.info("Buscando accesos del usuario en la base de datos de AUNAR...")
            self.cursor.execute(sql)
            resultado_busqueda=self.cursor.fetchall()
        except mysql.connector.Error as err:   
            logging.warning("Algo ocurrio: {}".format(err))
        else:
            logging.info("Buscando...")
        if(not resultado_busqueda ):
           logging.warning("El usuario no ha accedido a las instalaciones.")
           resultado_busqueda = " "
        else:
            logging.info("Listando accesos:")

        return resultado_busqueda
         




            
        
