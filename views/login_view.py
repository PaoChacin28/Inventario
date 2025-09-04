# views/login_view.py

import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector

from utils.db_connection import conectar_db
from utils import styles
from utils.validation import resource_path 
from views import main_view

def _verify_credentials(username, password):
    """
    Verifica las credenciales en la base de datos en varios pasos para dar mensajes específicos.
    Retorna una tupla (ESTADO, DATOS_O_MENSAJE).
    """
    db = conectar_db()
    if not db:
        return ('DB_ERROR', "No se pudo conectar a la base de datos.")
    
    cursor = db.cursor(dictionary=True)
    try:
        # Paso 1: Buscar al usuario SOLO por su nombre de usuario.
        query = "SELECT id_usuario, nombre_completo, rol, contrasena, estado FROM usuario WHERE usuario = %s"
        cursor.execute(query, (username,))
        user_data = cursor.fetchone()

        # Caso 1: El usuario no existe.
        if not user_data:
            return ('NOT_FOUND', "Usuario o contraseña incorrectos.")

        # Caso 2: La contraseña es incorrecta.
        if user_data['contrasena'] != password:
            return ('WRONG_PASS', "Usuario o contraseña incorrectos.")

        # Caso 3: El usuario está inactivo.
        if user_data['estado'] == 'Inactivo':
            return ('INACTIVE', "Este usuario ha sido desactivado. Por favor, contacte al administrador.")
            
        # Si todo está bien, el inicio de sesión es exitoso.
        return ('SUCCESS', user_data)

    except mysql.connector.Error as err:
        return ('DB_ERROR', f"Ocurrió un error al verificar credenciales: {err}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def create_login_window():
    """Crea y muestra la ventana de inicio de sesión."""
    login_window = tk.Tk()
    login_window.title("Inicio de Sesión - Sistema de Inventario")
    
    # Se configuran los estilos una sola vez al inicio de la aplicación.
    styles.configure_styles(login_window)
    
    login_window.geometry("550x650")
    login_window.resizable(False, False)

    try:
        # Usamos resource_path para que la imagen funcione en el .exe
        img_path = resource_path("images/JPG.jpg")
        bg_image = ImageTk.PhotoImage(Image.open(img_path).resize((550, 650), Image.LANCZOS))
        bg_label = tk.Label(login_window, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_image
    except Exception as e:
        print(f"Advertencia: No se pudo cargar la imagen de fondo. Error: {e}")
        login_window.configure(bg="#e0f2f7")

    # Frame para el contenido del formulario
    content_frame = tk.Frame(login_window, bg="white", relief="groove", bd=2)
    content_frame.place(relx=0.5, rely=0.5, anchor="center", width=250, height=250)
    
    ttk.Label(content_frame, text="Sistema de Inventario", font=("Arial", 14, "bold"), background="white").pack(pady=(20, 10))
    ttk.Label(content_frame, text="Usuario:", font=("Arial", 12), background="white").pack(pady=(1,0))
    user_entry = ttk.Entry(content_frame, font=("Arial", 12), width=20)
    user_entry.pack(pady=1, padx=20)
    ttk.Label(content_frame, text="Contraseña:", font=("Arial", 12), background="white").pack(pady=(1,0))
    pass_entry = ttk.Entry(content_frame, show="*", font=("Arial", 12), width=20)
    pass_entry.pack(pady=1, padx=20)

    # Función interna para limpiar los campos, se pasará como referencia.
    def clear_login_fields():
        user_entry.delete(0, tk.END)
        pass_entry.delete(0, tk.END)
        user_entry.focus_set()

    # Función que maneja el evento de clic o "Enter".
    def login_action(event=None):
        username = user_entry.get().strip()
        password = pass_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
            return

        status, result = _verify_credentials(username, password)
        
        if status == 'SUCCESS':
            user_data = result
            login_window.unbind('<Return>') # Desactivar "Enter" para evitar re-logins
            login_window.withdraw()
            
            # Pasamos todas las referencias necesarias a la ventana principal
            main_view.create_main_menu_window(
                rol=user_data['rol'], 
                user_id=user_data['id_usuario'], 
                login_window_ref=login_window, 
                login_action_ref=login_action,
                clear_login_fields_ref=clear_login_fields
            )
        elif status == 'INACTIVE':
            messagebox.showerror("Acceso Denegado", result)
        else:
            messagebox.showerror("Error de Inicio de Sesión", result)

    # Creación del botón y vinculación del evento "Enter"
    login_button = ttk.Button(content_frame, text="Iniciar Sesión", command=login_action, style='Accent.TButton')
    login_button.pack(pady=20)
    login_window.bind('<Return>', login_action)
    
    # Foco inicial para una mejor experiencia de usuario
    user_entry.focus_set()

    login_window.mainloop()