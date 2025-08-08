# controllers/product_controller.py
from tkinter import messagebox
from datetime import datetime
import services.product_services as product_service

def _validate_and_convert_data(data):
    # CORRECCIÓN: 'precio' eliminado de la lista de campos requeridos.
    required_fields = [
        'codigo_producto', 'nombre', 'tipo', 'unidad_medida', 
        'fecha_ingreso', 'fecha_vencimiento', 'cantidad', 'id_proveedor'
    ]
    if any(not data.get(field) for field in required_fields):
        messagebox.showwarning("Campos Incompletos", "Todos los campos del formulario son obligatorios.")
        return None
    try:
        # CORRECCIÓN: 'precio' eliminado del diccionario de datos validados.
        validated_data = {
            'codigo_producto': data['codigo_producto'], 'nombre': data['nombre'], 'tipo': data['tipo'],
            'unidad_medida': data['unidad_medida'],
            'fecha_ingreso': datetime.strptime(data['fecha_ingreso'], "%Y-%m-%d").date(),
            'fecha_vencimiento': datetime.strptime(data['fecha_vencimiento'], "%Y-%m-%d").date(),
            'cantidad': float(data['cantidad']),
            'id_proveedor': int(data['id_proveedor'])
        }
        # CORRECCIÓN: Eliminada la regla de negocio que validaba el precio.
        if validated_data['cantidad'] < 0: raise ValueError("La cantidad no puede ser un número negativo.")
        if validated_data['fecha_vencimiento'] < validated_data['fecha_ingreso']:
            raise ValueError("La fecha de vencimiento no puede ser anterior a la de ingreso.")
        return validated_data
    except (ValueError, TypeError) as e:
        messagebox.showerror("Error de Formato", f"Error en el formato de los datos: {e}")
        return None

# El resto de las funciones handle_... usan _validate_and_convert_data,
# por lo que se adaptan automáticamente y no necesitan cambios.
def handle_add_product(data):
    validated_data = _validate_and_convert_data(data)
    if not validated_data: return False
    success, message = product_service.add_product(**validated_data)
    if success: messagebox.showinfo("Éxito", message); return True
    else: messagebox.showerror("Error de Registro", message); return False

def handle_find_product(code):
    if not code: messagebox.showwarning("Campo Vacío", "Ingrese un código de producto para buscar."); return None
    product_data = product_service.get_product_by_code(code)
    if product_data: messagebox.showinfo("Producto Encontrado", f"Datos de '{product_data['nombre']}' cargados.")
    else: messagebox.showwarning("No Encontrado", f"No se encontró producto con código '{code}'.")
    return product_data

def handle_update_product(product_id, data):
    validated_data = _validate_and_convert_data(data)
    if not validated_data: return False
    validated_data.pop('codigo_producto', None)
    success, message = product_service.update_product(product_id, **validated_data)
    if success: messagebox.showinfo("Éxito", message); return True
    else: messagebox.showerror("Error de Actualización", message); return False

def handle_delete_product(code):
    if not code: messagebox.showwarning("Campo Vacío", "Ingrese un código de producto a eliminar."); return False
    if not messagebox.askyesno("Confirmar Eliminación", f"¿Seguro que desea eliminar el producto con código '{code}'?"): return False
    success, message = product_service.delete_product_by_code(code)
    if success: messagebox.showinfo("Éxito", message); return True
    else: messagebox.showerror("Error de Eliminación", message); return False

def handle_get_all_products():
    return product_service.get_all_products()