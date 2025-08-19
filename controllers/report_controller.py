# controllers/report_controller.py
from tkinter import messagebox
import services.report_services as report_service
import services.movement_services as movement_service
import services.provider_services as provider_service

def get_report_data(report_type, params):
    """Función central que llama al servicio correcto y valida los parámetros."""
    try:
        if report_type == "Movimientos por Fecha":
            if not params.get('start_date') or not params.get('end_date'): return None
            return report_service.get_movements_by_date_range(params['start_date'], params['end_date'])
            
        elif report_type == "Trazabilidad de Lote":
            if not params.get('lote_id'):
                messagebox.showwarning("Filtro Requerido", "Por favor, seleccione un lote para generar el reporte.")
                return None
            return report_service.get_lot_traceability_report(params['lote_id'])
            
        elif report_type == "Movimientos por Producto":
            if not params.get('product_id'):
                messagebox.showwarning("Filtro Requerido", "Por favor, seleccione un producto para generar el reporte.")
                return None
            return report_service.get_movements_by_product(params['product_id'], params['start_date'], params['end_date'])
            
        elif report_type == "Entradas por Proveedor":
            if not params.get('provider_id'):
                messagebox.showwarning("Filtro Requerido", "Por favor, seleccione un proveedor para generar el reporte.")
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

# Funciones para poblar los filtros
def get_products_for_selection():
    return movement_service.get_products_for_selection()
def get_active_lots_for_selection():
    return movement_service.get_active_lots_for_selection()
def get_providers_for_selection():
    return provider_service.get_providers_for_selection()