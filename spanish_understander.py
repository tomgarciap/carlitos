NUMEROS = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce",
           "trece",
           "catorce", "quince", "dieciseis", "diecisiete", "dieciocho", "diecinueve", "veinte",
           "veintiuno",
           "treinta",
           "cuarenta",
           "cincuenta",
           "sesenta",
           "setenta",
           "ochenta",
           "noventa",
           "cien", "ciento",
           "doscientos", "doscientas",
           "trescientos", "trescientas",
           "cuatrocientos", "cuatrocientas",
           "quinientos", "quinientas",
           "seiscientos", "seiscientas",
           "setecientos", "setecientas",
           "ochocientos", "ochocientas",
                          "novecientos", "novecientas"]

PRE_DECIMALES = ["ciento", "mil", "millon", "billon", "trillon"]
PRE_DECIMALES_MULTIPLICADOR = {
    "ciento": 100,
    "mil": 1000,
    "millon": 1000000,
    "billon": 1000000000,
    "trillon": 1000000000000
}
NUMEROS_EN_ENTEROS = {
    "cero": 0,
    "uno": 1,
    "dos": 2,
    "tres": 3,
    "cuatro": 4,
    "cinco": 5,
    "seis": 6,
    "siete": 7,
    "ocho": 8,
    "nueve": 9,
    "diez": 10,
    "once": 11,
    "doce": 12,
    "trece": 13,
    "catorce": 14,
    "quince": 15,
    "dieciseis": 16,
    "diecisiete": 17,
    "dieciocho": 18,
    "diecinueve": 19,
    "veinte": 20,
    "veintiuno": 21,
    "veintiuna": 21,
    "treinta": 30,
    "cuarenta": 40,
    "cincuenta": 50,
    "sesenta": 60,
    "setenta": 70,
    "ochenta": 80,
    "noventa": 90,
    "cien": 100,
    "ciento": 100,
    "cienta": 100,
    "doscientos": 200,
    "doscientas": 200,
    "trescientos": 300,
    "trescientas": 300,
    "cuatrocientos": 400,
    "cuatrocientas": 400,
    "quinientos": 500,
    "quinientas": 500,
    "seiscientos": 600,
    "seiscientas": 600,
    "setecientos": 700,
    "setecientas": 700,
    "ochocientos": 800,
    "ochocientas": 800,
    "novecientos": 900,
    "novecientas": 900
}


def is_a_number(word):
    return word in NUMEROS


def is_a_pre_decimal(word):
    return word in PRE_DECIMALES


def get_integer_from_numeric_word(numeric_word):
    if not isinstance(numeric_word, str):
        raise Exception("La palabra debe ser siempre un string")
    if is_a_number(numeric_word):
        return NUMEROS_EN_ENTEROS[numeric_word]
    else:
        raise Exception("La palabra no es un numero")


def get_pre_decimal_multiplicator(numeric):
    if not isinstance(numeric, str):
        raise Exception("La palabra debe ser siempre un string")
    if is_a_pre_decimal(numeric):
        return PRE_DECIMALES_MULTIPLICADOR[numeric]
    else:
        raise Exception("La palabra no es un pre decimal")


def extract_integers_from_phrase(phrase):
    if not isinstance(phrase, str):
        raise Exception("La frase debe ser siempre un string")
    words = phrase.split(" ")
    if len(words) == 0:
        return []
    numeric_in_phrase = []
    number_blocks_buffer = []
    for word in words:
        if len(word) <= 2:
            continue
        if is_a_number(word) or is_a_pre_decimal(word):
            number_blocks_buffer.append(word)
        if not is_a_number(word) and not is_a_pre_decimal(word):
            if len(number_blocks_buffer) != 0:
                numeric_in_phrase.append(number_blocks_buffer)
            number_blocks_buffer = []
        if is_a_number(word) and len(number_blocks_buffer) == 1 and words[::-1].index(word) == 0:
            numeric_in_phrase.append(number_blocks_buffer)
    integers = []
    for number_block in numeric_in_phrase:
        if len(number_block) == 0:
            raise Exception("El number block debe ser siempre no nulo")
        if len(number_block) == 1:
            integers.append(get_integer_from_numeric_word(number_block[0]))
        else:
            final_integer = 0
            for numeric in number_block:
                if is_a_pre_decimal(numeric):
                    if final_integer == 0:
                        final_integer = get_pre_decimal_multiplicator(numeric)
                    elif final_integer > 0:
                        if number_block[::-1].index(numeric) == 0:
                            final_integer *= get_pre_decimal_multiplicator(numeric)
                        else:
                            final_integer += get_pre_decimal_multiplicator(numeric)
                elif is_a_number(numeric):
                    final_integer += NUMEROS_EN_ENTEROS[numeric]
                else:
                    raise Exception("La palabra no es un numero ni un pre decimal")
            integers.append(final_integer)
    return integers


if __name__ == "__main__":
    print(extract_integers_from_phrase("tengo ochocientas cuarenta y dos abejas en el panal dos"))
