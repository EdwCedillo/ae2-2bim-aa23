"""
    APEB2-10%] Actividad 2: Genere aplicaciones en un lenguaje de alto nivel que gestione y administre hilos – AE2
"""

import requests
import time
import csv
import threading
# libreria de Python que permite ejecutar operaciones relacionadas con el sistema de archivos
import os
# librería de python que permite ejecutar comandos
import subprocess

def obtener_data():
    lista = []
    with open("informacion/data.csv") as archivo:
        lineas = csv.reader(archivo, quotechar="|")
        for row in lineas:
            # row es una lista iterador
            # con esta estructura ['1|https://es.wikipedia.org/wiki/Provincia_de_Loja']
            # row[0] tendrá: '1|https://es.wikipedia.org/wiki/Provincia_de_Loja'
            # row[0].split("|"), será: ["1", "https://es.wikipedia.org/wiki/Provincia_de_Loja"]
            # row[0].split("|")[1], será: "https://es.wikipedia.org/wiki/Provincia_de_Loja"
            
            numero = row[0].split("|")[0] #obtiene la primera parte
            pagina = row[0].split("|")[1] #obtiene la segunda parte
            # print("Iteracion: ", row," Numero: ", numero," Direccion: ", pagina) #comprobacion dentro del bucle

            # pass
            lista.append((numero, pagina)) #Agrega un nuevo pares elemento al final de la lista.

    #print(lista) #comprobacion de que si esta guardando en list   
    # se retorna la lista con la información que se necesita
    return lista

#obtener_data() #llamada a funcion #comprobacion


def obtenerHTML(direccion_web):
    try:
        # Realizar la solicitud HTTP para obtener el HTML
        respuesta = requests.get(direccion_web)
        respuesta.raise_for_status()
        #print(respuesta) #respuesta del estado de la peticion
        # Obtener el contenido HTML
        contenido_html = respuesta.text
    except requests.exceptions.RequestException as e:
        print(f"No se pudo obtener el HTML de {direccion_web}: {e}")

    #print(contenido_html) #comprobacion que si se imprime
    # Retorno del contenido de l direccion
    return contenido_html

#contenido = obtenerHTML("https://es.wikipedia.org/wiki/Provincia_de_Loja") #llamada a funcion #comprobacion

#print(contenido) 

#Guardar contenido HTML en formato .txt
def guardarArchivoHTML(nombre_archivo, contenido_html):
    
    # Crear el nombre del archivo a partir del  nombre del parametro + su formato
    #nombre_archivo = nombre_archivo + ".txt"
    #ruta_carpeta_actual = os.getcwd() #Para guardadr en la ruta actual

    # Guardar el contenido HTML en un archivo .txt en la carpeta "salida"
    ruta_archivo = os.path.join("salida", nombre_archivo + ".txt") # Concatrenamos nombre_archivo con el formato .txt
    with open(ruta_archivo, 'w', encoding = 'utf-8') as archivo_salida: #se abre el archivo en modo de escritura ("w")
        archivo_salida.write(contenido_html) #se escribe el contenido HTML 
        archivo_salida.close()

    print(f"Se ha guardado el archivo {nombre_archivo}")


#guardarArchivoHTML("ejemplo2", contenido) #llamada a funcion #comprobacion



def worker(numero, url):
    print("Iniciando %s %s" % (threading.current_thread().getName(), url ))
    # pass
    contenido = obtenerHTML(url)
    guardarArchivoHTML(numero, contenido)

    time.sleep(10)
    print("Finalizando %s" % (threading.current_thread().getName()))

for c in obtener_data():
    # Se crea los hilos
    # en la función
    numero = c[0]
    url = c[1]
    hilo1 = threading.Thread(name='descargando...',
                            target=worker,
                            args=(numero, url))
    hilo1.start()
