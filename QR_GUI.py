#Programa de interfaz gráfica para generación de códigos QR
#Gerardo Sánchez Alba

import PySimpleGUI as sg
import pandas as pd
import os.path

#Tipo de archivos que admitimos para lectura
FILETYPES = (("Libro de Excel", "*.xlsx"),("Archivo CSV", "*.csv")) 

#Recipe - Get Filename With No Input Display. Returns when file selected
sg.theme()

layout = [[sg.Text('Elige un archivo con extensión CSV o un Libro de Excel')],
          [sg.Input(key='-FILE-', visible=False, enable_events=True), sg.FileBrowse(button_text='Buscar',file_types=(FILETYPES),pad = (150,10))]]

event, values = sg.Window('Generador_QR', layout).read(close=True)

print(f'You chose: {values["-FILE-"]}')

#Leer datos del archivo desde la ruta seleccionada por el usuario
nombre_archivo, extension = os.path.splitext(str(values["-FILE-"]))

if extension == ".csv":
     datos = pd.read_csv(values["-FILE-"])

elif extension == ".xlsx":
    datos = pd.read_excel(values["-FILE-"])
else: 
    sg.popup("No se eligió un tipo de archivo permitido", title = "Error")

print(datos)