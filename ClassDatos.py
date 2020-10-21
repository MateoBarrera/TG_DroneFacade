import csv

class mainDatos:
    def __init__(self):
        super().__init__()

        #CONFIGURACIÓN
        ##camara
        self.camara_id= "ZED StereoLab"
        self.camara_fx= 699.839
        self.camara_fy= 699.839
        self.camara_cx= 675.962
        self.camara_cy= 348.013
        self.camara_k1= -0.170874
        self.camara_k2= 0.023340
        self.camara_cv_h= 90.0
        self.camara_cv_v= 60.0

        ##datos de la mision
        self.nombre_de_la_mision = ""
        self.nombre_de_usuario = ""
        self.correo_usuario = ""
        self.nombre_de_la_fachada = ""
        self.descripcion = ""
        self.fecha = ""
        self.departamento_seleccionado = ""
        self.municipio_municipio_seleccionado = ""

        self.coordenadas = ""
        self.fachada_alto = 12.0
        self.fachada_ancho = 6.0
        self.estado_mision = 0

        ##datos de ejecución

        self.hora = ""
        self.sensor_1 = ""
        self.sensor_2 = "" 
        self.sensor_3 = ""
        self.sensor_4 = ""
        self.sensor_5 = ""    

        self.registro_imagenes = ("imagen1", "imagen2", "imagen3") 

        ##datos procesamiento

        self.imagen_salida = (" ")
        self.size_im_entrada = 15.0
        self.size_im_salida = 40.0
        self.parametro_p_1 = True



        with open('ciudades.csv') as csvfile:
            DANEcsv = csv.reader(csvfile,delimiter=';')
            #line=1
            self.departamento=[]
            aux_1=""
            line = 0
            for row in DANEcsv:
                if line == 0:
                    line += 1
                else:
                    aux=row[1]
                    if aux!=aux_1:
                        self.departamento.append(aux)
                    line += 1
                    aux_1 = aux  
                        
    def buscarMunicipios(self,dep):
        with open('ciudades.csv') as csvfile:
            DANEcsv = csv.reader(csvfile,delimiter=';')
            self.municipios = []
            line = 0
            for row in DANEcsv:
                if line == 0:
                    line += 1
                else:
                    aux=row[1]
                    if aux==dep:
                        self.municipios.append(row[3])
                    line += 1