# Programa para graficar en tiempo real, los datos obtenidos por el arduino receptor mediante el puerto serial

# Importar las librerias de trabajo
import sys  # Interactúa con el sistema operativo
import csv  # Librería para trabajar con archivos CSV
import serial  # Establecer comunicación con el puerto serial
from datetime import datetime  # Trabaja con las fechas y horas
from PyQt5.QtWidgets import *  # Crea la interfaz gráfica del usuario
from PyQt5.QtCore import *  # Módulos principales de PyQt5
from PyQt5.QtGui import *  # Módulos para la interfaz gráfica
import numpy as np  # Módulo para trabajar con arreglos numéricos
import pyqtgraph as pg  # Biblioteca para graficar en PyQt5


class SerialPlot(QWidget):  # Define la clase SerialPlot que hereda QWidget
    def __init__(self, parent=None):
        super(SerialPlot, self).__init__(parent)

        # Configuración de la ventana principal
        self.setWindowTitle("Datos del cohete")
        self.setGeometry(0, 0, 800, 600)  # Posición y tamaño de la ventana

        # Configuración del gráfico de la Altura
        self.graphWidget = pg.PlotWidget(self) # Permite mostrar graficos 2D en esta interfaz
        self.graphWidget.setGeometry(50, 550, 600, 200) #Posición y tamaño, 50 (pos horizontal X), 550 (pos vertical Y), 600 ancho 200 altura
        self.graphWidget.setBackground('w') #Establece color del fondo, en este caso blanco
        self.graphWidget.showGrid(x=True, y=True) # Muestra una cuadricula en el grafico en los dos ejes
        self.graphWidget.setLabel('left', 'Altitud') #Etiqueta eje Y
        self.graphWidget.setLabel('bottom', 'Tiempo (s)') #Etiqueta eje X
        self.graphWidget.setTitle('<b><font size=6 color="black">Altitud</font></b>') # Titulo personalizado de la grafica

        # Configuración del gráfico de la aceleración
        self.graphWidget1 = pg.PlotWidget(self)
        self.graphWidget1.setGeometry(50, 50, 600, 200)
        self.graphWidget1.setBackground('w')
        self.graphWidget1.showGrid(x=True, y=True)
        self.graphWidget1.setLabel('left', 'Aceleración')
        self.graphWidget1.setLabel('bottom', 'Tiempo (s)')
        self.graphWidget1.setTitle('<b><font size=6 color="black">Acelerómetro</font></b>')

        # Configuración del gráfico del giroscopio
        self.graphWidget2 = pg.PlotWidget(self)
        self.graphWidget2.setGeometry(50, 300, 600, 200)
        self.graphWidget2.setBackground('w')
        self.graphWidget2.showGrid(x=True, y=True)
        self.graphWidget2.setLabel('left', 'Giroscopio')
        self.graphWidget2.setLabel('bottom', 'Tiempo (s)')
        self.graphWidget2.setTitle('<b><font size=6 color="black">Giroscopio</font></b>')

        # Configuración del puerto serial
        self.ser = serial.Serial('COM3', 9600)
        self.ser.flush()

        # Variables para almacenar los datos
        num_points = 900  # Arreglo de ceros (Puntos) a mostrar en la gráfica
        self.x_data = np.zeros(num_points)  # Tiempo Inicializa arreglo de ceros con la longitud defninida 1100
        self.y_data_1 = np.zeros(num_points)  # Altura
        self.y_data_2 = np.zeros(num_points)  # AcX
        self.y_data_3 = np.zeros(num_points)  # AcY
        self.y_data_4 = np.zeros(num_points)  # AcZ
        self.y_data_5 = np.zeros(num_points)  # GyX
        self.y_data_6 = np.zeros(num_points)  # GyY
        self.y_data_7 = np.zeros(num_points)  # GyZ

        # Crear las líneas para cada valor a graficar
        self.curve1 = self.graphWidget.plot(self.x_data, self.y_data_1, pen='red', name='Altura') #Crea una curva en el grafico utilizando los datos de los ejes "x" , "y" 
        # Crear las líneas para cada valor a graficar
        self.curve2 = self.graphWidget1.plot(self.x_data, self.y_data_2, pen='g', name='AcX')
        self.curve3 = self.graphWidget1.plot(self.x_data, self.y_data_3, pen='b', name='AcY')
        self.curve4 = self.graphWidget1.plot(self.x_data, self.y_data_4, pen='r', name='AcZ')
        # Crear las líneas para cada valor a graficar
        self.curve5 = self.graphWidget2.plot(self.x_data, self.y_data_5, pen='g', name='GyX')
        self.curve6 = self.graphWidget2.plot(self.x_data, self.y_data_6, pen='b', name='GyY')
        self.curve7 = self.graphWidget2.plot(self.x_data, self.y_data_7, pen='r', name='GyZ')

        # Etiqueta para la temperatura
        self.temp_label = QLabel(self)
        self.temp_label.setGeometry(self.width() - 150, self.height() - 50, 150, 30)
        self.temp_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout = QHBoxLayout() # Define el diseño horizontal con una sola fila 
        layout.addWidget(self.graphWidget) # Agrega un primer grafico
        layout.addWidget(self.graphWidget1) # Agrega el segundo grafico
        layout.addWidget(self.graphWidget2) # Agrega el tercer grafico
        self.setLayout(layout) # Establece diseño de la ventana principal
        self.showFullScreen() #Muestra la ventana en pantalla completa 

        # Configuración del temporizador para actualizar los datos
        self.timer = QTimer()  # Esta línea crea un objeto QTimer y lo asigna a la variable self.timer. Este objeto se utiliza para controlar la ejecución periódica de una función.
        self.timer.timeout.connect(self.update_data)  # Aquí se establece una conexión entre la señal timeout del temporizador (self.timer) y la función self.update_data. Cuando el temporizador alcance su intervalo especificado (en este caso, 10 milisegundos), emitirá la señal timeout
        self.timer.start(10)  # Inicia el temporizador con un intervalo de tiempo de 10 milisegundos.

        # Variable para almacenar el tiempo inicial
        self.start_time = datetime.now()

    def update_data(self):
        # Leer los datos del puerto serie
        line = self.ser.readline().decode().strip()
        values = line.split(',')

        # Calcular el tiempo transcurrido en segundos
        current_time = datetime.now()  # Crea un objeto datetime llamado current_time que representa el momento actual. La función datetime.now() devuelve la fecha y hora actual del sistema.
        elapsed_time = (current_time - self.start_time).total_seconds()  # Realiza una resta entre estos dos objetos de tiempo, lo que resulta en timedelta. total_seconds convierte la diferencia de tiempo en segundos.

        # Obtener la temperatura de Arduino
        temperature = float(values[7]) #Convierte el valor en la posición 7 de la lista values a un número flotante y lo asigna a la variable temperature

        # Mostrar la temperatura en la etiqueta
        self.temp_label.setText(f'Temperatura: {temperature} °C')

        # Añadir los nuevos valores a los datos de la altura
        self.y_data_1[:-1] = self.y_data_1[1:] #Desplaza los elementos de self.y_data_1 una posición hacia la izquierda
        self.y_data_1[-1] = float(values[0]) #Asigna el primer valor (values[0]) convertido a tipo float al último elemento de self.y_data_1
        # Añadir los nuevos valores a los datos de la aceleración
        self.y_data_2[:-1] = self.y_data_2[1:]
        self.y_data_2[-1] = float(values[1]) #Asigna el segundo valor (values[1]) convertido a tipo float al último elemento de self.y_data_2
        self.y_data_3[:-1] = self.y_data_3[1:]
        self.y_data_3[-1] = float(values[2]) #Asigna el tercer valor (values[2]) convertido a tipo float al último elemento de self.y_data_3
        self.y_data_4[:-1] = self.y_data_4[1:]
        self.y_data_4[-1] = float(values[3]) #Asigna el cuarto valor (values[3]) convertido a tipo float al último elemento de self.y_data_4
        # Añadir los nuevos valores a los datos del giroscopio
        self.y_data_5[:-1] = self.y_data_5[1:]
        self.y_data_5[-1] = float(values[4]) #Asigna el quinto valor (values[4]) convertido a tipo float al último elemento de self.y_data_5
        self.y_data_6[:-1] = self.y_data_6[1:]
        self.y_data_6[-1] = float(values[5]) #Asigna el sexto valor (values[5]) convertido a tipo float al último elemento de self.y_data_6
        self.y_data_7[:-1] = self.y_data_7[1:]
        self.y_data_7[-1] = float(values[6]) #Asigna el septimo valor (values[6]) convertido a tipo float al último elemento de self.y_data_7
        # Crear valores para el tiempo
        self.x_data[:-1] = self.x_data[1:]  # Aquí se está realizando una asignación de valores
        self.x_data[-1] = elapsed_time

        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Altura)
        self.curve1.setData(self.x_data, self.y_data_1) # Linea Tiempo Vs Altura
        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Aceleración)
        self.curve2.setData(self.x_data, self.y_data_2) # Linea Tiempo Vs Acel X
        self.curve3.setData(self.x_data, self.y_data_3) # Linea Tiempo Vs Acel Y
        self.curve4.setData(self.x_data, self.y_data_4) # Linea Tiempo Vs Acel Z
        # Actualizar las líneas de la gráfica con los nuevos datos -> (Tiempo, Giroscopio)
        self.curve5.setData(self.x_data, self.y_data_5) # Linea Tiempo Vs Gyr X
        self.curve6.setData(self.x_data, self.y_data_6) # Linea Tiempo Vs Gyr Y
        self.curve7.setData(self.x_data, self.y_data_7) # Linea Tiempo Vs Gyr Z

        with open('datos.csv', 'a', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            if archivo_csv.tell() == 0:  # Verificar si el archivo está vacío
                escritor_csv.writerow(['Tiempo', 'Altitud', 'Acel X', 'Acel Y', 'Acel Z', 'Gyr X', 'Gyr Y', 'Gyr Z', 'Temperatura']) # Escribe una columna con las etiquetas de los datos
            escritor_csv.writerow([elapsed_time, values[0], values[1], values[2], values[3], values[4], values[5], values[6], temperature]) # Escribe en un archivo CSV los datos obtenidos 

    def resizeEvent(self, event):
        # Actualizar el tamaño del gráfico al cambiar el tamaño de la ventana
        self.graphWidget.setGeometry(50, 50, self.width() - 100, self.height() // 3 - 50)
        self.graphWidget1.setGeometry(50, self.height() // 3 + 10, self.width() - 100, self.height() // 3 - 50)
        self.graphWidget2.setGeometry(50, (self.height() // 3) * 2 + 10, self.width() - 100, self.height() // 3 - 50)
        self.temp_label.setGeometry(self.width() - 150, self.height() - 50, 150, 30)


if __name__ == '__main__':
    app = QApplication(sys.argv)  # Crea una instancia de la aplicación QApplication.
    app.setStyle("Fusion")
    palette = QPalette() #Define la paleta de colores de la aplicación.
    palette.setColor(QPalette.Window, QColor(53, 53, 53)) # crea un objeto de color utilizando los valores RGB (rojo, verde, azul) En este caso gris oscuri
    app.setPalette(palette) # Aplica la paleta de colores a la aplicación con setpalette
    window = SerialPlot()  # Crea una instancia de la clase SerialPlot
    sys.exit(app.exec_())  # Sale del programa cuando se cierra la ventana

