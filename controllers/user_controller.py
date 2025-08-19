# controllers/user_controller.py
from tkinter import messagebox
import services.user_services as user_service

def handle_register_user(nombre_completo, usuario, contrasena, rol):
    """Maneja la lógica de validación y registro de un nuevo usuario."""
    if not all([nombre_completo, usuario, contrasena, rol]):
        messagebox.showwarning("Campos Incompletos", "Todos los campos son obligatorios.")
        return False

    success, message = user_service.add_user(nombre_completo, usuario, contrasena, rol)

    if success:
        messagebox.showinfo("Éxito", message)
        return True
    else:
        messagebox.showerror("Error de Registro", message)
        return False

def handle_find_user(username):
    """
    Maneja la búsqueda de un usuario. Es SILENCIOSO.
    Solo devuelve los datos o None.
    """
    if not username:
        return None
    user_data = user_service.get_user_by_username(username)
    return user_data

def handle_get_all_users():
    """Llama al servicio para obtener todos los usuarios."""
    return user_service.get_all_users()

def handle_update_user(user_id, nombre_completo, rol, nueva_contrasena):
    """Maneja la lógica de validación y actualización de un usuario."""
    if not nombre_completo or not rol:
        messagebox.showwarning("Campos Incompletos", "El nombre completo y el rol son obligatorios.")
        return False

    password_to_update = nueva_contrasena if nueva_contrasena else None
    success, message = user_service.update_user(user_id, nombre_completo, rol, password_to_update)

    if success:
        messagebox.showinfo("Éxito", message)
        return True
    else:
        messagebox.showerror("Error de Actualización", message)
        return False
        
def handle_deactivate_user(username):
    """Maneja la desactivación de un usuario."""
    if not username:
        messagebox.showwarning("Error", "No se ha proporcionado un nombre de usuario.")
        return False
        
    if not messagebox.askyesno("Confirmar Desactivación", f"¿Está seguro de que desea desactivar al usuario '{username}'?\nYa no podrá iniciar sesión."):
        return False

    success, message = user_service.deactivate_user_by_username(username)
    
    if success:
        messagebox.showinfo("Éxito", message)
        return True
    else:
        messagebox.showerror("Error", message)
        return False