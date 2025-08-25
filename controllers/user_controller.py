# controllers/user_controller.py

from tkinter import messagebox
import services.user_services as user_service
# --- 1. IMPORTAMOS LA NUEVA FUNCIÓN ---
from utils.validation import is_valid_password

def handle_register_user(nombre_completo, usuario, contrasena, rol):
    """Maneja la lógica de validación y registro de un nuevo usuario."""
    if not all([nombre_completo, usuario, contrasena, rol]):
        messagebox.showwarning("Campos Incompletos", "Todos los campos son obligatorios.")
        return False

    # --- 2. AÑADIMOS EL BLOQUE DE VALIDACIÓN DE CONTRASEÑA ---
    if not is_valid_password(contrasena):
        messagebox.showerror("Contraseña Inválida",
                             "La contraseña no cumple con los requisitos de formato:\n\n"
                             "- Mínimo 8 caracteres\n"
                             "- Al menos una letra mayúscula (A-Z)\n"
                             "- Al menos una letra minúscula (a-z)\n"
                             "- Al menos un número (0-9)")
        return False
    # --- FIN DE LA NUEVA VALIDACIÓN ---

    success, message = user_service.add_user(nombre_completo, usuario, contrasena, rol)

    if success:
        messagebox.showinfo("Éxito", message)
        return True
    else:
        messagebox.showerror("Error de Registro", message)
        return False

def handle_find_user(username):
    """Busca un usuario. Es silencioso."""
    if not username:
        return None
    return user_service.get_user_by_username(username)

def handle_get_all_users():
    """Llama al servicio para obtener todos los usuarios."""
    return user_service.get_all_users()

def handle_update_user(user_id, nombre_completo, rol, nueva_contrasena):
    """Maneja la lógica de validación y actualización de un usuario."""
    if not nombre_completo or not rol:
        messagebox.showwarning("Campos Incompletos", "El nombre completo y el rol son obligatorios.")
        return False

    password_to_update = None
    # Solo validamos la contraseña si el usuario ha escrito una nueva
    if nueva_contrasena:
        # --- 3. AÑADIMOS LA MISMA VALIDACIÓN AQUÍ ---
        if not is_valid_password(nueva_contrasena):
            messagebox.showerror("Contraseña Inválida",
                                 "La nueva contraseña no cumple con los requisitos:\n\n"
                                 "- Mínimo 8 caracteres\n"
                                 "- Al menos una letra mayúscula (A-Z)\n"
                                 "- Al menos una letra minúscula (a-z)\n"
                                 "- Al menos un número (0-9)")
            return False
        # --- FIN DE LA NUEVA VALIDACIÓN ---
        password_to_update = nueva_contrasena

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