#Programa de interfaz gráfica para generación de códigos QR
#Gerardo Sánchez Alba

import PySimpleGUI as sg
import pandas as pd
import os,qrcode,sys

#Tipo de archivos que admitimos para lectura
FILETYPES = (("Libro de Excel", "*.xlsx"),("Archivo CSV", "*.csv")) 

#Recipe - Get Filename With No Input Display. Returns when file selected
sg.theme()

layout = [[sg.Text('Elige un archivo con extensión CSV o un Libro de Excel')],
          [sg.Input(key='-FILE-', visible=False, enable_events=True), sg.FileBrowse(button_text='Buscar',file_types=(FILETYPES),pad = (150,10))],
          [sg.Text("Elegiste: "),sg.Text(size=(30,1), key='-ARCHIVO_ELEGIDO-')],
          [sg.Button('Continuar')]]

window_buscar_archivo = sg.Window('Generador_QR', layout,element_justification="center")


while True:                  # the event loop
    event, values = window_buscar_archivo.read()
    if event == sg.WIN_CLOSED:
        sys.exit("Se cerró el programa")
    if event == '-FILE-':
        nombre_archivo = values['-FILE-'].split("/")
        window_buscar_archivo['-ARCHIVO_ELEGIDO-'].update(nombre_archivo[-1])
    if event == 'Continuar':
        if values['-FILE-']:  
              # if something is highlighted in the list
            archivo_elegido = values['-FILE-']
            break
    
window_buscar_archivo.close()
#print(f'You chose: {values["-FILE-"]}')

#Leer datos del archivo desde la ruta seleccionada por el usuario
nombre_archivo, extension = os.path.splitext(str(archivo_elegido))


if extension == ".csv":
    datos = pd.read_csv(values["-FILE-"])

elif extension == ".xlsx":
    datos = pd.read_excel(values["-FILE-"])
else: 
    sg.popup("No se eligió un tipo de archivo permitido", title = "Error")

# except UnicodeDecodeError:
#     sg.popup("El archivo elegido tiene problemas de decodificación, pruebe otro formato, como csv utf-8", title = "Error")
    

#Elegir columna que se desea convertir a QR
diccionario_de_datos = datos.to_dict()
nombre_columnas = [nombre for nombre in diccionario_de_datos.keys()]
#print(nombre_columnas)

layout = [  [sg.Text('¿De qué columna desea obtener los códigos QR?')],
            [sg.Listbox(nombre_columnas, size=(45, len(nombre_columnas)), key='-NOMBRE_COLUMNA-')],
            [sg.Button('Ok')]]
            #[sg.Text("Elegiste: "),sg.Text(size=(15,1), key='-COLUMNA_ELEGIDA-')]]
            

window_elegir_columna = sg.Window('Elige un nombre de columna', layout, element_justification="center")

while True:                  # the event loop
    event, values = window_elegir_columna.read()
    if event == sg.WIN_CLOSED:
        sys.exit("Se cerró el programa")
    if event == 'Ok':
        if values['-NOMBRE_COLUMNA-']:  
            #window_elegir_columna['-COLUMNA_ELEGIDA-'].update(values['-NOMBRE_COLUMNA-'][0])  # if something is highlighted in the list
            columna_elegida = values['-NOMBRE_COLUMNA-'][0]
            break
window_elegir_columna.close()
#Creación de carpeta para la columna seleccionada
nombre_columna = str(columna_elegida).title()
nombre_carpeta = nombre_columna.upper().replace(" ","_")+"_QR"

if "resultados" not in os.listdir("./"):
    os.makedirs("resultados")

if nombre_carpeta not in os.listdir("./resultados"):
    os.makedirs("./resultados/" + nombre_carpeta)

#Creación de códigos QR para la columna seleccionada en el directorio elegido
def generar_qr(diccionario_de_datos, columna_elegida, nombre_carpeta = ""):
    for index,dato in enumerate(diccionario_de_datos[columna_elegida].values()):
        imagen = qrcode.make(str(dato))
        f = open("./resultados/" + nombre_carpeta+"/"+nombre_columna+"_"+str(index)+".png","wb")
        imagen.save(f)
        f.close()
    return index+1
    
n_datos = generar_qr(diccionario_de_datos, columna_elegida, nombre_carpeta)

layout = [[sg.Text("Los códigos QR fueron generados en la carpeta: " + nombre_carpeta)],
            [sg.Text("Se crearon: " + str(n_datos) + " QRs")],
            [sg.Text("En la dirección: " + str(os.getcwd()) + "\\resultados\\" + nombre_carpeta)]]

event, values = sg.Window('Generador_QR', layout).read(close=True)