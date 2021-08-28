#Programa de interfaz gráfica para generación de códigos QR
#Gerardo Sánchez Alba

import PySimpleGUI as sg

#Recipe - Get Filename With No Input Display. Returns when file selected-----------------
sg.theme()

layout = [[sg.Text('Elige un archivo con extensión CSV')],
          [sg.Input(key='-FILE-', visible=False, enable_events=True), sg.FileBrowse(button_text='Buscar',file_types=(("CSV", "*.csv"), ))]]

event, values = sg.Window('Buscar archivo', layout).read(close=True)

print(f'You chose: {values["-FILE-"]}')


#----------------------------------------------------------------------------------------