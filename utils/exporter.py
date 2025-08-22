# utils/exporter.py

import os
import tempfile
import shutil
import webbrowser
from tkinter import filedialog, messagebox
from datetime import datetime
from fpdf import FPDF
import csv

# Clase auxiliar para tener un header y footer estándar en los PDFs
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        # Puedes descomentar esto si tienes un logo en 'assets/images/logo_empresa.png'
        try:
             self.image('images/logo_empresa.png', 10, 8, 33)
        except Exception:
            self.cell(40, 10, 'Logo JPG')
        
        self.cell(0, 10, 'Reporte de Inventario', 0, 1, 'C')
        self.set_font('Arial', '', 8)
        self.cell(0, 10, f'Generado el: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def generate_and_preview_pdf(data_list, headers, report_title='Reporte'):
    """
    Genera un PDF, lo guarda en un archivo temporal, lo abre y devuelve su ruta.
    """
    if not data_list:
        messagebox.showwarning("Sin Datos", "No hay datos para generar el PDF.")
        return None

    try:
        pdf = PDF('L', 'mm', 'A4') # 'L' para formato horizontal (Landscape)
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, report_title, 0, 1, 'L')
        pdf.ln(5)

        pdf.set_font('Arial', 'B', 9)
        num_columns = len(headers)
        page_width = pdf.w - 2 * pdf.l_margin
        cell_width = page_width / num_columns if num_columns > 0 else page_width

        for header_text in headers.values():
            pdf.cell(cell_width, 10, header_text, 1, 0, 'C')
        pdf.ln()

        pdf.set_font('Arial', '', 8)
        for row_data in data_list:
            for key in headers.keys():
                value = str(row_data.get(key, ''))
                pdf.cell(cell_width, 10, value, 1, 0, 'L')
            pdf.ln()

        temp_dir = tempfile.gettempdir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_filepath = os.path.join(temp_dir, f"report_preview_{timestamp}.pdf")
        
        pdf.output(temp_filepath)

        try:
            webbrowser.open(f'file://{os.path.realpath(temp_filepath)}')
        except Exception:
             messagebox.showinfo("Vista Previa", f"El PDF se ha generado en:\n{temp_filepath}\n\nNo se pudo abrir automáticamente.")

        return temp_filepath

    except Exception as e:
        messagebox.showerror("Error al Generar PDF", f"Ocurrió un error inesperado:\n{e}")
        return None

def save_pdf(temp_filepath, default_filename='reporte'):
    """
    Mueve un archivo PDF temporal a una ubicación permanente elegida por el usuario.
    """
    if not temp_filepath or not os.path.exists(temp_filepath):
        messagebox.showerror("Error", "No hay un archivo de vista previa para guardar.")
        return

    timestamp = datetime.now().strftime("%Y%m%d")
    filename_suggestion = f"{default_filename}_{timestamp}.pdf"

    filepath = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
        initialfile=filename_suggestion,
        title="Guardar Reporte PDF"
    )

    if not filepath:
        return # Usuario canceló el diálogo

    try:
        shutil.move(temp_filepath, filepath)
        messagebox.showinfo("Éxito", f"Reporte guardado exitosamente en:\n{filepath}")
    except PermissionError:
        messagebox.showerror("Error de Permisos", "No se pudo guardar el archivo. Verifique los permisos y que el archivo no esté abierto.")
    except Exception as e:
        messagebox.showerror("Error al Guardar", f"Ocurrió un error inesperado:\n{e}")

# Mantenemos la función de exportar a CSV por si la necesitas en otro lugar
def export_to_csv(data_list, headers, default_filename='reporte'):
    # ... (tu código original de CSV aquí, sin cambios)
    pass

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