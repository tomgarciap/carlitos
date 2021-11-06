import re

OPERADORES_MATEMATICOS = ["más", "menos", "dividido", "por", "sobre"]
OPERADORES_ADITIVOS_Y_SUBSTRACTIVOS = ["más", "menos"]


def calculate_operation_result(operation_elements):
    if len(operation_elements) == 0:
        return 0
    terms = get_terms(operation_elements)
    result = execute_calculation_on_elements(terms)
    return result


def execute_calculation_on_elements(terms):
    if len(terms) == 0:
        return 0
    first_term = terms.pop(0)
    if isinstance(first_term, int):
        result = first_term
    elif isinstance(first_term, str):
        if first_term.isnumeric():
            result = int(first_term)
        else:
            raise Exception(f"El primer elemento debe ser un número {first_term}")
    elif isinstance(first_term, list):
        result = execute_calculation_on_elements(first_term)
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
                number_element = execute_calculation_on_elements(operation_element)
            else:
                raise Exception("Tipo de dato no soportado")
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
    return result


def get_terms(operation_elements):
    def not_empty(element):
        if isinstance(element, str):
            element = element.strip()
        return not not element

    str_list = ""
    for operation_element in operation_elements:
        str_list += " " + operation_element
    regex_string = ''
    for index in range(len(OPERADORES_ADITIVOS_Y_SUBSTRACTIVOS)):
        if index == 0:
            regex_string += OPERADORES_ADITIVOS_Y_SUBSTRACTIVOS[index]
        else:
            regex_string += f' |{OPERADORES_ADITIVOS_Y_SUBSTRACTIVOS[index]} '
    str_terms = re.split(regex_string, str_list)
    non_null_str_terms = list(filter(not_empty, str_terms))
    operadores_ad_sub = list(filter(lambda x: x in OPERADORES_ADITIVOS_Y_SUBSTRACTIVOS, operation_elements))
    terms = []
    for index in range(len(non_null_str_terms)):
        if index == 0:
            terms.append(non_null_str_terms[index].strip())
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
