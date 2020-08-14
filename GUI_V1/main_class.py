#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from PyQt5.QtGui import QApplication, QMainWindow
import matplotlib.pyplot as plt
import pandas as pd
import xml.etree.ElementTree as ET
import math

import sys
import re
import pyqtgraph as pg
import numpy as np
import cv2
import imutils
from imutils import paths
from pyqtgraph import PlotWidget, plot
from ClassDatos import mainDatos
from PyQt5 import QtWidgets, QtGui, QtCore 
from ClassWindow1 import Ui_DroneFacade
import time

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.datos = mainDatos()
        self.ui = Ui_DroneFacade()
        self.ui.setupUi(self)
        info_configuracion = mainDatos()
        self.calibracionCamara = (info_configuracion.camara_id, info_configuracion.camara_fx, info_configuracion.camara_fy, info_configuracion.camara_cx, 
            info_configuracion.camara_cy, info_configuracion.camara_k1, info_configuracion.camara_k2, info_configuracion.camara_cv_h, info_configuracion.camara_cv_v)
        self.parametrosCamara()
        self.departamento = self.datos.departamento


        #Display buttons
        self.ui.inicioButton.clicked.connect(self.display_1)
        self.ui.configuracionButton.clicked.connect(self.display_2)
        self.ui.procesamientoButton.clicked.connect(self.display_4)
        self.ui.resultadosButton.clicked.connect(self.display_5)

        #Ventana de Configuración
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

        self.hour = [1,2,3,4,5,6,7,8,9,10]    
        self.temperature = [30,32,34,32,33,31,29,32,35,45]
        self.wp_entrada = []
        self.ui.confimportarWaypoints.clicked.connect(self.confOpenFile)
        self.ui.conftrayectoriaplot.canvas.ax.set_facecolor('#faf9fa')
        self.ui.conftrayectoriaplot.canvas.ax.mouse_init(rotate_btn=1, zoom_btn=3)
        #self.ui.conftrayectoriaplot.canvas.draw()


        self.flag_validacion = False
        self.reg_exp_1 = "^[a-z-A-Z_0-9áéíóúñÑ]+|([a-z-A-Z_0-9áéíóúñÑ]+\s[a-z-A-Z_0-9áéíóúñÑ]+)+"
        self.reg_exp_2 = '^[(a-z0-9.)]+@[(a-z0-9)]+\.[(a-z)]{2,15}$'
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
        self.ui.ejectGraficaTelemetria.setBackground(background='#ffffff')
        self.p1_telemetria = self.ui.ejectGraficaTelemetria.addPlot()
        self.p1_telemetria.setTitle('Captura de telemetría')
        self.p1_telemetria.setLabel('left','Magnitud', units='?')
        self.p1_telemetria.setLabel('bottom', 'Muestra', units='n')
        self.ui.ejecucionButton.clicked.connect(self.cargarConfiguracion)
        self.ui.ejecttrayectoriaPlot.setBackground(background='#faf9fa')


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
        self.ui.procimageView.nextRow()
        self.p2_imageView = self.ui.procimageView.addPlot(colspan=2)
        self.p2_imageView.vb.setMouseEnabled(y=False,x=False)
        self.p2_imageView.hideAxis('left')
        self.p2_imageView.hideAxis('bottom')
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



    def plot(self):
        self.ui.confplot.plot(self.hour,self.temperature)


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

    def display_4(self):
        self.ui.area1.setCurrentIndex(3)
        self.ui.ejecucionLabel.setDisabled(True)
        self.ui.procesamientoLabel.setEnabled(True)
               
    def display_5(self):
        self.ui.area1.setCurrentIndex(4)
        self.ui.procesamientoLabel.setDisabled(True)
        self.ui.resultadosLabel.setEnabled(True)


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
        self.datos.buscarMunicipios(dep)
        for index in range (len(self.datos.municipios)):
            self.ui.confcomboMunicipio.addItem(self.datos.municipios[index])

    def confOpenFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Cargar Waypoints', '/home', filter="gpx(*.gpx)")
        if filename[0]:
            self.ui.confrutaWaypoints.setText(filename[0])
            self.wp_entrada = self.leerFicheroGPX(filename[0])
            ydata = self.wp_entrada['lat'].tolist()
            xdata = self.wp_entrada['lon'].tolist()
            zdata = self.wp_entrada['ele'].tolist()
            media_z = self.wp_entrada.mean(axis=0)
            media_z = media_z['ele']
            
            self.ui.conftrayectoriaplot.canvas.ax.set_zlim(media_z*0.9,media_z*1.1)
            azim_componentes=((ydata[-1]-ydata[0])/(xdata[-1]-xdata[0]))
            azim = (math.atan(azim_componentes)*math.pi/180)
            self.ui.conftrayectoriaplot.canvas.ax.view_init(elev=20., azim=azim+45)

            self.ui.conftrayectoriaplot.canvas.ax.scatter(xdata, ydata, zdata)
            self.ui.conftrayectoriaplot.canvas.ax.hold(True)
            self.ui.conftrayectoriaplot.canvas.ax.Patch3D( zs=980, zdir='z')
            self.ui.conftrayectoriaplot.canvas.draw()


    def leerFicheroGPX (self,dir):
        df = pd.DataFrame(columns=['wpt','lat','lon','ele'])
        tree = ET.parse(dir)
        root = tree.getroot()
        i=1
        self.ui.confdescripcionWpText.setText("CARGANDO WAYPOINTS...")
        
        for elem in root:

            lat = elem.attrib['lat']
            data_lat = (float(lat.replace('"', '').replace(',', '')))
            lon = elem.attrib['lon']
            data_lon = (float(lon.replace('"', '').replace(',', '')))

            if (str(elem[0]).find('ele') != -1):
                elev = elem[0].text
                data_eve = (float(elev.replace('"', '').replace(',', '')))
            else:
                elev = elev
                data_eve = (float(elev.replace('"', '').replace(',', '')))
            df = df.append({'wpt': str(i), 'lat': data_lat, 'lon': data_lon, 'ele': data_eve},ignore_index=True)
            self.ui.confdescripcionWpText.append('Waypoint '+str(i)+':      Latitud >'+ str(data_lat)[:10]+'        Longitud >'+str(data_lon)[:10]+'       Elevación >'+str(data_eve)[:5]+' m.')
            i=i+1
        return df
    
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
        set_info_user = mainDatos()
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
                self.display_3()            
        else:
            self.dialog_conf_error()

    def dialog_conf_error(self):
        dlg = QtWidgets.QMessageBox()
        dlg.setText("Los datos suministrados por el usuario son incorrectos.")
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

    ################ PROCESAMIENTO ################
    def procOpenDirectorio(self):
        filename = QtWidgets.QFileDialog.getExistingDirectory()
        if filename.isalpha:
            self.ui.procRutaRegistro.setText(filename)
            self.procCargarImagenes(filename)
        
    def procCargarImagenes(self, directorioImagenes):
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
        self.image_view = pg.ImageItem()
        self.p1_imageView.addItem(self.image_view)
        self.image_view.setImage(self.image_out)
        self.image_view.translate(0,self.image_out_size[0])
        self.image_view.rotate(270)
        self.p1_imageView.autoRange()

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