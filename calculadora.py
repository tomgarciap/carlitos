import re

OPERADORES_MATEMATICOS = ["más", "menos", "dividido", "por", "sobre"]
OPERADORES_ADITIVOS_Y_SUBSTRACTIVOS = ["más", "menos"]
OPERADORES_MATEMATICOS_SIMBOLOS = {
    "más": "+",
    "menos": "-",
    "dividido": "/",
    "por": "*"
}


def calculate_operation_result(operation_elements):
    if len(operation_elements) == 0:
        return 0
    terms = _get_separate_terms(operation_elements)
    result = _execute_calculation_on_elements(terms)
    return result


def _execute_calculation_on_elements(terms):
    calculo_en_string = ""
    if len(terms) == 0:
        return 0
    first_term = terms.pop(0)
    if isinstance(first_term, int):
        result = first_term
        calculo_en_string += str(first_term)
    elif isinstance(first_term, str):
        if first_term.isnumeric():
            result = int(first_term)
            calculo_en_string += first_term
        else:
            raise Exception(f"El primer elemento debe ser un número {first_term}")
    elif isinstance(first_term, list):
        result = _execute_calculation_on_elements(first_term)
    else:
        raise Exception("El primer elemento debe ser un número o una lista")
    previous_operator_buffer = None
    for index in range(len(terms)):
        operation_element = terms[index]
        if operation_element in OPERADORES_MATEMATICOS:
            previous_operator_buffer = operation_element
        else:
            if previous_operator_buffer is None:
                raise Exception("Operador matemático no encontrado")
            if isinstance(operation_element, int):
                number_element = operation_element
            elif isinstance(operation_element, str):
                if operation_element.isnumeric():
                    number_element = int(operation_element)
                else:
                    raise Exception("Tipo de dato no soportado")
            elif isinstance(operation_element, list):
                number_element = _execute_calculation_on_elements(operation_element)
            else:
                raise Exception("Tipo de dato no soportado")
            calculo_en_string += " " + OPERADORES_MATEMATICOS_SIMBOLOS[previous_operator_buffer] + " " + str(number_element)
            if previous_operator_buffer == "más":
                result = result + number_element
            elif previous_operator_buffer == "menos":
                result = result - number_element
            elif previous_operator_buffer == "dividido":
                result = result / number_element
            elif previous_operator_buffer == "por":
                result = result * number_element
            elif previous_operator_buffer == "sobre":
                result = result / number_element
    print (calculo_en_string + " = " + str(result))
    return result


def _get_separate_terms(operation_elements):
    def not_empty(element):
        if isinstance(element, str):
            element = element.strip()
        return not not element

    str_list = ""
    for operation_element in operation_elements:
        str_list += " " + str(operation_element)
    regex_matcher = ''
    for index in range(len(OPERADORES_ADITIVOS_Y_SUBSTRACTIVOS)):
        if index == 0:
            regex_matcher += OPERADORES_ADITIVOS_Y_SUBSTRACTIVOS[index]
        else:
            regex_matcher += f' |{OPERADORES_ADITIVOS_Y_SUBSTRACTIVOS[index]} '
    str_terms = re.split(regex_matcher, str_list)
    non_null_str_terms = list(filter(not_empty, str_terms))
    operadores_ad_sub = list(filter(lambda x: x in OPERADORES_ADITIVOS_Y_SUBSTRACTIVOS, operation_elements))
    if len(operadores_ad_sub) == 0:
        if len(non_null_str_terms) != 1:
            raise Exception("No se encontrarón separadores de terminos y no se encontró solamente ún termino")
        stripped_term = non_null_str_terms[0].strip()
        if " " in stripped_term:
            return stripped_term.split()
        else:
            return stripped_term
    terms = []
    for index in range(len(non_null_str_terms)):
        if index == 0:
            stripped_term = non_null_str_terms[0].strip()
            if " " in stripped_term:
                stripped_term = stripped_term.split()
            else:
                stripped_term = stripped_term
            terms.append(stripped_term)
        else:
            terms.append(operadores_ad_sub[index - 1])
            stripped_term = non_null_str_terms[index].strip()
            if " " in stripped_term:
                terms.append(stripped_term.split())
            else:
                terms.append(stripped_term)
    return terms


def unit_tests():
    print(calculate_operation_result(
        ["2", "más", "2", "menos", "4", "dividido", "4", "más", "1", "dividido", "2", "menos", "1"]))
    print(calculate_operation_result(["4125", "más", "142934", "menos", "3"]))


if __name__ == "__main__":
    unit_tests()
