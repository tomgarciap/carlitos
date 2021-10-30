

NUMEROS = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce", "quince", "dieciseis", "diecisiete", "dieciocho", "diecinueve", "veinte", 
"veintiuno",
"treinta", 
"cuarenta", 
"cincuenta", 
"sesenta", 
"setenta", 
"ochenta", "noventa", "cien", "ciento", "doscientos", "trescientos", "cuatrocientos", "quinientos", "seiscientos", "setecientos", "ochocientos", 
"novecientos"]

PRE_DECIMALES = ["ciento", "mil", "millon", "billon", "trillon"]


def is_a_number(word):
    return word in NUMEROS

def is_a_pre_decimal(word):
    return word in PRE_DECIMALES


def extract_numbers_from_phrase(phrase):
    if not isinstance(phrase, str):
        raise Exception("La frase debe ser siempre un string")
    words = phrase.split(" ")
    if words.length == 0:
        return []
    numbers_in_phrase = []    
    for word in words:
        if word.length <= 2:
            continue 
        word
    return numbers_in_phrase


if __name__ == "__main__":
    print(extract_numbers_from_phrase("doscientos treinta y dos"))

