# utils/exporter.py

import os
import tempfile
import webbrowser
from tkinter import messagebox
from datetime import datetime
from fpdf import FPDF
from utils.validation import resource_path
import re

# --- NUEVAS IMPORTACIONES PARA REPORTLAB ---
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# ==============================================================================
# SECCIÓN DE FPDF2 (PARA REPORTES TABULARES - SIN CAMBIOS)
# ==============================================================================
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        try:
            logo = resource_path("images/logo_empresa.png")
            self.image(logo, 10, 8, 33)
        except Exception as e:
            print(f"No se pudo cargar el logo para el reporte: {e}")
        self.cell(0, 10, 'Reporte de Inventario', 0, 1, 'C')
        self.set_font('Arial', '', 8)
        self.cell(0, 10, f'Generado el: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', 0, 1, 'C')
        self.ln(10)
    def footer(self):
        self.set_y(-15); self.set_font('Arial', 'I', 8); self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def generate_and_preview_pdf(data_list, headers, report_title='Reporte'):
    # ... (Esta función para reportes tabulares se queda como está, funciona bien)
    if not data_list: messagebox.showwarning("Sin Datos", "No hay datos para generar el PDF."); return None
    try:
        pdf = PDF('L', 'mm', 'A4')
        pdf.add_page()
        # ... (resto del código de esta función sin cambios)
        pdf.set_font('Arial', 'B', 14); pdf.cell(0, 10, report_title, 0, 1, 'L'); pdf.ln(5)
        pdf.set_font('Arial', 'B', 9)
        num_columns = len(headers)
        page_width = pdf.w - 2 * pdf.l_margin
        cell_width = page_width / num_columns if num_columns > 0 else page_width
        if cell_width < 5: messagebox.showerror("Error de Formato", "El reporte tiene demasiadas columnas para exportar a PDF."); return None
        for header_text in headers.values(): pdf.cell(cell_width, 10, header_text, 1, 0, 'C')
        pdf.ln()
        pdf.set_font('Arial', '', 8)
        for row_data in data_list:
            for key in headers.keys():
                value = str(row_data.get(key, '')); pdf.cell(cell_width, 10, value, 1, 0, 'L')
            pdf.ln()
        temp_filepath = os.path.join(tempfile.gettempdir(), f"report_preview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        pdf.output(temp_filepath)
        webbrowser.open(f'file://{os.path.realpath(temp_filepath)}')
        return temp_filepath
    except Exception as e:
        messagebox.showerror("Error al Generar PDF", f"Ocurrió un error inesperado:\n{e}"); return None

# ==============================================================================
# NUEVA SECCIÓN DE REPORTLAB (PARA EL MANUAL)
# ==============================================================================
def export_manual_with_reportlab(manual_text, title='Manual de Usuario'):
    """
    Genera un PDF profesional del manual usando ReportLab y lo abre.
    """
    try:
        temp_dir = tempfile.gettempdir()
        temp_filepath = os.path.join(temp_dir, f"manual_preview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        
        # 1. Crear el documento PDF
        doc = SimpleDocTemplate(temp_filepath, pagesize=letter)
        
        # 2. Definir estilos de texto
        styles = getSampleStyleSheet()
        style_title = styles['Title']
        style_h1 = styles['h1']
        style_h2 = styles['h2']
        style_body = styles['BodyText']
        style_body.leading = 14 # Espacio entre líneas
        
        # 3. Construir la historia (el contenido del PDF)
        story = []

        # Añadir el logo
        try:
            logo_path = resource_path("images/logo_empresa.png")
            logo = Image(logo_path, width=2*inch, height=0.6*inch)
            logo.hAlign = 'LEFT'
            story.append(logo)
            story.append(Spacer(1, 0.25*inch))
        except Exception as e:
            print(f"No se pudo cargar el logo para el manual de ReportLab: {e}")

        # Procesar el texto y añadirlo a la historia con el formato correcto
        lines = manual_text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue # Ignorar líneas vacías
            
            if line.startswith('Sistema de Control'):
                story.append(Paragraph(line, style_title))
                story.append(Spacer(1, 0.2*inch))
            elif line.startswith('Versión 1.0'):
                story.append(Paragraph(line, styles['Normal']))
                story.append(Spacer(1, 0.5*inch))
            elif line.startswith('---'):
                continue # Usamos Spacers en su lugar
            elif re.match(r"^\d\.\d\.", line): # Subtítulo (e.g. 2.1.)
                story.append(Paragraph(line, style_h2))
                story.append(Spacer(1, 0.1*inch))
            elif re.match(r"^\d\.", line): # Título principal (e.g. 1.)
                story.append(Spacer(1, 0.2*inch))
                story.append(Paragraph(line, style_h1))
                story.append(Spacer(1, 0.1*inch))
            else:
                story.append(Paragraph(line, style_body))
        
        # 4. Generar el PDF
        doc.build(story)
        
        # 5. Abrir el PDF generado
        webbrowser.open(f'file://{os.path.realpath(temp_filepath)}')
        return temp_filepath

    except Exception as e:
        messagebox.showerror("Error al Generar PDF con ReportLab", f"Ocurrió un error inesperado:\n{e}")
        return None