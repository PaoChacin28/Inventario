# utils/exporter.py
import csv
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime

def export_to_csv(data_list, headers, default_filename='reporte'):
    """
    Exporta una lista de diccionarios a un archivo CSV.
    
    Args:
        data_list (list): La lista de datos, donde cada elemento es un diccionario
                          que representa una fila.
        headers (dict): Un diccionario que mapea las claves de los datos (keys) a los
                        nombres de columna deseados (values). Ej: {'producto_nombre': 'Producto'}
        default_filename (str): El nombre base para el archivo sugerido.
    """
    if not data_list:
        messagebox.showwarning("Sin Datos", "No hay datos en la tabla para exportar.")
        return

    # Sugerir un nombre de archivo con fecha y hora para que sea único
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_suggestion = f"{default_filename}_{timestamp}.csv"

    # Abrir el diálogo para que el usuario elija dónde guardar el archivo
    filepath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
        initialfile=filename_suggestion,
        title="Guardar Reporte como CSV"
    )

    # Si el usuario presiona "Cancelar", filepath será una cadena vacía
    if not filepath:
        return

    # Obtener las claves de los datos en el orden de las cabeceras
    data_keys = list(headers.keys())
    # Obtener los nombres de las cabeceras en el mismo orden
    header_names = list(headers.values())

    try:
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # Usar DictWriter para manejar fácilmente la escritura desde diccionarios
            writer = csv.DictWriter(csvfile, fieldnames=data_keys)
            
            # Escribir la cabecera usando los nombres amigables del diccionario de headers
            csvfile.write(','.join(header_names) + '\n')
            
            # Escribir todas las filas de datos
            writer.writerows(data_list)
        
        messagebox.showinfo("Éxito", f"Reporte exportado exitosamente en:\n{filepath}")
    except PermissionError:
        messagebox.showerror("Error de Permisos", "No se pudo guardar el archivo.\n"
                                                  "Asegúrese de tener permisos de escritura en la carpeta seleccionada "
                                                  "y que el archivo no esté abierto en otro programa (ej. Excel).")
    except Exception as e:
        messagebox.showerror("Error al Exportar", f"Ocurrió un error inesperado al guardar el archivo:\n{e}")