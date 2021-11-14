
from simulacion_app.memorias.Hexadecimal import *

def reemplazoLRU(direccion, memoriaCache):
    #como se utiliza un indice para las direcciones este puede aumentar el tamaño de la direccion
    #por lo que se debe controlar si es mas grande de lo  normal
    set = direccion[0:1]
    if len(direccion)>16:
        set=direccion[0:2]
    #Se continua con la siguiente parte
    n =  int(set)
    
    bitUso=0
    for i in range(7):
        bitUso=bitUso+int(memoriaCache[(n%4)*8+i][-1])
        #print(str((n%4)*8+i))
    #si existe mas de uno se utiliza el agoritmo FIFO
    if bitUso>=1:
        for i in range(7):
            #print(memoriaCache[(n%4)*8+i][-1])
            if int(memoriaCache[(n%4)*8+i][-1])==0:
                if len(direccion)>16:
                    memoriaCache[(n%4)*8+i]=str(n%4)+int_to_hexTAG(i)+direccion[7:] + "1"
                    break
                else:
                    memoriaCache[(n%4)*8+i]=str(n%4)+int_to_hexTAG(i)+direccion[6:] + "1"
                break
    else:
        memoriaCache[(n%4)*8+i]=str(n%4)+int_to_hexTAG(i)+direccion[5:] + "1"
    return memoriaCache      

def ubicacionReemplazo(memoriaCache,direccion):
    index= 0
    set = direccion[0:1]
    if len(direccion)>16:
        set=direccion[0:2]
    n=int(set)        
    for i in range (7):
        if memoriaCache[(n%4)*8+i][-1]==0:
            index = i
            break
    return index

def reescritura(memoriaPrincipal, memoriaCache, palabra, direccion):
    posC =0
    posP = 0
    #Se obtiene la ubicación de la dirección a cambiar en memoria principal
    posP=memoriaPrincipal.index(direccion)
    #Se procede a reemplazar los datos en memoria Princiapl
    #print(memoriaPrincipal[posP])
    memoriaPrincipal[posP]=memoriaPrincipal[posP][0:-len(palabra)]+palabra
    #Se obtiene la ubicación de la dirección a cambiar en memoria cache
    #print(direccion+"0")
    try:
        #Puede Se evalua si se encutra el bloque en memoria cache, (Tomar en cuenta el Bit de Uso)
        try:
            posC =  memoriaCache.index(direccion+"0")
        except:
            posC =  memoriaCache.index(direccion+"1")
        memoriaCache[posC]=memoriaCache[posC][0:-(len(palabra)+1)]+palabra+"1"
    except:
        direccion=direccion[0:len(direccion)-len(palabra)]+palabra
        memoriaCache=reemplazoLRU(direccion,memoriaCache)
        posC=ubicacionReemplazo(memoriaCache, direccion+"1")

    memorias=[memoriaPrincipal, memoriaCache]
    return memorias      