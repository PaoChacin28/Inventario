# controllers/movement_controller.py
from tkinter import messagebox
import services.movement_services as movement_service

def handle_get_products_for_selection():
    return movement_service.get_products_for_selection()

def handle_get_active_lots_for_selection():
    return movement_service.get_active_lots_for_selection()

def handle_get_lots_for_product(product_id):
    if not product_id: return []
    return movement_service.get_lots_for_product(product_id)

def handle_register_entry(data):
    """Valida y registra una nueva entrada de lote, recibiendo un diccionario de datos."""
    required = ['product_id', 'tag_lote', 'cantidad', 'unidad', 'user_id']
    if any(data.get(field) is None for field in required):
        messagebox.showwarning("Campos Incompletos", "Producto, Tag del Lote, Cantidad y Unidad son obligatorios.")
        return False
    try:
        cantidad = float(data['cantidad'])
        if cantidad <= 0: raise ValueError()
        data['cantidad'] = cantidad
    except (ValueError, TypeError):
        messagebox.showerror("Error de Formato", "La cantidad debe ser un número positivo.")
        return False
    
    success, message = movement_service.register_entry_movement(**data)
    if success:
        messagebox.showinfo("Éxito", message)
        return True
    else:
        messagebox.showerror("Error al Registrar Lote", message)
        return False

def handle_register_exit_or_adjustment(id_lote, cantidad_str, user_id, movement_type, descripcion):
    """Valida y registra una salida o un ajuste de un lote."""
    if not all([id_lote, cantidad_str]):
        messagebox.showwarning("Campos Incompletos", "Debe seleccionar un lote y especificar la cantidad.")
        return False
        
    if movement_type == 'Ajuste' and not descripcion:
        messagebox.showwarning("Descripción Requerida", "Para un 'Ajuste', la descripción es obligatoria.")
        return False

    try:
        cantidad = float(cantidad_str)
        if movement_type == 'Salida' and cantidad <= 0:
            messagebox.showerror("Valor Inválido", "La cantidad para una Salida debe ser un número positivo.")
            return False
    except ValueError:
        messagebox.showerror("Formato Inválido", "La cantidad debe ser un número (puede ser negativo para ajustes).")
        return False
        
    if movement_type == 'Salida':
        success, message = movement_service.register_exit_movement(id_lote, cantidad, user_id)
    else: # Es un Ajuste
        success, message = movement_service.register_adjustment_movement(id_lote, cantidad, user_id, descripcion)

    if success:
        messagebox.showinfo("Éxito", message)
        return True
    else:
        messagebox.showerror("Error en la Operación", message)
        return False

def handle_get_all_movements():
    return movement_service.get_all_movements_with_details()