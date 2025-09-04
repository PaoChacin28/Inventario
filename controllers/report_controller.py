# controllers/report_controller.py

from tkinter import messagebox
import services.report_services as report_service
import services.movement_services as movement_service
import services.provider_services as provider_service
from utils import exporter

def get_report_data(report_type, params):
    """
    Función central que llama al servicio correcto para obtener los datos del reporte.
    """
    try:
        # --- NUEVO REPORTE AÑADIDO ---
        if report_type == "Stock General":
            return report_service.get_full_stock_report_data()
            
        elif report_type == "Movimientos por Fecha":
            if not params.get('start_date') or not params.get('end_date'):
                messagebox.showwarning("Filtro Requerido", "Por favor, seleccione una fecha de inicio y fin.")
                return None
            return report_service.get_movements_by_date_range(params['start_date'], params['end_date'])
            
        elif report_type == "Trazabilidad de Lote":
            if not params.get('lote_id'):
                messagebox.showwarning("Filtro Requerido", "Por favor, seleccione un lote.")
                return None
            return report_service.get_lot_traceability_report(params['lote_id'])
            
        elif report_type == "Movimientos por Producto":
            if not all(params.get(k) for k in ['product_id', 'start_date', 'end_date']):
                messagebox.showwarning("Filtros Requeridos", "Por favor, seleccione producto, fecha de inicio y fin.")
                return None
            return report_service.get_movements_by_product(params['product_id'], params['start_date'], params['end_date'])
            
        elif report_type == "Entradas por Proveedor":
            if not all(params.get(k) for k in ['provider_id', 'start_date', 'end_date']):
                messagebox.showwarning("Filtros Requeridos", "Por favor, seleccione proveedor, fecha de inicio y fin.")
                return None
            return report_service.get_entries_by_provider(params['provider_id'], params['start_date'], params['end_date'])
        
        elif report_type == "Stock Mínimo":
            return report_service.get_low_stock_report_data()
            
        elif report_type == "Próximos a Vencer":
            return report_service.get_expiring_soon_report_data()
            
        else:
            messagebox.showerror("Error", f"Tipo de reporte no reconocido: {report_type}")
            return None
            
    except Exception as e:
        messagebox.showerror("Error en Controlador", f"Ocurrió un error al procesar la solicitud del reporte:\n{e}")
        return None

# --- Funciones para poblar los filtros de la vista ---
def get_products_for_selection():
    return movement_service.get_products_for_selection()

def get_active_lots_for_selection():
    return movement_service.get_active_lots_for_selection()

def get_providers_for_selection():
    return provider_service.get_providers_for_selection()

# --- Funciones para el flujo de PDF (sin cambios) ---
def handle_preview_report(data, headers, title):
    """
    (CORREGIDO) Genera y visualiza un reporte en PDF usando las nuevas funciones.
    """
    # 1. Llama a la función que genera los datos del PDF en memoria
    pdf_data = exporter.generate_report_pdf_data(data, headers, title)
    
    # 2. Llama a la función que previsualiza esos datos
    exporter.preview_pdf_from_data(pdf_data)

def handle_save_report(data, headers, title):
    """
    (CORREGIDO) Genera y guarda un reporte en PDF usando las nuevas funciones.
    """
    # 1. Llama a la función que genera los datos del PDF en memoria
    pdf_data = exporter.generate_report_pdf_data(data, headers, title)
    
    # 2. Llama a la función que guarda esos datos
    exporter.save_pdf_from_data(pdf_data, default_filename=title.replace(" ", "_"))