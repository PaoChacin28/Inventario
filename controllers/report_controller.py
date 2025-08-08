
# controllers/report_controller.py
from tkinter import messagebox
import services.report_services as report_service

def handle_generate_report(report_type, user_id):
    """
    Orquesta la generación de reportes: obtiene datos, los registra y maneja la retroalimentación.
    Retorna los datos del reporte (lista de diccionarios) o None si falla la conexión.
    """
    if not report_type:
        messagebox.showwarning("Selección Incompleta", "Por favor, seleccione un tipo de reporte.")
        return None

    report_data = None
    if report_type == "Stock mínimo":
        report_data = report_service.get_low_stock_report_data()
    elif report_type == "Productos Por Vencer":
        report_data = report_service.get_expiring_soon_report_data()
    else:
        messagebox.showerror("Error", "Tipo de reporte no reconocido.")
        return None

    # Si la conexión a la DB falló en el servicio
    if report_data is None:
        messagebox.showerror("Error de Base de Datos", "No se pudieron obtener los datos para el reporte.")
        return None
    
    # Si la consulta fue exitosa pero no arrojó resultados
    if not report_data:
        messagebox.showinfo("Reporte Vacío", f"No se encontraron productos para el reporte de '{report_type}'.")
    
    # Siempre intentamos registrar la generación del reporte
    log_success = report_service.log_report_generation(report_type, user_id)
    if not log_success:
        messagebox.showwarning("Advertencia", "El reporte fue generado pero no se pudo registrar la operación.")

    # Finalmente, notificamos que se generó (incluso si está vacío)
    if report_data is not None:
         messagebox.showinfo("Reporte Generado", f"El reporte de '{report_type}' ha sido generado.")

    return report_data