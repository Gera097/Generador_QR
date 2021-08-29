#Programa de interfaz gráfica para generación de códigos QR
#Gerardo Sánchez Alba

import PySimpleGUI as sg
import pandas as pd
import os.path
import qrcode

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

#Elegir columna que se desea convertir a QR
diccionario_de_datos = datos.to_dict()
nombre_columnas = [nombre for nombre in diccionario_de_datos.keys()]
print(nombre_columnas)

layout = [  [sg.Text('¿De qué columna desea obtener los códigos QR?')],
            [sg.Listbox(nombre_columnas, size=(15, len(nombre_columnas)), key='-NOMBRE_COLUMNA-')],
            [sg.Button('Ok')],
            [sg.Text("Elegiste: "),sg.Text(size=(15,1), key='-COLUMNA_ELEGIDA-')]]
            

window = sg.Window('Elige un nombre de columna', layout)

while True:                  # the event loop
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Ok':
        if values['-NOMBRE_COLUMNA-']:  
            window['-COLUMNA_ELEGIDA-'].update(values['-NOMBRE_COLUMNA-'])  # if something is highlighted in the list

window.close()

#Creación de códigos QR para la columna seleccionada en el directorio elegido
