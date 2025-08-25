# controllers/help_controller.py

from tkinter import messagebox
from utils import exporter

def handle_export_manual_as_pdf(manual_text):
    """
    Orquesta la generación del manual usando la nueva función de ReportLab.
    """
    try:
        # --- CORRECCIÓN DEFINITIVA ---
        # Llamamos a la nueva función que SÍ existe: 'export_manual_with_reportlab'
        exporter.export_manual_with_reportlab(manual_text, title='Manual de Usuario del Sistema')
        
        
    except Exception as e:
        messagebox.showerror("Error de Exportación", f"No se pudo exportar el manual.\n{e}")