# controllers/movement_controller.py
from tkinter import messagebox
import services.movement_services as movement_service
import services.product_services as product_service # Lo usamos para la vista de inventario general

def handle_get_products_for_selection():
    """Obtiene los productos para mostrarlos en el combobox de la vista."""
    return movement_service.get_products_for_selection()

def handle_register_movement(product_id, movement_type, quantity_str, user_id):
    """Valida la entrada y orquesta el registro de un movimiento."""
    if not all([product_id, movement_type, quantity_str]):
        messagebox.showwarning("Campos Incompletos", "Debe seleccionar un producto, tipo y cantidad.")
        return False
        
    try:
        quantity = int(quantity_str)
        if quantity <= 0:
            messagebox.showerror("Valor Inválido", "La cantidad debe ser un número entero positivo.")
            return False
    except ValueError:
        messagebox.showerror("Formato Inválido", "La cantidad debe ser un número entero.")
        return False

    success, message = movement_service.register_inventory_movement(product_id, movement_type, quantity, user_id)
    
    if success:
        messagebox.showinfo("Éxito", message)
        return True
    else:
        messagebox.showerror("Error en la Operación", message)
        return False

def handle_get_all_movements():
    """Obtiene la lista de todos los movimientos."""
    return movement_service.get_all_movements_with_details()

def handle_get_general_inventory():
    """Obtiene la lista de todos los productos para la vista de inventario."""
    # Reutilizamos el servicio de productos ya que es la misma consulta
    return product_service.get_all_products()