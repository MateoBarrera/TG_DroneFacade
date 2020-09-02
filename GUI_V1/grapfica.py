from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d, Axes3D
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
from mpl_toolkits.mplot3d.proj3d import proj_transform
from matplotlib.patches import FancyArrowPatch
from geopy.distance import geodesic,lonlat, distance
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



def _arrow3D(ax, x, y, z, dx, dy, dz, *args, **kwargs):
    '''Add an 3d arrow to an `Axes3D` instance.'''

    arrow = Arrow3D(x, y, z, dx, dy, dz, *args, **kwargs)
    ax.add_artist(arrow)

setattr(Axes3D,'arrow3D',_arrow3D)

def leerFicheroGPX (dir):
    df = pd.DataFrame(columns=['wpt','lat','lon','ele'])
    tree = ET.parse(dir)
    root = tree.getroot()
    i=1
    #self.ui.confdescripcionWpText.setText("CARGANDO WAYPOINTS...")
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
        #self.ui.confdescripcionWpText.append('Waypoint '+str(i)+':      Latitud >'+ str(data_lat)[:10]+'        Longitud >'+str(data_lon)[:10]+'       Elevación >'+str(data_eve)[:5]+' m.')
        i=i+1
    return df


def calcularTrayectoria(df_input):
    df = pd.DataFrame(columns=['wpt','lat','lon','ele'],)
    loop = 0
    contador = 1
    for elem in df_input.itertuples():
        data_lat,data_lon,data_ele = elem[2], elem[3], elem[4]
        if loop % 2 == 0:
            df = df.append({'wpt': str(contador), 'lat': data_lat, 'lon': data_lon, 'ele': data_ele},ignore_index=True)
            df = df.append({'wpt': str(contador + 1), 'lat': data_lat, 'lon': data_lon, 'ele': np.nan},ignore_index=True)
        else:
            df = df.append({'wpt': str(contador), 'lat': data_lat, 'lon': data_lon, 'ele': np.nan},ignore_index=True)
            df = df.append({'wpt': str(contador + 1), 'lat': data_lat, 'lon': data_lon, 'ele': data_ele},ignore_index=True)

        contador = contador + 2
        loop = loop + 1

    return df

### Implicito en mplwifget.py
fig = plt.figure()
ax = Axes3D(fig)

ax.zaxis.set_major_locator(plt.LinearLocator(5))
ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.03f'))
ax.yaxis.set_major_locator(plt.LinearLocator(5))
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.03f'))
ax.xaxis.set_major_locator(plt.LinearLocator(5))
ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%.03f'))

###

rutaGPX = "/home/mateo/Escritorio/Universidad/TG/TG_DroneFacade/GUI_V1/Coordenadas.gpx"
wp_entrada = leerFicheroGPX(rutaGPX)
wp_trayectoria = calcularTrayectoria(wp_entrada)

altura = 1000
wp_trayectoria = wp_trayectoria.fillna(float(altura))

trayectoria_ydata = wp_trayectoria['lat'].tolist()
trayectoria_xdata = wp_trayectoria['lon'].tolist()
trayectoria_zdata = wp_trayectoria['ele'].tolist()
media,maximo,minimo = wp_trayectoria.mean(axis=0),wp_trayectoria.max(axis=0),wp_trayectoria.min(axis=0)


rows = wp_trayectoria.get_values()
row_1 = rows[0]
rows = rows[1:]
for row in rows:
    print((row[1],row[2]))
    print((row_1[1],row_1[2]))
    print(geodesic((row[1],row[2]), (row_1[1],row_1[2])).m)
    print("\n")
    distancia = geodesic((row[1],row[2]), (row_1[1],row_1[2])).m + distancia
    elevacion = elevacion + abs(row[3]-row_1[3])
    row_1 = row
print(distancia)
print(elevacion)

wp_entrada_ydata = wp_entrada['lat'].tolist()
wp_entrada_xdata = wp_entrada['lon'].tolist()
wp_entrada_zdata = wp_entrada['ele'].tolist()
ax.scatter(wp_entrada_xdata, wp_entrada_ydata, wp_entrada_zdata, s = 50, c = 'navy', label = 'Wpt entrada', marker = '.')

ax.scatter(trayectoria_xdata, trayectoria_ydata, trayectoria_zdata, s= 50, c='darkcyan',label = 'Wpt trayectoria', marker = 'd')
ax.legend(loc='lower left', ncol=2, borderaxespad=0.)
inicio = True
""" for row in wp_trayectoria.itertuples():
    if inicio:
        row_inicio = row
        ax.text(row[3],row[2],row[4],'w'+str(row[1]), size= 10, zorder=10, color='navy')
        inicio = False
        continue
    ax.text(row[3],row[2],row[4],'w'+str(row[1]), size= 10, zorder=10, color='navy')
    dx,dy,dz= row[3]-row_inicio[3],row[2]-row_inicio[2],row[4]-row_inicio[4]
    ax.arrow3D(row_inicio[3],row_inicio[2],row_inicio[4],
           dx,dy,dz,
           mutation_scale=10,
           arrowstyle="-|>",
           linestyle='dashdot',
           color = 'darkcyan' )
    row_inicio = row """

ax.view_init(elev=20., azim= -135 )
ax.set_title("WayPoints", fontdict=None, loc='center')
ax.set_anchor('C')
#plt.show()




