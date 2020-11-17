#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import xml.etree.ElementTree as ET
import math
import sys
import re
import time
import pyqtgraph as pg
import numpy as np
import cv2
import imutils
import matplotlib.pyplot as plt
from imutils import paths
from pyqtgraph import PlotWidget, plot
from mpl_toolkits.mplot3d.proj3d import proj_transform
from mpl_toolkits.mplot3d import axes3d, Axes3D
from matplotlib.patches import FancyArrowPatch
from ClassDatos import Datos
from PyQt5 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets 
from ClassWindow1 import Ui_DroneFacade
from geopy.distance import geodesic
import rospy
from Matrice100 import Matrice100Services, Matrice100Topics

import rosgraph
from std_msgs.msg import UInt8
from dji_sdk.msg import *

import base64
import paramiko
from paramiko import SSHClient

import folium
import io


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_DroneFacade()
        self.ui.setupUi(self)
        self.datos_obj = Datos()
        self.calibracionCamara = (self.datos_obj.camara_id, self.datos_obj.camara_fx, self.datos_obj.camara_fy, self.datos_obj.camara_cx, 
            self.datos_obj.camara_cy, self.datos_obj.camara_k1, self.datos_obj.camara_k2, self.datos_obj.camara_cv_h, self.datos_obj.camara_cv_v)
        self.parametrosCamara()
        self.departamento = self.datos_obj.departamento_list


        #Jetson
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()  
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        self.JetsonSSH = ssh 

        #Display buttons
        self.ui.inicioButton.clicked.connect(self.display_1)
        self.ui.configuracionButton.clicked.connect(self.display_2)
        self.ui.procesamientoButton.clicked.connect(self.display_4)
        self.ui.resultadosButton.clicked.connect(self.display_5)

        #Especificaciones del UAV
        self.UAV_REF = "DJI Matrice 100"
        self.UAV_Capacidad_Bateria = 4500
        self.UAV_Voltaje_Bateria = 22.2
        self.UAV_Peso = 2.355
        self.UAV_Potencia_x_Kg = 170
        self.UAV_Factor_Seguridad = 0.7
        self.UAV_Velocidad_Crucero = 0.5


        #Ventana de Configuración
        self.altura_fachada = 0
        self.ui.confZedButton.setChecked(True)
        self.ui.confZedButton.clicked.connect(self.parametrosCamara)
        self.ui.confmodoCamararadioButton.clicked.connect(self.parametrosCamara)
        self.ui.conffxSpinBox.setDisabled(True)
        self.ui.conffySpinBox.setDisabled(True)
        self.ui.confcxSpinBox.setDisabled(True)
        self.ui.confcySpinBox.setDisabled(True)
        self.ui.confk1SpinBox.setDisabled(True)
        self.ui.confk2SpinBox.setDisabled(True)

        self.ui.configuracionLabel.setDisabled(True)
        self.ui.ejecucionLabel.setDisabled(True)
        self.ui.procesamientoLabel.setDisabled(True)
        self.ui.resultadosLabel.setDisabled(True)

        for index in range (len(self.departamento)):
            self.ui.confcomboDepartamento.addItem(self.departamento[index])
        self.ui.confcomboDepartamento.currentIndexChanged.connect(self.comboMunicipios)

        self.wp_entrada = []
        self.wp_trayectoria = []
        self.wp_cap_1 = []
        self.wp_cap_2 = []
        self.distancia_wp = 5
        self.ui.confimportarWaypoints.clicked.connect(self.cargarWaypoint)
        self.ui.confgenerarTrayectoria.clicked.connect(self.generarTrayectoriaConf)
        self.ui.conftrayectoriaplot.canvas.ax.set_facecolor('#faf9fa')
        self.ui.conftrayectoriaplot.canvas.ax.mouse_init(rotate_btn=1, zoom_btn=3)


        self.flag_validacion = False
        self.reg_exp_1 = "^[a-z-A-Z_0-9áéíóúñÑ]+|([a-z-A-Z_0-9áéíóúñÑ]+\s[a-z-A-Z_0-9áéíóúñÑ]+)+"
        self.reg_exp_2 = '^[(a-z0-9.)]+@[(a-z0-9)]+\.[(a-z.)]{2,15}$'
        self.ui.confnombreMision.textChanged.connect(self.chequeo_datos)
        self.ui.confnombreUsuario.textChanged.connect(self.chequeo_datos)
        self.ui.confnombreFachada.textChanged.connect(self.chequeo_datos)
        self.ui.confdescripcion.textChanged.connect(self.chequeo_datos)
        self.ui.confcorreoUsuario.textChanged.connect(self.chequeo_correo)
        self.ui.confnombreMision.textChanged.connect(self.validacion_conf)
        self.ui.confnombreUsuario.textChanged.connect(self.validacion_conf)
        self.ui.confnombreFachada.textChanged.connect(self.validacion_conf)
        self.ui.confdescripcion.textChanged.connect(self.validacion_conf)
        self.ui.confcorreoUsuario.textChanged.connect(self.validacion_conf)
        
        #Ventana Ejecución
        self.mision_iniciada = False
        self.ros_node = []
        self.conexion_jetson = True
        self.ros_node_status = True
        self.MatriceSrv = Matrice100Services()
        self.MatriceTop = []
        self.num_wp = 0
        self.cameraPID = 0
        self.ui.ejectGraficaTelemetria.setBackground(background='#ffffff')
        self.p1_telemetria = self.ui.ejectGraficaTelemetria.addPlot()
        self.p1_telemetria.setTitle('Captura de telemetría')
        self.p1_telemetria.setLabel('left','Magnitud', units='?')
        self.p1_telemetria.setLabel('bottom', 'Muestra', units='n')
        self.ui.ejecucionButton.clicked.connect(self.cargarConfiguracion)
        self.ui.ejecttrayectoriaPlot.canvas.ax.set_facecolor('#faf9fa')
        self.ui.ejecttrayectoriaPlot.canvas.ax.mouse_init(rotate_btn=1, zoom_btn=3)
        self.ui.ejectCapturarWP.clicked.connect(self.capturar_wp)
        self.ui.ejectplayButton.clicked.connect(self.iniciarMision)
        self.ui.ejectpausaButton.clicked.connect(self.pausarMision)
        self.ui.ejectstopButton.clicked.connect(self.detenerMision)
        
        master = rosgraph.Master('/rosout')
        if master.is_online():
            self.ui.ejectstatus.setStyleSheet('background-color: rgb(46, 140, 16);')
            self.ui.ejectstatus.setText("CONECTADO ONBOARD PC")
            try:
                master.lookupNode('/dji_sdk')
                self.ros_node = rospy.init_node('dronfacade_node', anonymous=True)
                print("Nodo listo")
                self.ui.ejectstatus.setStyleSheet('background-color: rgb(46, 140, 16);')
                self.ui.ejectstatus.setText("CONECTADO")
                self.ui.ejectpausaButton.setDisabled(True)
                self.ui.ejectstopButton.setDisabled(True) 
            except Exception as e:
                print("Nodo no disponible")
                self.ui.ejectstatus.setStyleSheet('background-color: rgb(235, 15, 15);')
                self.ui.ejectstatus.setText("NO CONECTADO CON EL UAV")

        else:
            self.ui.ejectstatus.setStyleSheet('background-color: rgb(235, 15, 15);')
            self.ui.ejectstatus.setText("ONBOARD PC NO DISPONIBLE")                     

        
       


        #Ventana de Procesamiento
        pg.setConfigOptions(imageAxisOrder='col-major')
        pg.setConfigOptions(antialias=True)
        self.imagenes_entrada = []
        self.imagen_entrada_index = 0
        self.image_out_size = []
        self.directorioImagenes = ""
        self.alto_img_in = 0 
        self.acho_img_in = 0 
        self.canales_img_in = 0
        self.numero_imagenes = 0
        self.ui.procPreview.setDisabled(True)
        self.p1_inputView = self.ui.procPreview.addPlot() 
        self.ui.procPreview.setBackground(background='#faf9fa')
        self.p1_inputView.hideAxis('left')
        self.p1_inputView.hideAxis('bottom')
        self.p1_inputView.setAspectLocked()

        self.ui.procPreviewSiguiente.clicked.connect(self.previewSig)
        self.ui.procPreviewPrevio.clicked.connect(self.previewPrev)

        self.ui.procCargarDirectorio.clicked.connect(self.procOpenDirectorio)
        self.ui.procHabilitarInteraccion.clicked.connect(self.interaccion)
        self.ui.procMostrarEjes.clicked.connect(self.mostarEjes)
        self.ui.procRegionInteres.clicked.connect(self.regionInteres)
        self.ui.procimageView.setBackground(background='#faf9fa')
        
        
        #row=2, col=0
        self.p1_imageView = self.ui.procimageView.addPlot()          
        self.p1_imageView.hideAxis('left')
        self.p1_imageView.hideAxis('bottom')
        self.p1_imageView.vb.setMouseEnabled(y=False,x=False)
        self.p1_imageView.setAspectLocked()
        self.ui.procimageView.nextRow()
        self.p2_imageView = self.ui.procimageView.addPlot(colspan=2)
        self.p2_imageView.hideAxis('left')
        self.p2_imageView.hideAxis('bottom')
        self.p2_imageView.setAspectLocked()
        self.p2_imageView.vb.setMouseEnabled(y=False,x=False)
        self.ui.procimageView.removeItem(self.p2_imageView) 
       
        # Custom ROI for selecting an self.image_out region
        self.roi = pg.ROI([50, 50], [0, 200])
        self.roi.addScaleHandle([1, 1], [0, 0])
        #self.roi.addScaleHandle([0, 0.5], [0.5, 0.5])
        self.roi.setSize([200,200])
        self.roi.setZValue(10)
        self.roi.sigRegionChanged.connect(self.actualizarROI)

        self.image_out = cv2.imread("imagen_1.png", cv2.IMREAD_COLOR)
        self.visualizarImageOut(self.image_out)

        self.ui.procGenerarMosaico.clicked.connect(self.stitching)
        
        self.ui.resultadosButton_2.clicked.connect(self.display_5)
        self.ui.pushButton_7.clicked.connect(self.display_6)

    ################# MAIN #################

    def display_1(self):
        self.ui.area1.setCurrentIndex(0)
        self.ui.resultadosLabel.setDisabled(True)
        self.ui.inicioLabel.setEnabled(True)
        
    def display_2(self):
        self.ui.area1.setCurrentIndex(1) 
        self.ui.inicioLabel.setDisabled(True)
        self.ui.configuracionLabel.setEnabled(True)
      
    def display_3(self):
        self.ui.area1.setCurrentIndex(2)
        self.ui.configuracionLabel.setDisabled(True)
        self.ui.ejecucionLabel.setEnabled(True) 
        self.ui.ejecttrayectoriaPlot.canvas.draw()

    def display_4(self):
        self.ui.area1.setCurrentIndex(3)
        self.ui.ejecucionLabel.setDisabled(True)
        self.ui.procesamientoLabel.setEnabled(True)
               
    def display_5(self):
        self.ui.area1.setCurrentIndex(4)
        self.ui.inicioLabel.setDisabled(True)
        self.ui.procesamientoLabel.setDisabled(True)
        self.ui.resultadosLabel.setEnabled(True)

    def display_6(self):
        self.ui.area1.setCurrentIndex(5)


    ################ CONFIGURACIÓN ################
    def parametrosCamara(self):
        index = self.ui.confmodoCamararadioButton.isChecked()
        calibracionCamara = list(self.calibracionCamara)
        if (index == False):
            self.ui.confrefCamara.setDisabled(True)
            self.ui.conffxSpinBox.setDisabled(True)
            self.ui.conffySpinBox.setDisabled(True)
            self.ui.confcxSpinBox.setDisabled(True)
            self.ui.confcySpinBox.setDisabled(True)
            self.ui.confk1SpinBox.setDisabled(True)
            self.ui.confk2SpinBox.setDisabled(True)
            self.ui.confcvHSpinBox.setDisabled(True)
            self.ui.confcvVSpinBox.setDisabled(True) 
            self.ui.confrefCamara.setText(calibracionCamara[0])   
            self.ui.conffxSpinBox.setValue(calibracionCamara[1])
            self.ui.conffySpinBox.setValue(calibracionCamara[2])
            self.ui.confcxSpinBox.setValue(calibracionCamara[3])
            self.ui.confcySpinBox.setValue(calibracionCamara[4])
            self.ui.confk1SpinBox.setValue(calibracionCamara[5])
            self.ui.confk2SpinBox.setValue(calibracionCamara[6])
            self.ui.confcvHSpinBox.setValue(calibracionCamara[7])
            self.ui.confcvVSpinBox.setValue(calibracionCamara[8])
        else:
            self.ui.confrefCamara.setEnabled(True)
            self.ui.conffxSpinBox.setEnabled(True)
            self.ui.conffySpinBox.setEnabled(True)
            self.ui.confcxSpinBox.setEnabled(True)
            self.ui.confcySpinBox.setEnabled(True)
            self.ui.confk1SpinBox.setEnabled(True)
            self.ui.confk2SpinBox.setEnabled(True)
            self.ui.confcvHSpinBox.setEnabled(True)
            self.ui.confcvVSpinBox.setEnabled(True)     

    def comboMunicipios(self):
        
        self.ui.confcomboMunicipio.clear()
        self.ui.confcomboMunicipio.addItem("Municipio")
        dep = self.ui.confcomboDepartamento.currentText()
        self.datos_obj.buscarMunicipios(dep)
        for index in range (len(self.datos_obj.municipios_list)):
            self.ui.confcomboMunicipio.addItem(self.datos_obj.municipios_list[index])

    def cargarWaypoint(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Cargar Waypoints', '/home', filter="gpx(*.gpx)")
        if filename[0]:
            self.ui.confrutaWaypoints.setText(filename[0])
            self.wp_entrada = self.leerFicheroGPX(filename[0])
            wp_entrada_ydata = self.wp_entrada['latitude'].tolist()
            wp_entrada_xdata = self.wp_entrada['longitude'].tolist()
            wp_entrada_zdata = self.wp_entrada['altitude'].tolist()
            media = self.wp_entrada.mean(axis=0)
            media_z = media['altitude']

            self.ui.conftrayectoriaplot.canvas.ax.cla()
            self.ui.conftrayectoriaplot.canvas.ax.set_zlim(media_z*0.9,media_z*1.1)
            self.ui.conftrayectoriaplot.canvas.ax.scatter(wp_entrada_xdata, wp_entrada_ydata, wp_entrada_zdata, s = 50, c = 'navy', label = 'Wpt entrada', marker = '.')
            self.ui.conftrayectoriaplot.canvas.ax.legend(loc='lower left', ncol=2, borderaxespad=0.)
            self.ui.conftrayectoriaplot.canvas.draw()
            self.ui.confgenerarTrayectoria.setEnabled(True)
            latitude_map = media['latitude']
            longitude_map = media['longitude']
            data = io.BytesIO()
            mapa = folium.Map(location=[latitude_map, longitude_map], tiles="CartoDB positron", zoom_start=25)
            feature_group = folium.FeatureGroup("Locations")

            for coord in self.wp_entrada.itertuples():
                feature_group.add_child(folium.Marker(location=[coord[2],coord[3]],popup="Waypoint "+str(coord[1])))

            mapa.add_child(feature_group)

            mapa.save(data, close_file=False)
            self.ui.confmapa.setHtml(data.getvalue().decode())
            self.ui.confmapa.show()
        else:
            self.ui.confgenerarTrayectoria.setDisabled(True)

    def generarTrayectoriaConf(self):
        setattr(Axes3D,'arrow3D',self._arrow3D_1)
        ax = self.ui.conftrayectoriaplot.canvas
        consola = self.ui.confdescripcionTrayectoria
        self.altura_fachada = self.ui.confalturaSpinBox.value()
        self.generarTrayectoria(ax,consola)

    def generarTrayectoria(self, canvas, consola):
        self.wp_trayectoria = self.calcularTrayectoria(self.wp_entrada,consola)
        trayectoria_ydata = self.wp_trayectoria['latitude'].tolist()
        trayectoria_xdata = self.wp_trayectoria['longitude'].tolist()
        trayectoria_zdata = self.wp_trayectoria['altitude'].tolist()
        canvas.ax.cla()
        canvas.ax.scatter(trayectoria_xdata, trayectoria_ydata, trayectoria_zdata, s= 50, c='darkcyan',label = 'Wpt trayectoria', marker = 'd')
        canvas.ax.legend(loc='lower left', ncol=2, borderaxespad=0.)
        inicio = True
        for row in self.wp_trayectoria.itertuples():
            if inicio:
                row_inicio = row
                canvas.ax.text(row[3],row[2],row[4],'w'+str(row[1]), size= 10, zorder=10, color='navy')
                inicio = False
                continue
            canvas.ax.text(row[3],row[2],row[4],'w'+str(row[1]), size= 10, zorder=10, color='navy')
            dx,dy,dz= row[3]-row_inicio[3],row[2]-row_inicio[2],row[4]-row_inicio[4]
            canvas.ax.arrow3D(self,row_inicio[3],row_inicio[2],row_inicio[4],
                dx,dy,dz,
                mutation_scale=18,
                arrowstyle="-|>",
                linestyle='dashed',
                color = 'darkcyan')
            row_inicio = row

        canvas.ax.view_init(elev=20., azim= -135 )
        canvas.draw()
        distancia_trayectoria = self.longitudTrayectoria(self.wp_trayectoria)
        consola.append('\n'"Distancia estimada: "+str(distancia_trayectoria)[:7]+" m")
        corriente_empuje = 1000*self.UAV_Peso*self.UAV_Potencia_x_Kg/self.UAV_Voltaje_Bateria
        autonomia = (self.UAV_Capacidad_Bateria*self.UAV_Factor_Seguridad*60)/(corriente_empuje*1.5)
        tiempo_vuelo = distancia_trayectoria/(self.UAV_Velocidad_Crucero*60)
        factor_tiempo = tiempo_vuelo//autonomia
        consola.append("Tiempo estimado de vuelo: "+str(round(tiempo_vuelo))+" min")
        consola.append("Recambio de bateria: "+str(factor_tiempo)[:1])
        if(factor_tiempo>=1): self.cambio_bateria(factor_tiempo, canvas)
        
    def _arrow3D_1(self, ax, x, y, z, dx, dy, dz, *args, **kwargs):
        '''Add an 3d arrow to an `Axes3D` instance.'''

        arrow = Arrow3D(x, y, z, dx, dy, dz, *args, **kwargs)
        self.ui.conftrayectoriaplot.canvas.ax.add_artist(arrow)

    def _arrow3D_2(self, ax, x, y, z, dx, dy, dz, *args, **kwargs):
        '''Add an 3d arrow to an `Axes3D` instance.'''

        arrow = Arrow3D(x, y, z, dx, dy, dz, *args, **kwargs)      
        self.ui.ejecttrayectoriaPlot.canvas.ax.add_artist(arrow)
     
    def leerFicheroGPX (self,dir):
        df = pd.DataFrame(columns=['wpt','latitude','longitude','altitude'])
        tree = ET.parse(dir)
        root = tree.getroot()
        contador=1
        self.ui.confdescripcionWpText.setText("CARGANDO WAYPOINTS...")
        for elem in root:
            lat = elem.attrib['lat']
            data_lat = (float(lat.replace('"', '').replace(',', '')))
            lon = elem.attrib['lon']
            data_lon = (float(lon.replace('"', '').replace(',', '')))

            if (str(elem[0]).find('ele') != -1):
                elev = elem[0].text
                data_ele = (float(elev.replace('"', '').replace(',', '')))
            else:
                elev = elev
                data_ele = (float(elev.replace('"', '').replace(',', '')))
            df = df.append({'wpt': str(contador), 'latitude': data_lat, 'longitude': data_lon, 'altitude': data_ele},ignore_index=True)
            self.ui.confdescripcionWpText.append('Waypoint '+str(contador)+':      Latitud >'+ str(data_lat)[:10]+'        Longitud >'+str(data_lon)[:10]+'       Elevación >'+str(data_ele)[:5]+' m.')
            contador=contador+1
        return df

    def calcularTrayectoria(self, df_input, consola):
        df = pd.DataFrame(columns=['wpt','latitude','longitude','altitude'],)
        media_z = df_input.mean(axis=0)
        elevacion = self.altura_fachada
        contador = 1
        wp1 = df_input.iloc[0].tolist()
        wp2 = df_input.iloc[1].tolist()
        intercalar = False
        df = df.append({'wpt': 'Home', 'latitude': wp1[1], 'longitude': wp1[2], 'altitude': 0.0},ignore_index=True)
        consola.append("WAYPOINTS TRAYECTORIA:")
        while elevacion>5:
            if not intercalar:
                df = df.append({'wpt': contador, 'latitude': wp1[1], 'longitude': wp1[2], 'altitude': elevacion},ignore_index=True)
                df = df.append({'wpt': contador+1,'latitude': wp2[1], 'longitude': wp2[2], 'altitude': elevacion},ignore_index=True)
                intercalar = True
                consola.append('Waypoint '+str(contador)+':      Latitud >'+ str(wp1[1])[:10]+'        Longitud >'+str(wp1[2])[:10]+'       Altitud >'+str(elevacion)+' m.')
                consola.append('Waypoint '+str(contador+1)+':      Latitud >'+ str(wp2[1])[:10]+'        Longitud >'+str(wp2[2])[:10]+'       Altitud >'+str(elevacion)+' m.')
            
            else:
                df = df.append({'wpt': contador,'latitude': wp2[1], 'longitude': wp2[2], 'altitude': elevacion},ignore_index=True)
                df = df.append({'wpt': contador+1, 'latitude': wp1[1], 'longitude': wp1[2], 'altitude': elevacion},ignore_index=True)
                intercalar = False
                consola.append('Waypoint '+str(contador)+':      Latitud >'+ str(wp2[1])[:10]+'        Longitud >'+str(wp2[2])[:10]+'       Altitud >'+str(elevacion)+' m.')
                consola.append('Waypoint '+str(contador+1)+':      Latitud >'+ str(wp1[1])[:10]+'        Longitud >'+str(wp1[2])[:10]+'       Altitud >'+str(elevacion)+' m.')           
            elevacion = elevacion-self.distancia_wp
            contador = contador + 2

        return df

    def longitudTrayectoria(self,df):
        rows = df.get_values()
        row_1 = rows[0]
        rows = rows[1:]
        distancia,elevacion = 0,0
        for row in rows:
            distancia = geodesic((row[1],row[2]), (row_1[1],row_1[2])).m + distancia
            elevacion = elevacion + abs(row[3])
            row_1 = row
        recorrido = distancia + elevacion    
        return recorrido

    def cambio_bateria(self, segmentos, canvas):
        numero_wpt = int(self.wp_entrada['wpt'].max())
        recambio = int(round(numero_wpt/(segmentos + 1)))
        entrada_ydata = self.wp_entrada['latitude'].tolist()
        entrada_xdata = self.wp_entrada['longitude'].tolist()
        entrada_zdata = self.wp_entrada['altitude'].tolist()
        recambio_xdata = list()
        recambio_ydata = list()
        recambio_zdata = list()
        for row_index in range (recambio,numero_wpt-1,recambio):
            print(row_index)
            recambio_xdata.append(entrada_xdata[row_index])
            recambio_ydata.append(entrada_ydata[row_index])
            recambio_zdata.append(entrada_zdata[row_index]+1.5)
               
        canvas.ax.scatter(recambio_xdata, recambio_ydata, recambio_zdata, s= 150, c='yellow',label = 'Cambio Bateria', marker = 'o')
        canvas.ax.legend(loc='lower left', ncol=2, borderaxespad=0.)
        canvas.draw()

    def validacion_conf(self):
        validacion = QtGui.QRegExpValidator(QtCore.QRegExp(self.reg_exp_1))
        info_user_in = {self.ui.confnombreMision.text(), self.ui.confnombreUsuario.text(), self.ui.confnombreFachada.text(), self.ui.confdescripcion.text(), self.ui.confrefCamara.text()}
                
        for info_user in info_user_in:
            state = validacion.validate(info_user,0)[0]
            if(state == QtGui.QValidator.Acceptable):
                self.flag_validacion = True

        validacion = QtGui.QRegExpValidator(QtCore.QRegExp(self.reg_exp_2))
        info_user_in_correo = self.ui.confcorreoUsuario.text()
        state = validacion.validate(info_user_in_correo,0)[0]
        if(state == QtGui.QValidator.Acceptable):
           self.flag_validacion = True

        info_user_in_dp = self.ui.confcomboDepartamento.currentText()   
        info_user_in_mp = self.ui.confcomboMunicipio.currentText()
        if(info_user_in_mp != "Municipio"):
            self.flag_validacion = True

    def cargarConfiguracion(self):
        set_info_user = self.datos_obj
        if(self.flag_validacion):
            try:
                set_info_user.departamento_seleccionado = self.ui.confcomboDepartamento.currentText()
                set_info_user.municipio_municipio_seleccionado = self.ui.confcomboMunicipio.currentText()
                set_info_user.nombre_de_la_mision = self.ui.confnombreMision.text()
                set_info_user.nombre_de_usuario = self.ui.confnombreUsuario.text()
                set_info_user.correo_usuario = self.ui.confcorreoUsuario.text()
                set_info_user.nombre_de_la_fachada = self.ui.confnombreFachada.text()
                set_info_user.descripcion = self.ui.confdescripcion.text()
                set_info_user.nombre_de_usuario = self.ui.confnombreUsuario.text()
                set_info_user.nombre_de_la_mision = self.ui.confnombreMision.text()
                set_info_user.nombre_de_usuario = self.ui.confnombreUsuario.text()
                set_info_user.camara_id = self.ui.confrefCamara.text()
                set_info_user.camara_fx = self.ui.conffxSpinBox.text()
                set_info_user.camara_fy = self.ui.conffySpinBox.text()
                set_info_user.camara_cx = self.ui.confcxSpinBox.text()
                set_info_user.camara_cy = self.ui.confcySpinBox.text()
                set_info_user.camara_k1 = self.ui.confk1SpinBox.text()
                set_info_user.camara_k2 = self.ui.confk2SpinBox.text()
                set_info_user.camara_cv_h = self.ui.confcvHSpinBox.text()
                set_info_user.camara_cv_v = self.ui.confcvVSpinBox.text()

            except ValueError as e:
                self.dialog_conf_error()
                print(e)
            else:
                self.dialog_conf_done()
                #self.ros_node = rospy.init_node('dronfacade_node', anonymous=True)
                self.display_3()            
        else:
            self.dialog_conf_error()

    def dialog_conf_error(self):
        dlg = QtWidgets.QMessageBox()
        dlg.setText("Los datos_obj suministrados por el usuario son incorrectos.")
        dlg.setWindowTitle("Upss! Datos invalidos")
        pixmap = QtGui.QPixmap("Imagenes/PackIconos/ejecucion/ic_highlight_off.png")
        pixmap.setDevicePixelRatio(2.0)
        dlg.setIconPixmap(pixmap)
        pushButton = QtWidgets.QPushButton()
        dlg.setStyleSheet('background-color: rgb(255, 255, 255);')
        dlg.setDefaultButton(pushButton)
        returnValue = dlg.exec()

    def dialog_conf_done(self):
        dlg = QtWidgets.QMessageBox()
        dlg.setText("Datos cargados correctamente.")
        dlg.setWindowTitle("Yeah! Datos guardados")
        pixmap = QtGui.QPixmap("Imagenes/PackIconos/ejecucion/ic_launch.png")
        pixmap.setDevicePixelRatio(2.0)
        dlg.setIconPixmap(pixmap)
        pushButton = QtWidgets.QPushButton()
        dlg.setStyleSheet('background-color: rgb(255, 255, 255);')
        dlg.setDefaultButton(pushButton)
        returnValue = dlg.exec()        

    def chequeo_datos(self):
        sender = self.sender()

        validacion = QtGui.QRegExpValidator(QtCore.QRegExp(self.reg_exp_1))
        state = validacion.validate(sender.text(),0)[0]
        if state == QtGui.QValidator.Acceptable:
            color = '#000000'
        else:
            color = '#ED0C0C'
        sender.setStyleSheet('QLineEdit { color : %s }' % color)

    def chequeo_correo(self):
        sender = self.sender()
        validacion = QtGui.QRegExpValidator(QtCore.QRegExp(self.reg_exp_2))
        state = validacion.validate(sender.text().lower(),0)[0]
        if state == QtGui.QValidator.Acceptable:
            color = '#000000'
        else:
            color = '#ED0C0C'        
        sender.setStyleSheet('QLineEdit { color : %s }' % color)

    ################ EJECUCIÓN ################
    def capturar_wp(self):        
        if self.conexion_jetson:
            if not rospy.is_shutdown():
                
                status = True
                waypoint1 = MissionWaypoint()
                waypoint1.latitude = 3.4036057784757636
                waypoint1.longitude = -76.5488217339057
                waypoint1.altitude = 2
                waypoint2 = MissionWaypoint()
                waypoint2.latitude = 3.4031985991609472
                waypoint2.longitude = -76.54882609581352
                waypoint2.altitude = 2
                print(self.num_wp)
                if self.num_wp==0:
                    #####
                    #status, wp = self.MatriceSrv.getGPS()
                    if status:
                        ###
                        wp = waypoint1
                        self.wp_cap_1 = wp
                        self.num_wp = 1
                        self.ui.ejectConsola.append('WAYPOINTS ENTRADA:')
                        self.ui.ejectConsola.append('Waypoint 2:      Latitud >'+ str(wp.latitude)[:10]+'        Longitud >'+str(wp.longitude)[:10]+'       Elevación >'+str(wp.altitude)[:5]+' m.')
                    
                    else:
                        self.ui.ejectConsola.append('Fallo lectura GPS!')
                elif self.num_wp == 1:
                    #####
                    #status, wp = self.MatriceSrv.getGPS()
                    if status:
                        ###
                        wp = waypoint2
                        self.wp_cap_2 = wp
                        self.num_wp = 2
                        self.ui.ejectConsola.append('Waypoint 1:      Latitud >'+ str(wp.latitude)[:10]+'        Longitud >'+str(wp.longitude)[:10]+'       Elevación >'+str(wp.altitude)[:5]+' m.')                    
                        self.ui.ejectConsola.append('\n')

                        self.wp_entrada = []
                        self.wp_entrada = pd.DataFrame(columns=['wpt','latitude','longitude','altitude'],)
                        #self.ui.ejectConsola.append('WAYPOINTS ENTRADA:')
                        
                        
                        #####
                        wp = self.wp_cap_2
                        #wp = Waypoint1

                        self.wp_entrada= self.wp_entrada.append({'wpt': 2,'latitude': wp.latitude, 'longitude': wp.longitude, 'altitude': 2 },ignore_index=True)
                        #self.ui.ejectConsola.append('Waypoint 2:      Latitud >'+ str(wp.latitude)[:10]+'        Longitud >'+str(wp.longitude)[:10]+'       Elevación >'+str(wp.altitude)[:5]+' m.')
                        
                        #####
                        wp = self.wp_cap_1
                        #wp = waypoint2
                        self.wp_entrada= self.wp_entrada.append({'wpt': 1,'latitude': wp.latitude, 'longitude': wp.longitude, 'altitude': 2 },ignore_index=True)
                        #self.ui.ejectConsola.append('Waypoint 1:      Latitud >'+ str(wp.latitude)[:10]+'        Longitud >'+str(wp.longitude)[:10]+'       Elevación >'+str(wp.altitude)[:5]+' m.')                    
                        self.ui.ejectConsola.append('\n')
                        self.ui.ejectConsola.append('WAYPOINTS Listos!')
                        self.ui.ejectCapturarWP.setDisabled(True)
                        setattr(Axes3D,'arrow3D',self._arrow3D_2)
                        canvas = self.ui.ejecttrayectoriaPlot.canvas
                        consola = self.ui.ejectConsola
                        self.altura_fachada = 12
                        print(self.wp_entrada)
                        self.generarTrayectoria(canvas,consola)
                        
                    else:
                        self.ui.ejectConsola.append('Fallo lectura GPS!')
                    """                 else:
                    
                    self.wp_entrada = []
                    self.wp_entrada = pd.DataFrame(columns=['wpt','latitude','longitude','altitude'],)
                    #self.ui.ejectConsola.append('WAYPOINTS ENTRADA:')
                    wp = self.wp_cap_2                    
                    self.wp_entrada= self.wp_entrada.append({'wpt': self.num_wp,'latitude': wp.latitude, 'longitude': wp.longitude, 'altitude': wp.altitude },ignore_index=True)
                    #self.ui.ejectConsola.append('Waypoint 2:      Latitud >'+ str(wp.latitude)[:10]+'        Longitud >'+str(wp.longitude)[:10]+'       Elevación >'+str(wp.altitude)[:5]+' m.')
                    wp = self.wp_cap_1
                    self.wp_entrada= self.wp_entrada.append({'wpt': self.num_wp,'latitude': wp.latitude, 'longitude': wp.longitude, 'altitude': wp.altitude },ignore_index=True)
                    #self.ui.ejectConsola.append('Waypoint 1:      Latitud >'+ str(wp.latitude)[:10]+'        Longitud >'+str(wp.longitude)[:10]+'       Elevación >'+str(wp.altitude)[:5]+' m.')                    
                    self.ui.ejectConsola.append('\n')
                    self.ui.ejectConsola.append('WAYPOINTS Listos!')
                    self.ui.ejectCapturarWP.setDisabled(True)
                    setattr(Axes3D,'arrow3D',self._arrow3D_2)
                    canvas = self.ui.ejecttrayectoriaPlot.canvas
                    consola = self.ui.ejectConsola
                    self.altura_fachada = 12
                    print(self.wp_entrada)
                    self.generarTrayectoria(canvas,consola) """

    def iniciarMision(self):
        if self.conexion_jetson:
            """ self.JetsonSSH.connect('10.42.0.227', username='jetsonnano', password='Jetson3744')
            stdin, stdout, stderr = self.JetsonSSH.exec_command('nohup python3 ZED.py &\necho $!')
            for line in stdout:
                self.cameraPID = line
                break
            self.JetsonSSH.close() """
            if not rospy.is_shutdown():
                if not self.mision_iniciada:
                    self.MatriceSrv.waypoint_mission(self.wp_trayectoria)
                    status = self.MatriceSrv.uploadMission()
                    if status:
                        status1 = self.MatriceSrv.getSDKControl()
                        status2 = self.MatriceSrv.setLocalPosition()
                        
                        if status1 and status2==True:
                            try:
                                sub = rospy.Subscriber('dji_sdk/gps_health', UInt8, self._gpsCB)  
                            except rospy.ServiceException as e:
                                print("Failed to subscribe GPS health: %s"%e)
                            
                            status = self.MatriceSrv.startMission()
                            if status==True:
                                self.ui.ejectConsola.append('\n')
                                self.ui.ejectConsola.append("Misión Iniciada!")
                                self.ui.ejectplayButton.setDisabled(True)
                                self.ui.ejectpausaButton.setEnabled(True)
                                self.ui.ejectstopButton.setEnabled(True)
                                self.mision_iniciada = True
                                try:
                                    sub_2 = rospy.Subscriber('/dji_sdk/flight_status', UInt8, self._flightCB)
                                except rospy.SubscriberExeption as e:
                                    print("Failed to subscribe GPS position: %s"%e)
                            else:
                                self.ui.ejectConsola.append('\n')
                                self.ui.ejectConsola.append("No se pudo iniciar!")
                                self.ui.ejectConsola.append("error: "+str(status))
                        else:

                            self.ui.ejectConsola.append('\n')
                            self.ui.ejectConsola.append("Nodo no disponible!")
                            self.ui.ejectConsola.append("error: " +str(status1))
                    else:

                        self.ui.ejectConsola.append('\n')
                        self.ui.ejectConsola.append("No se pudo cargar la misión!")
                        self.ui.ejectConsola.append("error: " +str(status))
                else:
                    status = self.MatriceSrv.resumeMission()
                    if status:
                        self.ui.ejectConsola.append('\n')
                        self.ui.ejectConsola.append("Misión resumida!")
                    else:    
                        self.ui.ejectConsola.append("error: " +str(status))

    def _gpsCB(self, data):
        gps_health = data.data
        if gps_health < 3:
            self.detenerMision()
    
    def _flightCB(self,data):
        flight_status = data.data
        if flight_status==1:
            self.ui.ejectstatus.setStyleSheet('background-color: rgb(73, 255, 51);')
            self.ui.ejectstatus.setText("EN TIERRA")
        if flight_status==3:
            self.ui.ejectstatus.setStyleSheet('background-color: rgb(10, 87, 198);')
            self.ui.ejectstatus.setText("TAKEOFF")
        if flight_status==4:
            self.ui.ejectstatus.setStyleSheet('background-color: rgb(247, 138, 16);')
            self.ui.ejectstatus.setText("LANDING")
        if flight_status==5:
            self.ui.ejectstatus.setStyleSheet('background-color: rgb(247, 240, 16);')
            self.ui.ejectstatus.setText("LANDIG FINISH")
           
    def pausarMision(self):
        if self.mision_iniciada:
            if self.conexion_jetson:
                if not rospy.is_shutdown():
                    status = self.MatriceSrv.pauseMission()
                    if status:
                        self.ui.ejectConsola.append('\n')
                        self.ui.ejectConsola.append("Misión pausada!")
                        self.ui.ejectplayButton.setEnabled(True)
                        self.ui.ejectplayButton.setText('Resumen')
                        self.ui.ejectpausaButton.setDisabled(True)
                    else:
                        print(status)
                       
    def detenerMision(self):
        if self.conexion_jetson:
            """             self.JetsonSSH.connect('10.42.0.227', username='jetsonnano', password='Jetson3744')
            stdin, stdout, stderr = self.JetsonSSH.exec_command('kill '+str(self.cameraPID))

            self.JetsonSSH.close() """
            if not rospy.is_shutdown():
                status = self.MatriceSrv.stopMission()
                if status:
                    self.ui.ejectConsola.append('\n')
                    self.ui.ejectConsola.append("Misión detenida!")
                    self.ui.ejectpausaButton.setDisabled(True)
                    self.ui.ejectstopButton.setDisabled(True)
                    self.ui.ejectplayButton.setText('Iniciar')
                    self.ui.ejectplayButton.setEnabled(True)
                    self.mision_iniciada = False
                else:
                    print(status)

    ################ PROCESAMIENTO ################
    def procOpenDirectorio(self):
        filename = QtWidgets.QFileDialog.getExistingDirectory()
        if filename.isalpha:
            self.ui.procRutaRegistro.setText(filename)
            self.procCargarImagenes(filename)
        
    def procCargarImagenes(self, directorioImagenes):
        self.imagenes_entrada = []
        self.imagen_entrada_index = 0
        imagePaths = sorted(list(paths.list_images(directorioImagenes)))
        self.directorioImagenes=directorioImagenes
        i=0 
        for imagePath in imagePaths:
            image_input = cv2.imread(imagePath, cv2.IMREAD_COLOR)
            image = cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB)
            i = i+1
            self.imagenes_entrada.append(image_input)
        
        self.alto_img_in,  self.ancho_img_in, self.canales_img_in = image.shape  
        self.numero_imagenes = i
        self.ui.procImageSize.setText(str(self.alto_img_in) +"x"+ str(self.ancho_img_in))
        self.visualizarImagenesEntrada()

    def visualizarImagenesEntrada(self):
        self.p1_inputView.clear()
        image_view = pg.ImageItem()
        self.p1_inputView.addItem(image_view)
        image_view.setImage(cv2.cvtColor(self.imagenes_entrada[self.imagen_entrada_index],cv2.COLOR_BGR2RGB))
        image_size = self.imagenes_entrada[self.imagen_entrada_index].shape
        image_view.translate(0,image_size[0])
        image_view.rotate(270)
        self.ui.procNumeroImg.setText(str(self.imagen_entrada_index+1)+"/"+str(self.numero_imagenes))
        self.p1_inputView.autoRange()
    
    def previewSig(self):
        if(self.imagen_entrada_index<self.numero_imagenes-1):
            self.imagen_entrada_index=self.imagen_entrada_index+1
            self.visualizarImagenesEntrada()

    def previewPrev(self):
        if(self.imagen_entrada_index>0):
            self.imagen_entrada_index=self.imagen_entrada_index-1
            self.visualizarImagenesEntrada()      

    def stitching(self):
        # initialize OpenCV's image sticher object and then perform the image
        # stitching
        #self.textBrowser.append('[INFO] stitching Images')
        print("[INFO] stitching images...")
        stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
        (status, stitched) = stitcher.stitch(self.imagenes_entrada)

        # if the status is '0', then OpenCV successfully performed image
        # stitching
        if status == 0:
            # check to see if we supposed to crop out the largest rectangular
            # region from the stitched image
            if self.ui.procRecortarImage.isChecked():
                # create a 10 pixel border surrounding the stitched image
                #self.textBrowser.append('[INFO] Recortando')
                #self.textBrowser.setText('[INFO] Recortando...')
                print("[INFO] cropping...")
                stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10,
                    cv2.BORDER_CONSTANT, (0, 0, 0))

                # convert the stitched image to grayscale and threshold it
                # such that all pixels greater than zero are set to 255
                # (foreground) while all others remain 0 (background)
                gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
                thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

                # find all external contours in the threshold image then find
                # the *largest* contour which will be the contour/outline of
                # the stitched image
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                c = max(cnts, key=cv2.contourArea)

                # allocate memory for the mask which will contain the
                # rectangular bounding box of the stitched image region
                mask = np.zeros(thresh.shape, dtype="uint8")
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

                # create two copies of the mask: one to serve as our actual
                # minimum rectangular region and another to serve as a counter
                # for how many pixels need to be removed to form the minimum
                # rectangular region
                minRect = mask.copy()
                sub = mask.copy()

                # keep looping until there are no non-zero pixels left in the
                # subtracted image
                while cv2.countNonZero(sub) > 0:
                    # erode the minimum rectangular mask and then subtract
                    # the thresholded image from the minimum rectangular mask
                    # so we can count if there are any non-zero pixels left
                    minRect = cv2.erode(minRect, None)
                    sub = cv2.subtract(minRect, thresh)

                # find contours in the minimum rectangular mask and then
                # extract the bounding box (x, y)-coordinates
                cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                c = max(cnts, key=cv2.contourArea)
                (x, y, w, h) = cv2.boundingRect(c)

                # use the bounding box coordinates to extract the our final
                # stitched image
                stitched = stitched[y:y + h, x:x + w]
            
            # write the output stitched image to disk
            
            if self.ui.procResizeOutput.isChecked():

                # M = cv2.getRotationMatrix2D((width/2,height/2),90,1)
                # stitched = cv2.warpAffine(stitched,M,(width,height))
                
                stitched = cv2.rotate(stitched, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # cv2.imshow("estaes",stitched)
            cv2.imwrite("/home/mateo/Escritorio/Universidad/TG/TG_DroneFacade/GUI_V1/Salida/Output.png", stitched)

            # display the output stitched image to our screen
            #stitched = cv2.cvtColor(stitched, cv2.COLOR_BGR2RGB)
            
            # cv2.imshow("estanoes",stitched)
            height, width, channel = stitched.shape
            step = channel * width
            self.image_out_size = stitched.shape
            self.visualizarImageOut(stitched)
            #qImg = QImage(stitched.data, width, height, step, QImage.Format_RGB888)
            #self.imagelabel.setPixmap(QPixmap.fromImage(qImg))
            # cv2.imshow("Stitched", stitched)
            # cv2.waitKey(0)

            # otherwise the stitching failed, likely due to not enough keypoints)
            # being 
            #self.textBrowser.setText('[INFO] Stitching finalizado')
            print("termino")
            #self.timer_process.stop()
        else:
            #self.textBrowser.setText("[INFO] image stitching failed ({})".format(status))
            print("[INFO] image stitching failed ({})".format(status))

    def visualizarImageOut(self, image_out):
        self.p1_imageView.clear()
        self.image_out_size = image_out.shape
        self.image_out = cv2.cvtColor(image_out, cv2.COLOR_BGR2RGB)
        self.image_view = pg.ImageItem(autoScale= False,autoRange=False)
        self.p1_imageView.addItem(self.image_view)
        self.image_view.setImage(self.image_out, autoScale=False)
        self.image_view.translate(0,self.image_out_size[0])
        self.image_view.rotate(270)
        self.p1_imageView.autoRange(False)

    def interaccion(self):
        if(self.ui.procHabilitarInteraccion.isChecked()):
            self.p1_imageView.vb.setMouseEnabled(y=True,x=True)
        else:
            self.p1_imageView.vb.setMouseEnabled(y=False,x=False)
            self.p1_imageView.autoRange()

    def actualizarROI(self):
        self.p2_imageView.clear()
        seleccion = self.roi.getArrayRegion(self.image_out,self.image_view)
        imagen = pg.ImageItem()
        imagen.setImage(seleccion)
        self.p2_imageView.addItem(imagen)
        self.p2_imageView.autoRange()
            
    def mostarEjes(self):
        if(self.ui.procMostrarEjes.isChecked()):
            self.p1_imageView.showAxis('left')
            self.p1_imageView.showAxis('bottom')
            self.p2_imageView.showAxis('left')
            self.p2_imageView.showAxis('bottom')
        else:
            self.p1_imageView.hideAxis('left')
            self.p1_imageView.hideAxis('bottom')
            self.p2_imageView.hideAxis('left')
            self.p2_imageView.hideAxis('bottom')

    def regionInteres(self):
        index = self.ui.procRegionInteres.isChecked()
        if(index):
            self.p1_imageView.addItem(self.roi)
            self.ui.procimageView.addItem(self.p2_imageView)
            seleccion = self.roi.getArrayRegion(self.image_out,self.image_view)
            imagen = pg.ImageItem()
            imagen.setImage(seleccion)
            self.p2_imageView.addItem(imagen)
            self.p2_imageView.autoRange()
        else:
            self.p1_imageView.removeItem(self.roi)
            self.ui.procimageView.removeItem(self.p2_imageView)

    def keyPressEvent(self, e):

        if e.key() == QtCore.Qt.Key_Escape:

            self.close()


class Arrow3D(FancyArrowPatch):
    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0,0), (0,0), *args, **kwargs)
        self._xyz = (x,y,z)
        self._dxdydz = (dx,dy,dz)

    def draw(self, renderer):
        x1,y1,z1 = self._xyz
        dx,dy,dz = self._dxdydz
        x2,y2,z2 = (x1+dx,y1+dy,z1+dz)

        xs, ys, zs = proj_transform((x1,x2),(y1,y2),(z1,z2), renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        super().draw(renderer)

class CustomDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("hello")


app = QtWidgets.QApplication([])
pixmap = QtGui.QPixmap("Imagenes/dron_facade_splash.png")
splash = QtWidgets.QSplashScreen(pixmap)
splash.show()

application = mywindow()
app.processEvents()
""" time.sleep(1)
splash.showMessage("Cargando modulos")
time.sleep(2)
splash.finish(application) """
application.showMaximized()
sys.exit(app.exec())