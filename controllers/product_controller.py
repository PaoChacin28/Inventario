# controllers/product_controller.py
from tkinter import messagebox
import services.product_services as product_service

def _validate_and_convert_data(data):
    """Valida los datos de definición de un producto."""
    required_fields = ['codigo_producto', 'nombre', 'tipo', 'id_proveedor']
    if any(not data.get(field) for field in required_fields):
        messagebox.showwarning("Campos Incompletos", "Código, Nombre, Tipo y Proveedor son obligatorios.")
        return None
    try:
        validated_data = {
            'codigo_producto': data['codigo_producto'],
            'nombre': data['nombre'],
            'tipo': data['tipo'],
            'id_proveedor': int(data['id_proveedor'])
        }
        return validated_data
    except (ValueError, TypeError):
        messagebox.showerror("Error de Formato", "El ID de Proveedor debe ser un número válido.")
        return None

def handle_add_product(data):
    validated_data = _validate_and_convert_data(data)
    if not validated_data: return False
    success, message = product_service.add_product(**validated_data)
    if success: messagebox.showinfo("Éxito", message); return True
    else: messagebox.showerror("Error de Registro", message); return False

def handle_find_product(code):
    if not code: return None
    return product_service.get_product_by_code(code)

def handle_update_product(product_id, data):
    # (Similar a add, pero sin 'codigo_producto')
    pass

def handle_delete_product(code):
    if not code: messagebox.showwarning("Campo Vacío", "Ingrese un código de producto a eliminar."); return False
    if not messagebox.askyesno("Confirmar Eliminación", f"¿Seguro que desea eliminar el producto '{code}'? Esto eliminará todos sus lotes y movimientos asociados."): return False
    success, message = product_service.delete_product_by_code(code)
    if success: messagebox.showinfo("Éxito", message); return True
    else: messagebox.showerror("Error de Eliminación", message); return False

def handle_get_all_products_with_stock():
    return product_service.get_all_products_with_stock()