#Las siguientes funciones se encargan de crear las diferentes parates de cada dirección de memoria.

def int_to_hex(dato):
    hex_string = str(f'{dato:x}')
    while len(hex_string) < 8:
        hex_string = "0" + hex_string
    return hex_string

def int_to_hexTAG(dato):
    hex_string = str(f'{dato:x}')
    while len(hex_string) < 5:
        hex_string = "0" + hex_string
    return hex_string

def int_to_hexWord(dato):
    hex_string = str(f'{dato:x}')
    while len(hex_string) < 2:
        hex_string = "0" + hex_string
    return hex_string
