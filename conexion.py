from MySQL_Connector import MySQL
import time
import logging
conexion = MySQL()
conexion.conectar()
logging.info("concectando.")
conexion.conexion.connect(database = 'TG_1')
departameno = conexion.buscar_departamento()
print(departameno)
time.sleep(5)

conexion.desconectar()