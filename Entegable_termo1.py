# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 22:33:41 2025

@author: jorge
"""

import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson


def lee_archivos(ruta,patron = '*.*'):

   ruta_archivos = os.path.join(ruta,patron)
   
   archivos = glob.glob(ruta_archivos)
   
   return archivos

archivos_flujo = lee_archivos('Entregable2_termo','F*.*')

def extraer_archivos(ruta,nombres,patron = '*.*'):
    '''
    Esta función extrae los archivos de un directorio dado
    
        Inputs:
            
            ruta: ruta hacia la carpeta donde se guardan los archivos.
                  si los archivos se guardan en la misma carpeta que el 
                  programa usar ''.
                  
            nombres: nombres de los datos almacenados en las variables
            
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
                              names=[nombres[0],nombres[1]],
                              dtype={nombres[0]: np.float64, 
                                     nombres[1]: np.float64})
            print(df.dtypes)
            archivo_ext[nombre] = df
            
    return archivo_ext


datos_flujo = extraer_archivos('Entregable2_termo',['Tiempo','Flujos'],'F*.*')
datos_temp = extraer_archivos('Entregable2_termo',['Tiempo','Temperaturas'],
                              'T*.*')



'Representación de los flujos'

plt.figure(1)
for columnas in datos_flujo.values():
        
    plt.plot(columnas['Tiempo'],columnas['Flujos'],'.')

plt.xlabel('Tiempo')
plt.ylabel('Flujo')

plt.title('Evolución temporal del flujo en cada posición de la barra')

plt.legend(('x = 0.25','x = 0.5','x = 0.75','x = 1.0','x = 1.25','x = 1.5',
            'x = 1.75','x = 2.0','x = 2.25','x = 2.5','x = 2.75'),
             prop={'size':8},loc='upper right')

plt.grid('on')
plt.show()

'Representación de las temperaturas en kelvin'

plt.figure(2)
for columnas in datos_temp.values():
        
    plt.plot(columnas['Tiempo'],columnas['Temperaturas']+273,'.')

plt.xlabel('Tiempo')
plt.ylabel('Temperatura')

plt.title('Evolución temporal del flujo en cada posición de la barra')

plt.legend(('x = 0.25','x = 0.5','x = 0.75','x = 1.0','x = 1.25','x = 1.5',
            'x = 1.75','x = 2.0','x = 2.25','x = 2.5','x = 2.75'),
             prop={'size':8},loc='upper right')

plt.grid('on')
plt.show()

'Analicemos si los se llega a un estado estacionario y cuando'

'Interpolemos los datos que tenemos 6000 datos'
tiempo_estudiado = datos_flujo['Flux0.25.txt']['Tiempo']

flujo_interp2_0 = np.interp(tiempo_estudiado,
                            datos_flujo['Flux2.0.txt']['Tiempo'],
                            datos_flujo['Flux2.0.txt']['Flujos'])

temp_interp2_25 = np.interp(tiempo_estudiado,
                            datos_temp['Temp2.25.txt']['Tiempo'],
                            datos_temp['Temp2.25.txt']['Temperaturas'])+273

'Representemos el estado estacionario'
x = np.arange(0.25,2.76,0.25)
temp_esta = np.zeros(11)
i = 0
for columnas in datos_temp.values():
    
    if x[i] == 2.25:
        
        temp_esta[i] = temp_interp2_25[len(temp_interp2_25)-1]
        
    else:
        
        temp_esta[i] = columnas['Temperaturas'][len(columnas['Temperaturas']
                                                    )-1]+273
    
    i += 1

plt.figure(3)

plt.plot(x,temp_esta,'r')

plt.xlabel('posición')
plt.ylabel('Temperatura')

plt.title('Temperatura en cada posición en el estado estacionario')

plt.grid('on')

plt.show()

'Obtengamos un ajuste por minimos cuadrados a una recta '
'(perfil de temperatura)'

coef = np.polyfit(x,temp_esta,1)
pol = np.poly1d(coef) #Esto es nuestro polinomio

tempx_0 = pol(0)
tempx_3 = pol(3) 

'promedio del flujo'
suma = 0

i = 0

for columnas in datos_flujo.values():
    
    if x[i] == 2.0:
        
        suma += flujo_interp2_0[len(flujo_interp2_0)-1]
        
    else:
        
        suma += columnas['Flujos'][len(columnas['Flujos'])-1]
        
    i += 1    
    
flujprom = suma/len(x)

conduc =- flujprom/coef[0]

def sigma(x):
    return flujprom*33.333*1/pol(x)**2

x_repre = np.linspace(0.25,2.75,50)

plt.figure(4)

plt.plot(x_repre,sigma(x_repre))

plt.xlabel('Posición x')
plt.ylabel('Producción de entropia')

plt.title('Producción de entropia en función de la posición')

plt.grid('on')

plt.show()

flujentro0 = flujprom/pol(0)
flujentro3 = flujprom/pol(3)

'Calculemos la producción total de entropía en función del tiempo'

#Cálculo de la derivada

dx = 0.25
A = np.pi*(0.2/2)**2

tiempo_ev = datos_flujo['Flux0.25.txt']['Tiempo']

T_mat = np.zeros([len(datos_temp['Temp0.25.txt']['Temperaturas']),11])
J_mat = np.zeros([len(datos_flujo['Flux0.25.txt']['Flujos']),11])
i = 0
for columnas in datos_temp.values():
    
    if x[i] == 2.25:
        T_mat[:,i] = temp_interp2_25
    else:
        T_mat[:,i] = columnas['Temperaturas']+273
    i+=1
i = 0
for columnas in datos_flujo.values():
    
    if x[i] == 2.0:
        J_mat[:,i] = flujo_interp2_0
    else:
        J_mat[:,i] = columnas['Flujos']
    i+=1
    
dTdx = np.gradient(T_mat,dx,axis = 1)

sigma_mat = J_mat/T_mat**2*np.abs(dTdx)

P = A*simpson(sigma_mat,x)


plt.figure(5)

plt.plot(tiempo_ev,P)

plt.title('Producción total de entropia en función del tiempo')

plt.xlabel('Tiempo')
plt.ylabel('Producción total de entropia')

plt.grid('on')
plt.show()