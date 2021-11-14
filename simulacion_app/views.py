from functools import cache
from mmap import mmap
from random import Random
from django.http.request import HttpRequest
from django.shortcuts import render
from simulacion_app.memorias.Hexadecimal import *
from simulacion_app.memorias.memorias import *
from simulacion_app.memorias.buscarEncontar import *
import numpy as np
import pandas as pd
from django.http import JsonResponse

from simulacion_app.memorias.reemplazo import reemplazoLRU, reescritura

def imprimirMemoria(request):
    mm = memoriaPrincipal(256)
    #Convierte en un array
    num = np.array(mm)
    #Convierte en una matriz
    reshaped = num.reshape(32,8)
    #Crea una tabla
    tabla = pd.DataFrame(reshaped)
    table = tabla.to_html(classes=["table"],columns=None, header=False ,index=False)
    table = ""

    #Memoria Cache
    sizeCache=40
    mcache=memoriaCache(mm, sizeCache)
    nmc = np.array(mcache)
    reshaped = nmc.reshape(5,8)
    #Tabla Memeoria Cache
    tableCache = pd.DataFrame(reshaped)
    tableCache=tableCache.to_html(classes=["table"],columns=None, header=False ,index=False)
    tableCache=""

    #Perdidas y Exitos
    resultados=[]
    resultados=buscarEncontrar(mm, mcache, 10)
    exitos=resultados[0]
    fracasos=resultados[1]
    indexEncontrados=resultados[2]
    indexNoEncontrados=resultados[3]

    #Reemplazo Aleatorio (Apartir de uno de los sdatos perdidos)
    direccionReemplazo=mm[indexNoEncontrados[0]]
    #print(direccionReemplazo)
    mcache=reemplazoLRU(direccionReemplazo,mcache)
    nmc = np.array(mcache)
    reshaped = nmc.reshape(5,8)
        #Tabla Memeoria Cache con reemplazo
    tableCacheLRU = pd.DataFrame(reshaped)
    tableCacheLRU=tableCacheLRU.to_html(classes=["table"],columns=None, header=False ,index=False)

    #Reemplazo Memoria Principal y Cache
    direccionReemplazo=mm[59]
    #print(direccionReemplazo)
    nuevasmemorias=[]
    palabra="aa"
    nuevasmemorias=reescritura(mm,mcache,palabra,direccionReemplazo)
    #Creando nuevas Tablas
    mm=nuevasmemorias[0]
    nmc = np.array(mm)
    reshaped = nmc.reshape(32,8)
        #Tabla Memoria Principal nueva
    tablePrincipalN = pd.DataFrame(reshaped)
    tablePrincipalN=tablePrincipalN.to_html(classes=["table"],columns=None, header=False ,index=False)
        #Tabla
    mcache=nuevasmemorias[1]
    nmc = np.array(mcache)
    reshaped = nmc.reshape(5,8)
        #Tabla Memeoria Cache Nueva
    tableCacheN = pd.DataFrame(reshaped)
    tableCacheN=tableCacheN.to_html(classes=["table"],columns=None, header=False ,index=False)



    

    context={'table':table, 'tableCache':tableCache, 'exitos':exitos, 'frecasos':fracasos, 'encontrados':indexEncontrados,
            'noEncontrados':indexNoEncontrados, 'tableCacheReemplazo':tableCacheLRU, 'nTablePrincipal': tablePrincipalN,
            'nTableCache':tableCacheN}
    return render(request, "test.html", context)

def inicio(request):
    return render(request, "inicio.html")

def nuevasMemorias(request):

    sizePrincipal = request.GET.get('selectedP')
    sizeCache= request.GET.get('selectedC')

    try:
        sizePrincipal=int(sizePrincipal)
        sizeCache=int(sizeCache)
        #Validando que no entre ningun dato extraño
        if sizePrincipal == 64 or sizePrincipal==128 or sizePrincipal==256:
            if sizeCache == 8 or sizeCache==16 or sizeCache ==32:
                principalMemory= memoriaPrincipal(sizePrincipal)
                #Esto es para crear la tabla
                numLineas = int(sizePrincipal/8)
                direccionPorLinea = int(sizePrincipal/numLineas)
                #Convierte en un array
                num = np.array(principalMemory)
                #Convierte en una matriz
                reshaped = num.reshape(numLineas,direccionPorLinea)
                #Crea una tabla
                tabla = pd.DataFrame(reshaped)
                tabla = tabla.to_html(classes=["table"],columns=None, header=False ,index=False)

                #Memoria Cache
                numLineas = int(sizeCache/8)
                direccionPorLinea = int(sizeCache/numLineas)
                mcache=memoriaCache(principalMemory, sizeCache)
                nmc = np.array(mcache)
                reshaped = nmc.reshape(numLineas,direccionPorLinea)
                #Tabla Memeoria Cache
                tableCache = pd.DataFrame(reshaped)
                tableCache=tableCache.to_html(classes=["table"],columns=None, header=False ,index=False)
                
                #Html de lista para inserción en memoria
                listDirecciones='<option selected>Seleccione una Dirección: </option>'
                for direccion in principalMemory:
                    listDirecciones=listDirecciones+'<option value="'+direccion+'">'+direccion+'</option>'
                listDirecciones=listDirecciones+'</ul>'     
                
    except:
        pass

    #print(sizePrincipal)
    #print(sizeCache)
    contexto={'table':tabla, 'tableCache':tableCache, 'cache':mcache,'principal':principalMemory, 'listDirecciones':listDirecciones}
    return (JsonResponse(contexto))

def randomBusqueda(request):
    cantidad= int(request.GET.get('cantidad'))
    sizeP = request.GET.get('sizeP')
    getCache=request.GET.get('cache')

    cacheMemory = list(getCache.split(","))
    #print(cacheMemory)
    try:
        sizeP=int(sizeP)
        if sizeP == 64 or sizeP==128 or sizeP==256:
            memoriaP=memoriaPrincipal(sizeP)
            memoriaC=cacheMemory
            resultados=buscarEncontrar(memoriaP, memoriaC, cantidad)
            exitos=resultados[0]
            perdidas=resultados[1]
            indexEncontrados=resultados[2]
            indexNoEncontrados=resultados[3]
    except:
        context={}

    exitos="Aciertos: "+str(exitos)
    perdidas = "Perdidas: "+str(perdidas)

    #Se procede a reemplazar en la memoria Cache las direcciones perdidas

    #Genera el html para la lista de direcciones encontradas
    htmlEncontrados = '<ul class="list-group">'
    htmlEncontrados=htmlEncontrados+'<li class="list-group-item bg-dark text-white">'+exitos+'</li>'
    for encontrado in indexEncontrados:
        direccion=memoriaP[encontrado]
        htmlEncontrados = htmlEncontrados + '<li class="list-group-item">'+direccion+'</li>'
    htmlEncontrados = htmlEncontrados + '</ul>'

    #Genera el html para la lista de direcciones no encontradas
    htmlListNoE='<option selected>Seleccione una Dirección: </option>'
    htmlNoEncontrados= '<ul class="list-group">'+'<li class="list-group-item bg-dark text-white">'+perdidas+'</li>'
    for noEncontrado in indexNoEncontrados:
        direccion=memoriaP[noEncontrado]
        htmlNoEncontrados=htmlNoEncontrados+'<li class="list-group-item">'+direccion+'</li>'
        htmlListNoE=htmlListNoE+'<option value="'+direccion+'">'+direccion+'</option>'
    htmlNoEncontrados=htmlNoEncontrados+'</ul>'
    htmlListNoE=htmlListNoE+'</ul>'
    print(htmlListNoE)
    #Retorno de Datos
    context={'thmlNoEncontrados':htmlNoEncontrados, 'thmlEncontrados': htmlEncontrados, 'listNoEncontrado':htmlListNoE}
    return JsonResponse(context)

def reemplazoCache(request):
    #Recepción de datos
    direccion=request.GET.get('direccion')
    mCache=request.GET.get('cache')
    #Se convierte lo recibido en una lista
    cacheMemory = list(mCache.split(","))

    mcache=reemplazoLRU(direccion, cacheMemory)
    lineas=len(mcache)
    lineas=int(lineas/8)


    if len(direccion)>16:
        direccion=direccion[7:]
    else:
        direccion=direccion[6:]

    ##Se genera una variable con el html de una tabla con las direcciones de la nueva Cache
    htmlNuevaCache='<table border="1" class="dataframe table"><tbody>'
    contador=0
    for i in range(lineas):
        htmlNuevaCache=htmlNuevaCache+'<tr>'
        for e in range(8):
            if mcache[contador][6:]==direccion+"1":
                htmlNuevaCache=htmlNuevaCache+'<td class="table-primary">'+mcache[contador]+'</td>'
                contador=contador+1
            else:
                htmlNuevaCache=htmlNuevaCache+'<td>'+mcache[contador]+'</td>'
                contador=contador+1
        htmlNuevaCache=htmlNuevaCache+'</tr>'
    htmlNuevaCache=htmlNuevaCache+'</tbody></table>'

    context={'nuevaCache':htmlNuevaCache}
    return JsonResponse(context)

def insertPalabra(request):
    memoriaP=request.GET.get('principal')
    memoriaC=request.GET.get('cache')
    palabra=str(request.GET.get('palabra'))
    direccion = request.GET.get('direccion')

    cacheMemory = list(memoriaC.split(","))
    principalMemory = list(memoriaP.split(","))

    #Este metodo crear nuevas listas con los datos reemplazods
    nuevasM=reescritura(principalMemory,cacheMemory,palabra,direccion)
    principalMemory=nuevasM[0]
    cacheMemory=nuevasM[1]

    #Control del tamaño de las direcciones
    if len(direccion)>16:
        direccion=direccion[7:]
    else:
        direccion=direccion[6:]
    
    direccion=direccion[:-len(palabra)]+palabra

    ##Se genera una variable con el html de una tabla con las direcciones de la nueva Cache
    lineas=len(cacheMemory)
    lineas=int(lineas/8)
    htmlNuevaCache='<table border="1" class="dataframe table"><tbody>'
    contador=0
    for i in range(lineas):
        htmlNuevaCache=htmlNuevaCache+'<tr>'
        for e in range(8):
            if cacheMemory[contador][6:]==direccion+"1":
                htmlNuevaCache=htmlNuevaCache+'<td class="table-primary">'+cacheMemory[contador]+'</td>'
                contador=contador+1
            else:
                htmlNuevaCache=htmlNuevaCache+'<td>'+cacheMemory[contador]+'</td>'
                contador=contador+1
        htmlNuevaCache=htmlNuevaCache+'</tr>'
    htmlNuevaCache=htmlNuevaCache+'</tbody></table>'

    ##Se genera una variable con el html de una tabla con las direcciones de la nueva Memoria Principal
    htmlNuevaPrincipal=""

    lineas=len(principalMemory)
    lineas=int(lineas/8)
    htmlNuevaPrincipal='<table border="1" class="dataframe table"><tbody>'
    contador=0
    for i in range(lineas):
        htmlNuevaPrincipal=htmlNuevaPrincipal+'<tr>'
        for e in range(8):
            #print(principalMemory[contador][6:]+"---"+direccion)
            if len(principalMemory[contador]) > 16:
                #print(principalMemory[contador])
                if principalMemory[contador][7:]==direccion:
                    htmlNuevaPrincipal=htmlNuevaPrincipal+'<td class="table-primary">'+principalMemory[contador]+'</td>'
                    contador=contador+1
                else:
                    htmlNuevaPrincipal=htmlNuevaPrincipal+'<td>'+principalMemory[contador]+'</td>'
                    contador=contador+1
            else:
                if principalMemory[contador][6:]==direccion:
                    htmlNuevaPrincipal=htmlNuevaPrincipal+'<td class="table-primary">'+principalMemory[contador]+'</td>'
                    contador=contador+1
                else:
                    htmlNuevaPrincipal=htmlNuevaPrincipal+'<td>'+principalMemory[contador]+'</td>'
                    contador=contador+1
        htmlNuevaPrincipal=htmlNuevaPrincipal+'</tr>'
    htmlNuevaPrincipal=htmlNuevaPrincipal+'</tbody></table>'

    #print(cacheMemory)
    #print("--------------")
    #print(principalMemory)
    #print("--------------")
    #print(palabra)
    #print("--------------")
    #print(direccion)

    context={'nuevaCache':htmlNuevaCache, 'nuevaPrincipal':htmlNuevaPrincipal}
    return JsonResponse(context)
    
