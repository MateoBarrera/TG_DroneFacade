# Imports
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D

# Matplotlib canvas class to create figure
class MplCanvas(Canvas):
    def __init__(self):         
        self.fig = Figure()
        self.ax = Axes3D(self.fig)
        self.ax.zaxis.set_major_locator(plt.LinearLocator(5))
        self.ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.01f'))
        self.ax.yaxis.set_major_locator(plt.LinearLocator(5))
        self.ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.01f'))
        self.ax.xaxis.set_major_locator(plt.LinearLocator(5))
        self.ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%.01f'))
        self.ax.view_init(elev=20., azim= -135 )
        self.ax.set_title("WayPoints", fontdict=None, loc='center')
        self.ax.set_anchor('C')
        
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)
        
# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = MplCanvas()                  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
    
