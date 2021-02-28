#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

class Datos:
    def __init__(self):
        super().__init__()
        #CONFIGURACIÓN
        ##camara
        self.camara_id= "ZED StereoLab"
        self.camara_fx= 699.84268554688
        self.camara_fy= 699.84268554688
        self.camara_cx= 675.96219726562
        self.camara_cy= 348.0130004882812
        self.camara_k1= -0.17087399959564
        self.camara_k2= 0.023340599611402
        self.camara_cv_h= 90.0
        self.camara_cv_v= 60.0

        ##datos de la mision
        self.nombre_de_la_mision = "Misión 3"
        self.nombre_de_usuario = "None"
        self.correo_usuario = "None"
        self.nombre_de_la_fachada = "None"
        self.descripcion = "None"
        self.fecha = "None"
        self.departamento = "Valla"
        self.municipio = "Cali"

        self.coordenadas = "None"
        self.fachada_alto = "None"
        self.fachada_ancho = "None"
        self.estado_mision = "None"

        ##datos procesamiento

        self.imagen_salida = "None"
        self.sizeimg_entrada = "None"
        self.sizeimg_salida = "None"
        self.parametro_rd = "a"



        with open('ciudades.csv') as csvfile:
            DANEcsv = csv.reader(csvfile,delimiter=';')
            #line=1
            self.departamento_list=[]
            aux_1=""
            line = 0
            for row in DANEcsv:
                if line == 0:
                    line += 1
                else:
                    aux=row[1]
                    if aux!=aux_1:
                        self.departamento_list.append(aux)
                    line += 1
                    aux_1 = aux
      
                        
    def buscarMunicipios(self,dep):
        with open('ciudades.csv') as csvfile:
            DANEcsv = csv.reader(csvfile,delimiter=';')
            self.municipios_list = []
            line = 0
            for row in DANEcsv:
                if line == 0:
                    line += 1
                else:
                    aux=row[1]
                    if aux==dep:
                        self.municipios_list.append(row[3])
                    line += 1

