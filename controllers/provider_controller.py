# controllers/provider_controller.py
from tkinter import messagebox
import services.provider_services as provider_service

def handle_get_providers_for_selection():
    """Obtiene la lista de proveedores para poblar un Combobox en la vista."""
    return provider_service.get_providers_for_selection()

def handle_add_provider(nombre, rif, telefono, direccion):
    """Maneja la validación y el registro de un nuevo proveedor."""
    if not nombre or not rif:
        messagebox.showwarning("Campos Incompletos", "El Nombre y el RIF son campos obligatorios.")
        return False

    success, message = provider_service.add_provider(nombre, rif, telefono, direccion)

    if success:
        messagebox.showinfo("Éxito", message)
        return True
    else:
        messagebox.showerror("Error de Registro", message)
        return False

def handle_find_provider(rif):
    """Maneja la búsqueda de un proveedor y retorna sus datos."""
    if not rif:
        messagebox.showwarning("Campo Vacío", "Por favor, ingrese el RIF a buscar.")
        return None
    
    provider_data = provider_service.get_provider_by_rif(rif)
    
    if provider_data:
        messagebox.showinfo("Proveedor Encontrado", f"Datos de '{provider_data['nombre']}' cargados.")
    else:
        messagebox.showwarning("No Encontrado", f"No se encontró un proveedor con el RIF '{rif}'.")
        
    return provider_data

def handle_get_all_providers():
    """Maneja la obtención de todos los proveedores."""
    return provider_service.get_all_providers()

def handle_update_provider(provider_id, nombre, rif, telefono, direccion):
    """Maneja la validación y actualización de un proveedor."""
    if not nombre or not rif:
        messagebox.showwarning("Campos Incompletos", "El Nombre y el RIF son campos obligatorios.")
        return False

    success, message = provider_service.update_provider(provider_id, nombre, rif, telefono, direccion)

    if success:
        messagebox.showinfo("Éxito", message)
        return True
    else:
        messagebox.showerror("Error de Actualización", message)
        return False

def handle_delete_provider(rif):
    """Maneja la confirmación y eliminación de un proveedor."""
    if not rif:
        messagebox.showwarning("Campo Vacío", "Por favor, ingrese el RIF a eliminar.")
        return False
        
    if not messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar al proveedor con RIF '{rif}'?"):
        return False

    success, message = provider_service.delete_provider_by_rif(rif)

    if success:
        messagebox.showinfo("Éxito", message)
        return True
    else:
        messagebox.showerror("Error de Eliminación", message)
        return False