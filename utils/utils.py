from tkinter import messagebox
from datetime import datetime

def clear_frame(frame):
    """
    Elimina todos los widgets hijos de un frame de tkinter dado.
    Esto es útil para limpiar un área de contenido antes de dibujar una nueva vista.
    """

    for widget in frame.winfo_children():
        widget.destroy()


def validar_fecha(fecha_str):
    """
    Valida que un string tenga el formato de fecha 'YYYY-MM-DD'.
    Devuelve un objeto de fecha si es válido, de lo contrario devuelve None.
    """
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        messagebox.showerror("Error de Formato", f"La fecha '{fecha_str}' no es válida. Use el formato YYYY-MM-DD.")
        return None


def validar_entero_positivo(numero_str, nombre_campo):
    """

    Valida que un string sea un número entero y positivo (mayor o igual a cero).
    Devuelve el número como entero si es válido, de lo contrario devuelve None.
    """

    if not numero_str.isdigit():
        messagebox.showerror("Error de Formato", f"El campo '{nombre_campo}' debe ser un número entero.")
        return None
        
    numero = int(numero_str)
    if numero < 0:
        messagebox.showerror("Error de Valor", f"El campo '{nombre_campo}' no puede ser un número negativo.")
        return None
        
    return numero


def validar_flotante_positivo(numero_str, nombre_campo):
    """
    Valida que un string sea un número flotante y positivo (mayor que cero).
    Devuelve el número como flotante si es válido, de lo contrario devuelve None.
    """
    try:
        numero = float(numero_str)
        if numero <= 0:
            messagebox.showerror("Error de Valor", f"El campo '{nombre_campo}' debe ser un número positivo mayor que cero.")
            return None
        return numero
    except ValueError:
        messagebox.showerror("Error de Formato", f"El campo '{nombre_campo}' debe ser un número válido (ej. 10.50).")
        return None