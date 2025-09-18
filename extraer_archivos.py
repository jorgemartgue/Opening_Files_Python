# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 10:50:52 2025

@author: jorge
"""

import os
import glob
import pandas as pd

def lee_archivos(ruta,patron = '*.*'):

   ruta_archivos = os.path.join(ruta,patron)
   
   archivos = glob.glob(ruta_archivos)
   
   return archivos


def extraer_archivos(ruta,patron = '*.*'):
    '''
    Esta función extrae los archivos de un directorio dado
    
        Inputs:
            
            ruta: ruta hacia la carpeta donde se guardan los archivos.
                  si los archivos se guardan en la misma carpeta que el 
                  programa usar ''.
                  
            patrón: te permite diferenciar de archivos que tengas en el mismo
                    directorio. Por ejemplo 'p*.*' te extraería los archivos
                    que empiecen por p. Por defecto esta variable está fijada
                    a '*.*' que quiere decir que extraiga todos los archivos.
                
        Outputs: 
            
            archivo_ext: Es un diccionario con todos los archivos que cumplen
                         el patrón solicitado. Los nombres dentro del 
                         diccionario son los mismos nombres que los archivos
                         con el tipo de archivo. 
                         Por ejemplo un archivo llamado prueba que sea txt se
                         guardaria como prueba.txt
                
    '''
    
    archivo_ext = {}
    archivos_leidos = lee_archivos(ruta,patron)
    
    for ruta_comp in sorted(archivos_leidos):
        
            nombre = os.path.basename(ruta_comp)
            
            #Esta linea habría que modificarla en función de los archivos que 
            #tengas que abrir.
            df =  pd.read_csv(ruta_comp,sep ='\\s+' ,comment='%',
                              names=['Tiempo','Flujo'])
            
            archivo_ext[nombre] = df
            
    return archivo_ext
