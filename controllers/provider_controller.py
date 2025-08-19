# controllers/provider_controller.py
from tkinter import messagebox
import services.provider_services as provider_service
from utils import validation

def handle_add_provider(nombre, rif, telefono, direccion):
    """Maneja la validación y el registro, deteniéndose si hay errores."""
    if not nombre or not rif:
        messagebox.showwarning("Campos Incompletos", "El Nombre y el RIF son campos obligatorios.")
        return False # <-- DETENER EJECUCIÓN

    if not validation.is_valid_rif(rif):
        messagebox.showerror("Formato Incorrecto", "El formato del RIF es inválido.\nDebe ser J-12345678-9.")
        return False # <-- DETENER EJECUCIÓN

    success, message = provider_service.add_provider(nombre, rif, telefono, direccion)
    if success:
        messagebox.showinfo("Éxito", message)
        return True
    else:
        messagebox.showerror("Error de Registro", message)
        return False

def handle_update_provider(provider_id, nombre, rif, telefono, direccion):
    """Maneja la validación y la actualización, deteniéndose si hay errores."""
    if not nombre or not rif:
        messagebox.showwarning("Campos Incompletos", "El Nombre y el RIF son obligatorios.")
        return False # <-- DETENER EJECUCIÓN

    if not validation.is_valid_rif(rif):
        messagebox.showerror("Formato Incorrecto", "El formato del RIF es inválido.\nDebe ser J-12345678-9.")
        return False # <-- DETENER EJECUCIÓN
    
    success, message = provider_service.update_provider(provider_id, nombre, rif, telefono, direccion)
    if success:
        messagebox.showinfo("Éxito", message)
        return True
    else:
        messagebox.showerror("Error de Actualización", message)
        return False

def handle_find_provider(rif):
    """Maneja la búsqueda de un proveedor (silenciosa)."""
    if not rif: return None
    return provider_service.get_provider_by_rif(rif)

def handle_get_all_providers():
    """Maneja la obtención de todos los proveedores activos."""
    return provider_service.get_all_providers()

def handle_deactivate_provider(rif):
    """Maneja la desactivación de un proveedor."""
    if not rif:
        # Esto no debería ocurrir si se selecciona de la tabla, pero es una buena práctica
        messagebox.showwarning("Error", "No se ha proporcionado un RIF.")
        return False
        
    if not messagebox.askyesno("Confirmar Desactivación", f"¿Está seguro de que desea desactivar al proveedor con RIF '{rif}'?\nYa no podrá ser usado en operaciones nuevas."):
        return False

    # Llamada a la función correcta del servicio
    success, message = provider_service.deactivate_provider_by_rif(rif)
    
    if success:
        messagebox.showinfo("Éxito", message)
        return True
    else:
        messagebox.showerror("Error", message)
        return False
    
def handle_get_providers_for_selection():
    """
    Pasa la llamada al servicio para obtener la lista de proveedores
    para los combobox.
    """
    return provider_service.get_providers_for_selection()