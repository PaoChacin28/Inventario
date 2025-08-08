# views/login_view.py
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector

# Importaciones corregidas según la nueva estructura de carpetas
from utils.db_connection import conectar_db
from utils import styles # Importamos el módulo de estilos para que se carguen al inicio
from views import main_view

def _verify_credentials(username, password):
    """
    Función interna para verificar las credenciales en la base de datos.
    Retorna un diccionario con los datos del usuario o None si falla.
    """
    db = conectar_db()
    if not db:
        messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos.")
        return None
    
    cursor = db.cursor(dictionary=True)
    try:
        query = "SELECT id_usuario, nombre_completo, rol FROM usuario WHERE usuario = %s AND contrasena = %s"
        cursor.execute(query, (username, password))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Consulta", f"Ocurrió un error al verificar credenciales: {err}")
        return None
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def create_login_window():
    """Crea y muestra la ventana de inicio de sesión."""
    login_window = tk.Tk()
    login_window.title("Inicio de Sesión - Sistema de Inventario")
    
    # Llamamos a la configuración de estilos UNA SOLA VEZ al inicio de la app.
    styles.configure_styles(login_window)
    
    login_window.geometry("550x650")
    login_window.resizable(False, False)

    # --- Configurar la imagen de fondo ---
    try:
        # La ruta a la imagen ahora parte de la carpeta raíz del proyecto
        img_path = "images/JPG.jpg"
        bg_image = ImageTk.PhotoImage(Image.open(img_path).resize((550, 650), Image.LANCZOS))
        bg_label = tk.Label(login_window, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_image # Mantener referencia para evitar que el recolector de basura la elimine
    except Exception as e:
        print(f"Advertencia: No se pudo cargar la imagen de fondo. Error: {e}")
        login_window.configure(bg="#e0f2f7")

    # --- Frame para el contenido del login ---
    # Usamos un Frame normal para poder controlar mejor el background sobre la imagen.
    content_frame = tk.Frame(login_window, bg="white", relief="groove", bd=2)
    
    # --- ¡CORRECCIÓN IMPORTANTE! APLICAMOS TAMAÑO FIJO Y CENTRADO ---
    content_frame.place(relx=0.5, rely=0.5, anchor="center", width=250, height=250)
    # ----------------------------------------------------------------

    # Widgets dentro del frame. Usamos bg="white" para que no sean transparentes.
    ttk.Label(content_frame, text="Sistema de Inventario", font=("Arial", 14, "bold"), background="white").pack(pady=(20, 10))

    ttk.Label(content_frame, text="Usuario:", font=("Arial", 12), background="white").pack(pady=(1,0))
    user_entry = ttk.Entry(content_frame, font=("Arial", 12), width=20)
    user_entry.pack(pady=1, padx=20)

    ttk.Label(content_frame, text="Contraseña:", font=("Arial", 12), background="white").pack(pady=(1,0))
    pass_entry = ttk.Entry(content_frame, show="*", font=("Arial", 12), width=20)
    pass_entry.pack(pady=1, padx=20)

    def login_action():
        username = user_entry.get().strip()
        password = pass_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
            return

        user_data = _verify_credentials(username, password)
        
        if user_data:
            login_window.withdraw()
            main_view.create_main_menu_window(user_data['rol'], user_data['id_usuario'], login_window)
        else:
            messagebox.showerror("Error de Inicio de Sesión", "Usuario o contraseña incorrectos.")

    # El estilo 'Accent.TButton' fue definido en styles.py
    login_button = ttk.Button(content_frame, text="Iniciar Sesión", command=login_action, style='Accent.TButton')
    login_button.pack(pady=20)

    login_window.mainloop()