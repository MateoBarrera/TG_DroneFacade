#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from PyQt5.QtGui import QApplication, QMainWindow
import sys
import re
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from ClassDatos import mainDatos
from PyQt5 import QtWidgets, QtGui, QtCore 
from ClassWindow1 import Ui_MainWindow

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.datos = mainDatos()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        info_configuracion = mainDatos()
        self.calibracionCamara = (info_configuracion.camara_id, info_configuracion.camara_fx, info_configuracion.camara_fy, info_configuracion.camara_cx, 
            info_configuracion.camara_cy, info_configuracion.camara_k1, info_configuracion.camara_k2, info_configuracion.camara_cv_h, info_configuracion.camara_cv_v)
        self.parametrosCamara()
        self.departamento = self.datos.departamento


        #Display buttons
        self.ui.inicioButton.clicked.connect(self.display_1) # connecting the clicked signal with display slot
        self.ui.configuracionButton.clicked.connect(self.display_2)
        self.ui.ejecucionButton.clicked.connect(self.display_3)
        self.ui.procesamientoButton.clicked.connect(self.display_4)
        self.ui.resultadosButton.clicked.connect(self.display_5)
        self.ui.configuracionLabel.setDisabled(True)
        #self.ui.ejecucionLabel.setDisabled(True)
        #self.ui.procesamientoLabel.setDisabled(True)
        #self.ui.resultadosLabel.setDisabled(True)
        #self.ui.confplot.pg.setConfigOption('background', 'w')
        #selpg.setConfigOption('foreground', 'k')

        #Ventana de Configuración
        self.ui.confmodoCamararadioButton.clicked.connect(self.parametrosCamara)
        self.ui.conffxSpinBox.setDisabled(True)
        self.ui.conffySpinBox.setDisabled(True)
        self.ui.confcxSpinBox.setDisabled(True)
        self.ui.confcySpinBox.setDisabled(True)
        self.ui.confk1SpinBox.setDisabled(True)
        self.ui.confk2SpinBox.setDisabled(True)

        for index in range (len(self.departamento)):
            self.ui.confcomboDepartamento.addItem(self.departamento[index])
        self.ui.confcomboDepartamento.currentIndexChanged.connect(self.comboMunicipios)

        self.hour = [1,2,3,4,5,6,7,8,9,10]    
        self.temperature = [30,32,34,32,33,31,29,32,35,45]
        #self.ui.confcalcularDistancia.clicked.connect(self.plot)
        self.ui.confimportarWaypoints.clicked.connect(self.openFile)

        self.flag_validacion = (False, False, False)
        self.ui.confnombreMision.textChanged.connect(self.chequeo_datos)
        self.ui.confnombreUsuario.textChanged.connect(self.chequeo_datos)
        self.ui.confnombreFachada.textChanged.connect(self.chequeo_datos)
        self.ui.confdescripcion.textChanged.connect(self.chequeo_datos)
        self.ui.confcorreoUsuario.textChanged.connect(self.chequeo_correo)
        self.ui.ejecucionButton.clicked.connect(self.cargarConfiguracion)

    def plot(self):
        self.ui.confplot.plot(self.hour,self.temperature)


    def display_1(self):
        self.ui.area1.setCurrentIndex(0)
        self.ui.resultadosLabel.setDisabled(True)
        self.ui.inicioLabel.setEnabled(True)
        
    def display_2(self):
        self.ui.area1.setCurrentIndex(1) 
        self.ui.inicioLabel.setDisabled(True)
        self.ui.configuracionLabel.setEnabled(True)
      
    def display_3(self):
        if(self.flag_validacion):
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

    def openFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '/home')
        if filename[0]:
            f = open(filename[0],'r')
            self.ui.confrutaWaypoints.setText(filename[0])

            with f:
                data = f.read()
                #self.
    
    def cargarConfiguracion(self):
        set_info_user = mainDatos()
        
        if(self.flag_validacion):
            print("usado")
        else:
            print("error")

    def chequeo_datos(self):
        sender = self.sender()
        validacion = QtGui.QRegExpValidator(QtCore.QRegExp("^[a-z-A-Z_0-9]+|([a-z-A-Z_0-9ñÑ]+\s[a-z-A-Z_0-9ñÑ]+)+"))
        state = validacion.validate(sender.text(),0)[0]
        if state == QtGui.QValidator.Acceptable:
            color = '#000000'
            
            flag = True
        else:
            color = '#ED0C0C'
            flag = False

        sender.setStyleSheet('QLineEdit { color : %s }' % color)


    def chequeo_correo(self):
        sender = self.sender()
        validacion = QtGui.QRegExpValidator(QtCore.QRegExp('^[(a-z0-9.)]+@[(a-z0-9)]+\.[(a-z)]{2,15}$'))
        state = validacion.validate(sender.text().lower(),0)[0]
        if state == QtGui.QValidator.Acceptable:
            color = '#000000'
            ##self.flag_validacion = True
        else:
            color = '#ED0C0C'
            ##self.flag_validacion = False
        
        sender.setStyleSheet('QLineEdit { color : %s }' % color)

    def keyPressEvent(self, e):

        if e.key() == QtCore.Qt.Key_Escape:

            self.close()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())