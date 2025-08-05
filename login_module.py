# login_module.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # ¡Correcto, importar ttk para los otros widgets!
from db_connection import conectar_db
import main_menu
from PIL import Image, ImageTk
import mysql.connector

def crear_ventana_login():
    """Crea y muestra la ventana de inicio de sesión con imagen de fondo."""
    ventana_login = tk.Tk() # ¡CORREGIDO! Debe ser tk.Tk() para la ventana principal
    ventana_login.title("Inicio de Sesión - Frigorífico JPG Cermeño")
    ventana_login.geometry("550x650")
    ventana_login.resizable(False, False)

    # --- Configurar tema de ttk ---
    style = ttk.Style(ventana_login)
    style.theme_use('clam') # Puedes probar otros temas como 'alt', 'default', 'vista', 'xpnative'

    # --- Configurar la imagen de fondo ---
    try:
        imagen_original = Image.open("JPG.jpg") 
        ancho_ventana, alto_ventana = 550, 650
        imagen_redimensionada = imagen_original.resize((ancho_ventana, alto_ventana), Image.LANCZOS)
        imagen_fondo = ImageTk.PhotoImage(imagen_redimensionada)

        label_fondo = tk.Label(ventana_login, image=imagen_fondo) # tk.Label para el fondo
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        label_fondo.image = imagen_fondo 

    except FileNotFoundError:
        messagebox.showwarning("Advertencia", "No se encontró la imagen de fondo 'JPG.jpg'. Se usará un color de fondo.")
        ventana_login.configure(bg="#e0f2f7")
    except Exception as e:
        messagebox.showerror("Error de Imagen", f"Error al cargar la imagen de fondo: {e}. Se usará un color de fondo.")
        ventana_login.configure(bg="#e0f2f7")


    # --- Widgets de la Interfaz (colocados encima de la imagen de fondo) ---
    # Usaremos ttk.Frame para el contenedor de los campos de login
    contenido_frame = ttk.Frame(ventana_login, relief="groove")
    contenido_frame.place(relx=0.5, rely=0.5, anchor="center", width=250, height=250) 

    # Configurar el fondo de los Labels y el Frame para que coincida con el tema si es necesario
    # O para que se vea bien sobre la imagen
    # style.configure('TFrame', background='#e0f2f7') # Ejemplo de cómo configurar el fondo de un ttk.Frame por estilo
    # style.configure('TLabel', background='#e0f2f7') # Ejemplo de cómo configurar el fondo de un ttk.Label por estilo
    # Si el frame tiene un fondo sólido, no necesitas el background en los Labels internos si los Labels son transparentes al fondo del frame.

    ttk.Label(contenido_frame, text="Sistema de Inventario", font=("Arial", 14, "bold")).pack(pady=15)

    ttk.Label(contenido_frame, text="Username:", font=("Arial", 12)).pack(pady=2)
    entry_usuario = ttk.Entry(contenido_frame, font=("Arial", 12), width=20)
    entry_usuario.pack(pady=2)

    ttk.Label(contenido_frame, text="Password:", font=("Arial", 12)).pack(pady=2)
    entry_contrasena = ttk.Entry(contenido_frame, show="*", font=("Arial", 12), width=20)
    entry_contrasena.pack(pady=2)

    def iniciar_sesion_internal():
        usuario_ingresado = entry_usuario.get()
        contrasena_ingresada = entry_contrasena.get()

        if not usuario_ingresado or not contrasena_ingresada:
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id_usuario, nombre_completo, rol FROM usuario WHERE usuario = %s AND contrasena = %s",
                           (usuario_ingresado, contrasena_ingresada))
            resultado = cursor.fetchone()
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Consulta", f"Ocurrió un error al verificar las credenciales: {err}")
            resultado = None
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

        if resultado:
            rol = resultado['rol']
            nombre_completo = resultado['nombre_completo']
            id_usuario = resultado['id_usuario']
            messagebox.showinfo("Bienvenido", f"¡Bienvenido(a), {nombre_completo}! Rol: {rol}")
            ventana_login.withdraw()
            main_menu.abrir_menu_principal(rol, id_usuario, ventana_login) 
        else:
            messagebox.showerror("Error de Inicio de Sesión", "Usuario o contraseña incorrectos.")

    ttk.Button(contenido_frame, text="Iniciar Sesión", command=iniciar_sesion_internal,
               style="Accent.TButton").pack(pady=15)

    # Estilo para el botón (si tu tema 'clam' lo soporta bien, si no, puedes probar con otros valores)
    style.map('Accent.TButton',
        foreground=[('pressed', 'white'), ('active', 'white')],
        background=[('pressed', '!focus', "#913B02"), ('active', "#200D01")],
        relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
    style.configure('Accent.TButton', font=("Arial", 12, "bold"), padding=10, background="#411902", foreground='white')


    ventana_login.mainloop()

if __name__ == "__main__":
    crear_ventana_login()