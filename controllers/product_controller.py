# controllers/product_controller.py
from tkinter import messagebox
import services.product_services as product_service
from utils import validation

def _validate_product_definition(data):
    """Valida los datos de definición de un producto."""
    required_fields = ['codigo_producto', 'nombre', 'tipo']
    if any(not data.get(field) for field in required_fields):
        messagebox.showwarning("Campos Incompletos", "Código, Nombre y Tipo son obligatorios.")
        return None
    return data

def handle_add_product(data):
    """
    Maneja la creación de la definición de un producto.
    CORRECCIÓN: Ahora devuelve el ID del nuevo producto si tiene éxito.
    """
    validated_data = _validate_product_definition(data)
    if not validated_data:
        # La validación ya muestra un messagebox si falla
        return (False, None)
    # --- NUEVA VALIDACIÓN DE FORMATO ---
    if not validation.is_valid_product_code(data['codigo_producto']):
        messagebox.showerror("Formato Incorrecto", "El formato del Código de Producto es inválido.\nEjemplo: CAR-001")
        return None
    # ------------------------------------
    
    # El servicio 'add_product' devuelve (True, nuevo_id)
    success, result = product_service.add_product(**validated_data)
    
    if success:
        # No mostramos messagebox aquí, la vista se encargará del mensaje final
        return (True, result) # Retornamos True y el nuevo ID del producto
    else:
        # Si el servicio falla, sí mostramos el error
        messagebox.showerror("Error de Registro", result)
        return (False, None)

def handle_update_product(product_id, data):
    """Maneja la actualización de la definición de un producto."""
    if not data.get('nombre') or not data.get('tipo'):
        messagebox.showwarning("Campos Incompletos", "Nombre y Tipo son obligatorios.")
        return False
        
    success, message = product_service.update_product(product_id, data['nombre'], data['tipo'])
    if success:
        messagebox.showinfo("Éxito", message)
        return True
    else:
        messagebox.showerror("Error de Actualización", message)
        return False

def handle_find_product(code):
    if not code: return None
    return product_service.get_product_by_code(code)

def handle_get_all_products_with_stock():
    return product_service.get_all_products_with_stock()

def handle_deactivate_product(code):
    """Maneja la desactivación (borrado lógico) de un producto."""
    if not code:
        messagebox.showwarning("Error", "No se ha proporcionado un código de producto.")
        return False
        
    if not messagebox.askyesno("Confirmar Desactivación", f"¿Seguro que desea desactivar el producto con código '{code}'?\nNo podrá ser usado en nuevos lotes."):
        return False
        
    success, message = product_service.deactivate_product_by_code(code)
    
    if success:
        messagebox.showinfo("Éxito", message)
        return True
    else:
        messagebox.showerror("Error", message)
        return False

def handle_get_providers_for_product(product_id):
    return product_service.get_providers_for_product(product_id)

def handle_associate_provider(product_id, provider_id):
    if not product_id or not provider_id:
        messagebox.showwarning("Datos incompletos", "Se requiere un producto y un proveedor.")
        return False
    success, message = product_service.associate_provider_to_product(product_id, provider_id)
    if not success: messagebox.showerror("Error", message)
    return success

def handle_disassociate_provider(product_id, provider_id):
    if not product_id or not provider_id: return False
    if not messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar el vínculo con este proveedor?"):
        return False
    success, message = product_service.disassociate_provider_from_product(product_id, provider_id)
    if success: messagebox.showinfo("Éxito", message); return True
    else: messagebox.showerror("Error", message); return False