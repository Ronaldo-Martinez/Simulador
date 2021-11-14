import random

def buscarEncontrar(memoriaPrincipal, memoriaCache, numeroPruebas):
    #Para identificar las direcciones de memoria encontradas
    indicesEncontrados=[]
    indicesNoEncontrados=[]
    resultado = [0,numeroPruebas, indicesEncontrados, indicesNoEncontrados]
    for i in range(numeroPruebas):
        #Se generan indices aleatorios
        indice=random.randrange(0, len(memoriaPrincipal)-1)
        #Se extrae el bloque de información de la dirección (Solo se extrae el bloque sin el nuemro de direccion)
        #No se toman en cuenta los datos del set       
        bloque = memoriaPrincipal[indice][1:]
        if len(memoriaPrincipal[indice])>16:
            bloque = memoriaPrincipal[indice][2:]
        
        for cache in memoriaCache:
            #Se valida el tamaño de la variable y se comparan los datos
            size=len(cache)
            #print(indice)
            if size > 17:
                #print(bloque+" - "+cache[2:size-1])
                if bloque!=cache[2:size-1]:
                    fracaso=1
                else:
                    #Exitos
                    indicesEncontrados.append(indice)
                    resultado[0]=resultado[0]+1
                    resultado[1]=resultado[1]-1
                    #print('exito \n')
                    break

            else:
                #print(bloque+" - "+cache[1:size-1])
                if bloque!=cache[1:size-1]:
                    fracaso=1
                else:
                    #Exitos
                    indicesEncontrados.append(indice)
                    resultado[0]=resultado[0]+1
                    resultado[1]=resultado[1]-1
                    fracaso=0
                    #print('exito \n')
                    break
        if fracaso==1:
            indicesNoEncontrados.append(indice)
    #print(indicesEncontrados)
    resultado[2]=indicesEncontrados    
    resultado[3]=indicesNoEncontrados
    return resultado

def direccionEnMemoriaPrinciapl(memoriaCache, direccion):
    size=len(direccion)
    #Controlando tamaño de direccion
    if size>16:
        bloque=direccion[2:]
    else:
        bloque=direccion[1:]
    for cache in memoriaCache:
        size=len(cache)
        if size>17:
            cache=cache[2:size-2]
            if cache==bloque:
                return True
        else:
            cache=cache[1:size-2]
            if cache==bloque:
                return True
    return False
