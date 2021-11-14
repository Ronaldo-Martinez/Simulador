from django.http.request import HttpRequest
from django.shortcuts import render
from simulacion_app.memorias.Hexadecimal import *
from random import randint

def memoriaPrincipal(size):
    direccionPorLinea = 8
    aux=0
    tag=0
    memoriaPrincipal=[]
    for i in range(size):
        palabra=aux+i
        memoriaPrincipal.append(str(aux)+int_to_hexTAG(tag)+int_to_hex(i)+int_to_hexWord(palabra))
        tag = tag + 1
        if (i+1)%direccionPorLinea == 0:
            aux = aux +1
            tag =0
    '''
    for i in range(128):
        print(memoriaPrincipal[i])'''
    return memoriaPrincipal

def memoriaCache(memoriaPrincipal, sizeCache):
    cache=[]
    sizeCache=int(sizeCache)
    contador=1
    for memoria in memoriaPrincipal:
        bitUso= str(randint(0, 1))
        set = memoria[0:1]
        cache.append(set+memoria[1:]+bitUso)
        if contador == sizeCache:
            break
        contador=contador+1
    return cache


##Métodos heredados
def imprimirMemoria(request):
    mm = memoriaPrincipal()
    texto = ""
    contador = 0
    for i in mm:
        texto = texto + i + " | "
        if (contador+1)%8 == 0:
            texto=texto+"\n"
        contador= contador +1
    
    return render(request, "../templates/test.html", {'data': texto})
    


