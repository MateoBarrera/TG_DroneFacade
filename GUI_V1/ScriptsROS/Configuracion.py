import numpy as np
import cv2
import os
import time
from tkinter import *
from tkinter import filedialog
from imutils import paths
from operator import itemgetter, attrgetter
class Configuracion():

    def __init__(self):
        
        pass
    
    def cargar_imagenes(self):
        """Cargar path de imagenes

        Parameters
        ----------
        None
        Returns
        -------
        Path Images Folder

        """
        root = Tk()
        root.withdraw()
        root.folder_name =  filedialog.askdirectory(title = 'Choose the directory of the input files')
        
        if (root.folder_name):

            list_images  = list(paths.list_images(root.folder_name))
            ##Organizar paths dependiendo nomenclatura zed u other
            z = re.split('.jpg',list_images[0])
            w = re.split('(zedCamera)',z[0])
            
            if (len(w)==1):

                allImagePaths = sorted(list_images)
            
            else:
                allImagePaths = sorted(list_images,key=self.sort_espf)
                


            
            
        else:

            allImagePaths = []
            
        root.destroy()
    
        
        return allImagePaths
        
    def sort_espf(self,xs):
        #Organiza los paths de menor a mayor por este criterio:
        z = re.split('.jpg',xs)
        xs= re.split('zedCamera',z[0])
        xs = int(xs[1])

        return xs
    
    def cargar_video(self):
        """Cargar path de video

        Parameters
        ----------
        None
        Returns
        -------
        Path Video folder

        """
        root = Tk()
        root.withdraw()
        #initialdir = "/",
        root.video_name =  filedialog.askopenfilename(title = "Select file",filetypes = (("avi files",".avi"),("mp4 files",".mp4")))
        return root.video_name

    def calibracion(self,I,fxL,fyL,cxL,cyL,k1_L,k2_L,fxR,fyR,cxR,cyR,k1_R,k2_R):
        """Calibra la camara izquierda y derecha

        Parameters
        ----------
        I:  Image \n
            Imagen a desempeñar la calibración
        fx:  float \n
            Distancia focal X
        fy:  float \n
            Distancia focal Y
        Cx:  float \n
            Coordenada punto principal X 
        Cy  float \n
            Coordenada punto principal Y
        k1  float \n
            factor de distorsión k1
        k2  float \n
            factor de distorsion k2
       
        Returns
        -------
        I_calibrated: array-like
            Calibrated image

        """
        #Image information 
        height, width, channels = I.shape

        #Crop image on left and right camera
        left=I [0:height,0:int(width/2)]
        right= I[0:height,int(width/2):(width)]

        #Arranges the parameters of the left camera matrix and the coefficient vector
        mtx = np.array ([[float(fxL), 0, float(cxL)],[0, float(fyL), float(cyL)],[0,  0, 1]])
        coef_distorsionLeft = np.array([[float(k1_L),float(k2_L),0,0]])
        
        #Arranges the parameters of the right camera matrix and the coefficient vector
        mty = np.array ([[float(fxR), 0, float(cxR)],[0, float(fyR), float(cyR)],[0,  0, 1]])
        coef_distorsionRight = np.array([[float(k1_R),float(k2_R),0,0]])

        #Rectify the left and right camera images
        leftCam = cv2.undistort(left, mtx, coef_distorsionLeft, None, None)
        RightCam = cv2.undistort(right, mty, coef_distorsionRight, None, None)

        #stack the two images 
        img_stacked = np.hstack((leftCam,RightCam))

        return img_stacked
    
    def calibrate(self,I,fxL,fyL,cxL,cyL,k1_L,k2_L,fxR,fyR,cxR,cyR,k1_R,k2_R,TY,TZ,Baseline,CV,RX,RZ):
        """Calibracion stereo

        Parameters
        ----------
        I:  Image \n
            Imagen a desempeñar la calibración
        fx:  float \n
            Distancia focal X
        fy:  float \n
            Distancia focal Y
        Cx:  float \n
            Coordenada punto principal X 
        Cy  float \n
            Coordenada punto principal Y
        k1  float \n
            factor de distorsión k1
        k2  float \n
            factor de distorsion k2
       
        Returns
        -------
        I_calibrated: array-like
            Calibrated image

        """
        #Image information 
        height, width, channels = I.shape

        #Crop image on left and right camera
        left=I [0:height,0:int(width/2)]
        right= I[0:height,int(width/2):(width)]

        width = int(width/2)
        height = int(height) 
        #Arranges the parameters of the left camera matrix and the coefficient vector
        cameraMatrix_left= np.array ([[float(fxL), 0, float(cxL)],[0, float(fyL), float(cyL)],[0,  0, 1]])
        coef_distorsion_left = np.array([[float(k1_L),float(k2_L),0,0]])
        
        #Arranges the parameters of the right camera matrix and the coefficient vector
        cameraMatrix_right = np.array ([[float(fxR), 0, float(cxR)],[0, float(fyR), float(cyR)],[0,  0, 1]])
        coef_distorsion_right = np.array([[float(k1_R),float(k2_R),0,0]])
        T_ = np.array([-float(Baseline),float(TY), float(TZ)])

        R_zed = np.array([float(RX), float(CV), float(RZ)])
        
        #Rodrigues conversion
        R, _ = cv2.Rodrigues(R_zed)
        T = np.array([[T_[0]], [T_[1]], [T_[2]]])
        R1 = R2 = P1 = P2 = np.array([])
        
        R1, R2, P1, P2 = cv2.stereoRectify(cameraMatrix1=cameraMatrix_left,
                                       cameraMatrix2=cameraMatrix_right,
                                       distCoeffs1=coef_distorsion_left,
                                       distCoeffs2=coef_distorsion_right,
                                       R=R, T=T,
                                       flags=cv2.CALIB_ZERO_DISPARITY,
                                       alpha=0,
                                       imageSize=(width, height),
                                       newImageSize=(width, height))[0:4]

        map_left_x, map_left_y = cv2.initUndistortRectifyMap(cameraMatrix_left, coef_distorsion_left , R1, P1, (width, height), cv2.CV_32FC1)
        map_right_x, map_right_y = cv2.initUndistortRectifyMap(cameraMatrix_right, coef_distorsion_right, R2, P2, (width, height), cv2.CV_32FC1)
        cameraMatrix_left = P1
        cameraMatrix_right = P2
        left_rect = cv2.remap(left, map_left_x, map_left_y, interpolation=cv2.INTER_LINEAR)
        right_rect = cv2.remap(right, map_right_x, map_right_y, interpolation=cv2.INTER_LINEAR)
        img_stacked = np.hstack((left_rect,right_rect))
        
        return img_stacked
    
    
        
    

    



