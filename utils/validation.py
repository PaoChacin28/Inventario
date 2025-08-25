# utils/validation.py
import re
import os
import sys

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

def is_valid_password(password_string):
    """
    Valida la fortaleza de una contraseña según las reglas del sistema.
    Reglas:
    - Al menos 8 caracteres de longitud.
    - Al menos una letra minúscula.
    - Al menos una letra mayúscula.
    - Al menos un número.
    """
    if len(password_string) < 8:
        return False
    if not re.search(r"[a-z]", password_string):
        return False
    if not re.search(r"[A-Z]", password_string):
        return False
    if not re.search(r"\d", password_string):
        return False
    
    # Si pasa todas las comprobaciones, es válida
    return True

# --- AÑADE ESTA NUEVA FUNCIÓN ---
def resource_path(relative_path):
    """ Obtiene la ruta absoluta a un recurso, funciona para desarrollo y para el .exe de PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Si no se está ejecutando en un .exe, usa la ruta normal
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)