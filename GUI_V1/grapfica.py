from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d, Axes3D
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET

def leerFicheroGPX (dir):
    df = pd.DataFrame(columns=['wpt','lat','lon','ele'])
    df['lat'] = df['lat'].astype(np.float64)
    tree = ET.parse(dir)
    root = tree.getroot()
    i=1
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
        i=i+1
    return df




# f es la variable que contiene la ruta a nuestro fichero .gpx
f = "/home/mateo/Escritorio/Universidad/TG/TG_DroneFacade/GUI_V1/Coordenadas.gpx"
coorDF = leerFicheroGPX(f)
TrayectoriaDF = coorDF
#print(coorDF.to_string())
i = 0
for row in TrayectoriaDF:
    print(TrayectoriaDF['lon'][i])

ydata = coorDF['lat'].tolist()
xdata = coorDF['lon'].tolist()
zdata = coorDF['ele'].tolist()
media_z = coorDF.mean(axis=0)
media_z = media_z['ele']
fig = plt.figure()
ax = Axes3D(fig)
print(int(ydata[0])-1,int(ydata[0])+1)
yy, xx = np.meshgrid(range(int(ydata[0])-1,int(ydata[0])+1), range(int(xdata[0])-1,int(xdata[0])+1))
zz = yy*0


ax.scatter(xdata, ydata, zdata)
#ax.
#ax.set_xlim(left=, right=, emit=True, auto=False, **kw)
ax.set_autoscale_on(True)
ax.set_zlim(media_z*0.9,media_z*1.1)

ax.plot_surface(xx, yy, zz+media_z,color='#0C9F21')

azim_componentes=((ydata[-1]-ydata[0])/(xdata[-1]-xdata[0]))
azim = (math.atan(azim_componentes)*math.pi/180)
ax.view_init(elev=20., azim=azim+45)
ax.set_title("Trayectoria", fontdict=None, loc='center')
""" ax.zaxis.set_major_locator(plt.LinearLocator(10))
ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.02f')) """
#plt.show()



 
