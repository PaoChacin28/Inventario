# utils/validation.py
import re

def is_valid_rif(rif_string):
    """
    Valida el formato de un RIF venezolano (ej. J-12345678-9).
    Acepta J, V, E, G.
    """
    # ^: inicio de la cadena, [JVEG]: una de estas letras, -: guión, \d{8}: 8 dígitos, \d{1}: 1 dígito, $: fin de la cadena
    pattern = re.compile(r"^[JVEG]-\d{8}-\d{1}$")
    return pattern.match(rif_string) is not None

def is_valid_product_code(code_string):
    """
    Valida un formato de código de producto (ej. CAR-001).
    3-4 letras, un guión, y 3-5 números.
    """
    pattern = re.compile(r"^[A-Z]{3,4}-\d{3,5}$")
    return pattern.match(code_string) is not None

def is_valid_lote_tag(tag_string):
    """
    Valida un formato de tag de lote (ej. LOTE-QUESO-250815).
    Permite letras, números y guiones.
    """
    # \w: cualquier caracter alfanumérico (letras, números, _)
    pattern = re.compile(r"^[\w-]+$")
    return pattern.match(tag_string) is not None