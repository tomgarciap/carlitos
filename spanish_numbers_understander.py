
PALABRAS_CLAVE = ["cuanto es"]
OPERADORES_MATEMATICOS = ["más", "menos", "dividido", "por", "sobre"]
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

PRE_DECIMALES = ["ciento", "mil", "millón", "millones", "billón", "billones", "trillón", "trillones"]
PRE_DECIMALES_EN_ENTEROS = {
    "ciento": 100,
    "mil": 1000,
    "millón": 1000000,
    "millones": 1000000,
    "billón": 1000000000,
    "billones": 1000000000,
    "trillón": 1000000000000,
    "trillones": 1000000000000
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


def get_domain_dictionary():
    return NUMEROS + PRE_DECIMALES + OPERADORES_MATEMATICOS + PALABRAS_CLAVE


def is_a_number(word):
    return word in NUMEROS


def is_a_pre_decimal(word):
    return word in PRE_DECIMALES


def get_integer_from_numeric_word(numeric_word):
    if not isinstance(numeric_word, str):
        raise Exception("La palabra debe ser siempre un string")
    if is_a_number(numeric_word):
        return NUMEROS_EN_ENTEROS[numeric_word]
    if is_a_pre_decimal(numeric_word):
        return PRE_DECIMALES_EN_ENTEROS[numeric_word]
    else:
        raise Exception("La palabra no es un numero")


def get_pre_decimal_multiplicator(numeric):
    if not isinstance(numeric, str):
        raise Exception("La palabra debe ser siempre un string")
    if is_a_pre_decimal(numeric):
        return PRE_DECIMALES_EN_ENTEROS[numeric]
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
    index = 0
    for word in words:
        if len(word) <= 2:
            index += 1
            continue
        if is_a_number(word) or is_a_pre_decimal(word):
            number_blocks_buffer.append(word)
        if not is_a_number(word) and not is_a_pre_decimal(word):
            if len(number_blocks_buffer) != 0:
                numeric_in_phrase.append(number_blocks_buffer)
            number_blocks_buffer = []
        if is_a_number(word) and len(number_blocks_buffer) == 1 and index == (len(words) + 1):
            numeric_in_phrase.append(number_blocks_buffer)
        if len(number_blocks_buffer) >= 1 and index + 1 == len(words):
            numeric_in_phrase.append(number_blocks_buffer)
        index += 1
    integers = []
    for number_block in numeric_in_phrase:
        if len(number_block) == 0:
            raise Exception("El number block debe ser siempre no nulo")
        if len(number_block) == 1:
            integers.append(get_integer_from_numeric_word(number_block[0]))
        else:
            final_integer = 0
            index = 0
            skip_next_pre_decimal = False
            for numeric in number_block:
                if skip_next_pre_decimal and is_a_pre_decimal(numeric):
                    skip_next_pre_decimal = False
                    index += 1
                    continue
                if is_a_pre_decimal(numeric):
                    if final_integer == 0:
                        final_integer = get_pre_decimal_multiplicator(numeric)
                    elif final_integer > 0:
                        if index + 1 == len(number_block):
                            final_integer *= get_pre_decimal_multiplicator(numeric)
                        else:
                            final_integer += get_pre_decimal_multiplicator(numeric)
                elif is_a_number(numeric):
                    if index + 1 == len(number_block):
                        final_integer += get_integer_from_numeric_word(numeric)
                    elif is_a_pre_decimal(number_block[index + 1]):
                        skip_next_pre_decimal = True
                        final_integer += (get_integer_from_numeric_word(numeric) * get_pre_decimal_multiplicator(number_block[index + 1]))
                    else: 
                        final_integer += get_integer_from_numeric_word(numeric)
                else:
                    raise Exception("La palabra no es un numero ni un pre decimal")
                index += 1
            integers.append(final_integer)
    return integers


def extract_mathematical_operators(phrase):
    if len(phrase) == 0:
        return None
    operators = []
    for word in phrase.split():
        if word in OPERADORES_MATEMATICOS:
            operators.append(word)
    return operators


if __name__ == "__main__":
    test = "test"
    print(extract_integers_from_phrase("tengo ochocientas cuarenta y dos abejas en el panal dos"))
    print(extract_integers_from_phrase("cuanto es cuatro mil ochocientos noventa y cuatro mas doce mil doscientos mas "
                                       "cuatrocientos noventa y seis"))
    print(extract_integers_from_phrase("dos millones trescientos treinta y tres mil cuatrocientos noventa y cuatro"))
    print(extract_integers_from_phrase('cuanto es seiscientos más cinco mil más ochocientos más quinientos más mil más dos mil'))
