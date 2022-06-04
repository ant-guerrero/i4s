# importamos las librerías que vamos a necesitar
import pandas as pd
import numpy as np

def read_im_raw(filename):
    
    dd=dict();
   
    # leer el fichero por líneas
    f=open(filename)
    lines=f.readlines()
    
    # obtener el tamaño de la cabecera
    head_size=0
    while lines[head_size][0] != 'D':
        head_size+=1

    # obtener cúales son las componentes: 'HDZF', 'XYZF' u otras
    comp=lines[7].split()[1]
    
    # obtener la latitud y la longitud geográfica del observatorio
    lat=lines[4].split()[2]
    lon=lines[5].split()[2]
    
    names=['datetime','doy','c1','c2','c3','c4']
    colspecs=[(0,23), (25,27), (32,40), (42,50), (52,60), (62,70)]
    data=pd.read_fwf(filename,header=head_size,names=names, colspecs=colspecs)
    
   
    dd['data']=data
    dd['lon']=lon
    dd['lat']=lat
    dd['comp']=comp
    
    return dd

def read_im(filename):
    
    dd=dict();
   
    # leer el fichero por líneas
    f=open(filename)
    lines=f.readlines()
    
    # obtener el tamaño de la cabecera
    head_size=0
    while lines[head_size][0] != 'D':
        head_size+=1

    # obtener cúales son las componentes: 'HDZF', 'XYZF' u otras
    comp=lines[7].split()[1]
    
    # obtener la latitud y la longitud geográfica del observatorio
    lat=lines[4].split()[2]
    lon=lines[5].split()[2]
    
    names=['datetime','doy','c1','c2','c3','c4']
    colspecs=[(0,23), (25,27), (32,40), (42,50), (52,60), (62,70)]
    data=pd.read_fwf(filename,header=head_size,names=names, colspecs=colspecs)
    
    # Transform 99999 values to NaN
    data.c1 = np.where(data.c1 == 99999, data.c1*np.nan, data.c1)
    data.c2 = np.where(data.c2 == 99999, data.c2*np.nan, data.c2)
    data.c3 = np.where(data.c3 == 99999, data.c3*np.nan, data.c3)
    data.c4 = np.where(data.c4 == 99999, data.c4*np.nan, data.c4)
    
    # comprobar si el formato es 'HDZF' y convertir si es necesario
    if comp == 'XYZF':
        x = data.c1
        y = data.c2
        h = np.sqrt(x**2+y**2)
        d = 180./np.pi*60.*np.arctan2(y,x)
        data.c1=h
        data.c2=d
    elif comp != 'HDZF':
        print('Formato de coordenadas no reconocido')


    dd['data']=data
    dd['lon']=lon
    dd['lat']=lat
    dd['comp']=comp
    
    return dd