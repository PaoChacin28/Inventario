# main_menu.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk 
import mysql.connector 

# Importar módulos de gestión
import product_management
import user_management
import supplier_management
import movement_management
import report_generation

# Variables globales para acceder a los frames y el rol desde cualquier función
global sidebar_frame
global main_content_frame
global current_rol
global current_id_usuario
global menu_window 
global submenu_data_dict 

# Variable global para almacenar la referencia a la ventana de login
global login_window_ref 
login_window_ref = None # Inicialmente a None

def clear_frame(frame):
    """Limpia todos los widgets dentro de un frame."""
    for widget in frame.winfo_children():
        widget.destroy()

# --- Funciones para manejar la visibilidad de los submenús (Estilo Acordeón) ---
def toggle_submenu_visibility(target_submenu_frame, target_parent_button):
    """
    Expande el submenú objetivo si está oculto, o lo contrae si está visible.
    Contrae todos los demás submenús.
    """
    global submenu_data_dict
    
    for name, (frame, parent_button) in submenu_data_dict.items():
        if frame == target_submenu_frame:
            if frame.winfo_ismapped(): # Si el target_submenu_frame está visible, lo ocultamos
                frame.pack_forget()
            else:
                # Pack con 'after' cada vez que se hace visible
                frame.pack(fill="x", pady=(0, 5), padx=5, after=target_parent_button) 
        else:
            # Ocultamos cualquier otro submenú que pueda estar abierto
            if frame.winfo_ismapped():
                frame.pack_forget()

# --- Funciones para mostrar contenido en el main_content_frame ---
def show_welcome_screen():
    clear_frame(main_content_frame)
    
    # Asegúrate de que 'logo_empresa.png' sea el nombre de tu archivo de logo
    logo_path = "logo_empresa.png" 
    try:
        # Abre la imagen del logo
        logo_original = Image.open(logo_path)
        # Redimensiona el logo si es necesario (ajusta el tamaño a tu gusto)
        logo_redimensionado = logo_original.resize((350, 150), Image.LANCZOS) 
        # Convierte para Tkinter
        global app_logo_tk # Necesitas mantener una referencia global
        app_logo_tk = ImageTk.PhotoImage(logo_redimensionado)

        # Crea una etiqueta para mostrar el logo y la empaqueta
        ttk.Label(main_content_frame, image=app_logo_tk, style='ContentBackground.TLabel').pack(pady=(50, 20)) 
    except FileNotFoundError:
        messagebox.showwarning("Advertencia", f"No se encontró el archivo del logo '{logo_path}'. Asegúrate de que esté en la misma carpeta.")
    except Exception as e:
        messagebox.showerror("Error al cargar logo", f"Error al cargar el logo: {e}.")

    ttk.Label(main_content_frame, text=f"Bienvenido(a), {current_rol}!", style='ContentTitle.TLabel').pack(pady=10)
    ttk.Label(main_content_frame, text="Selecciona una opción del menú lateral.", style='ContentLabel.TLabel').pack(pady=20)

# Función para manejar el cierre de sesión
def logout():
    global menu_window, login_window_ref
    if menu_window:
        menu_window.destroy() # Cierra la ventana del menú principal
    if login_window_ref:
        login_window_ref.deiconify() # Muestra la ventana de login (si estaba oculta)
        login_window_ref.lift() # Asegura que la ventana de login esté al frente

# Modificación: la función ahora acepta un parámetro login_win
def abrir_menu_principal(rol, id_usuario, login_win): 
    global sidebar_frame, main_content_frame, current_rol, current_id_usuario, menu_window, submenu_data_dict, login_window_ref
    
    current_rol = rol 
    current_id_usuario = id_usuario 
    login_window_ref = login_win # Guardar la referencia a la ventana de login

    menu_window = tk.Toplevel() 
    menu_window.title("Sistema de Inventario - Menú Principal")
    
    screen_width = menu_window.winfo_screenwidth()
    screen_height = menu_window.winfo_screenheight()

    window_width = int(screen_width * 0.8)
    window_height = int(screen_height * 0.8)

    x_pos = int((screen_width - window_width) / 2)
    y_pos = int((screen_height - window_height) / 2)

    menu_window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

    style = ttk.Style(menu_window)
    style.theme_use('clam') 

    # --- Configurar las columnas y filas para que sean responsivas con grid ---
    menu_window.grid_columnconfigure(0, weight=0) 
    menu_window.grid_columnconfigure(1, weight=1) 
    menu_window.grid_rowconfigure(0, weight=1)

    # --- Creación de los Frames principales ---
    sidebar_width = 220 

    # Sidebar Frame
    style.configure('Sidebar.TFrame', background="#924904", borderwidth=0) 
    sidebar_frame = ttk.Frame(menu_window, width=sidebar_width, style='Sidebar.TFrame')
    sidebar_frame.grid(row=0, column=0, sticky="ns", padx=5, pady=5) 
    sidebar_frame.grid_propagate(False) 

    # Main Content Frame
    style.configure('MainContent.TFrame', background='#ffffff', borderwidth=0) 
    main_content_frame = ttk.Frame(menu_window, style='MainContent.TFrame')
    main_content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10) 

    # Estilos para los botones de la barra lateral (principales)
    style.configure('Sidebar.TButton', font=("Arial", 12, "bold"), padding=10, 
                    background="#913B02", foreground='white') 
    style.map('Sidebar.TButton',
              background=[('active', "#411902")], 
              foreground=[('active', 'white')])

    # Estilos para los botones de las subopciones (diferente padding/fuente, un poco más pequeños)
    style.configure('Submenu.TButton', font=("Arial", 10), padding=8, 
                    background="#411902", foreground='white') 
    style.map('Submenu.TButton',
              background=[('active', "#180901")], 
              foreground=[('active', 'white')])

    # Estilos para los títulos y etiquetas dentro del main_content_frame
    style.configure('ContentTitle.TLabel', font=("Arial", 24, "bold"), padding=10, 
                    background='#ffffff', foreground='black') 
    style.configure('ContentLabel.TLabel', font=("Arial", 12), 
                    background='#ffffff', foreground='black') 
    
    # --- Estilos adicionales para los botones de acción en los sub-módulos ---
    style.configure('Accent.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#007BFF", foreground='white', borderwidth=0, relief="flat") 
    style.map('Accent.TButton', background=[('active', "#0056b3")])

    style.configure('Search.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#2196F3", foreground='white', borderwidth=0, relief="flat") 
    style.map('Search.TButton', background=[('active', "#0B7CDA")])

    style.configure('Action.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#4CAF50", foreground='white', borderwidth=0, relief="flat") 
    style.map('Action.TButton', background=[('active', "#45A049")])

    style.configure('Delete.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#f44336", foreground='white', borderwidth=0, relief="flat") 
    style.map('Delete.TButton', background=[('active', "#DA190B")])

    # Estilo para los backgrounds de los frames de contenido (en main_content_frame)
    style.configure('ContentBackground.TLabel', background='#ffffff')
    style.configure('MainContent.TFrame', background='#ffffff') # Ya estaba, pero reiteramos para claridad.

    # --- Definición de los frames de los submenús ---
    submenu_data_dict = {} # Ahora almacena (frame_del_submenu, boton_principal_asociado)

    # Inicio button always visible
    ttk.Button(sidebar_frame, text="Inicio", 
               command=show_welcome_screen, style='Sidebar.TButton').pack(fill="x", pady=5, padx=5)
    
    # --- Productos y su submenú (ACCESIBLE PARA AMBOS ROLES) ---
    btn_productos = ttk.Button(sidebar_frame, text="Productos", 
                               command=lambda: toggle_submenu_visibility(products_submenu_frame, btn_productos), 
                               style='Sidebar.TButton')
    btn_productos.pack(fill="x", pady=5, padx=5)

    products_submenu_frame = ttk.Frame(sidebar_frame, style='Sidebar.TFrame')
    submenu_data_dict["products"] = (products_submenu_frame, btn_productos)

    ttk.Button(products_submenu_frame, text="Registrar Producto", 
               command=lambda: [clear_frame(main_content_frame), product_management.registrar_producto_internal(main_content_frame)], 
               style='Submenu.TButton').pack(fill="x", pady=1, padx=15)
    ttk.Button(products_submenu_frame, text="Consultar Producto", 
               command=lambda: [clear_frame(main_content_frame), product_management.consultar_producto_internal(main_content_frame)], 
               style='Submenu.TButton').pack(fill="x", pady=1, padx=15)
    ttk.Button(products_submenu_frame, text="Editar Producto", 
               command=lambda: [clear_frame(main_content_frame), product_management.editar_producto_internal(main_content_frame)], 
               style='Submenu.TButton').pack(fill="x", pady=1, padx=15)
    ttk.Button(products_submenu_frame, text="Eliminar Producto", 
               command=lambda: [clear_frame(main_content_frame), product_management.eliminar_producto_internal(main_content_frame)], 
               style='Submenu.TButton').pack(fill="x", pady=1, padx=15)


    # --- Inventario y su submenú (ACCESIBLE PARA AMBOS ROLES) ---
    btn_inventario = ttk.Button(sidebar_frame, text="Inventario", 
                                command=lambda: toggle_submenu_visibility(movements_submenu_frame, btn_inventario), 
                                style='Sidebar.TButton')
    btn_inventario.pack(fill="x", pady=5, padx=5)

    movements_submenu_frame = ttk.Frame(sidebar_frame, style='Sidebar.TFrame')
    submenu_data_dict["movements"] = (movements_submenu_frame, btn_inventario) 
    # Botones de subopción para Inventario
    ttk.Button(movements_submenu_frame, text="Registrar Movimiento", 
               command=lambda: [clear_frame(main_content_frame), movement_management.registrar_movimiento_internal(main_content_frame, current_id_usuario)], 
               style='Submenu.TButton').pack(fill="x", pady=1, padx=15) 
    ttk.Button(movements_submenu_frame, text="Consultar Movimientos", 
               command=lambda: [clear_frame(main_content_frame), movement_management.consultar_movimientos_internal(main_content_frame)],
               style='Submenu.TButton').pack(fill="x", pady=1, padx=15)
    ttk.Button(movements_submenu_frame, text="Consultar Inventario General", 
               command=lambda: [clear_frame(main_content_frame), movement_management.consultar_inventario_general_internal(main_content_frame)], 
               style='Submenu.TButton').pack(fill="x", pady=1, padx=15)

    # --- Secciones de Administrador (condicionales) ---
    if current_rol == "Administrador":
        # --- Usuarios y su submenú ---
        btn_usuarios = ttk.Button(sidebar_frame, text="Usuarios", 
                                  command=lambda: toggle_submenu_visibility(users_submenu_frame, btn_usuarios), 
                                  style='Sidebar.TButton')
        btn_usuarios.pack(fill="x", pady=5, padx=5)

        users_submenu_frame = ttk.Frame(sidebar_frame, style='Sidebar.TFrame')
        submenu_data_dict["users"] = (users_submenu_frame, btn_usuarios)
        ttk.Button(users_submenu_frame, text="Registrar Usuario", 
                   command=lambda: [clear_frame(main_content_frame), user_management.registrar_usuario_internal(main_content_frame)], 
                   style='Submenu.TButton').pack(fill="x", pady=1, padx=15)
        ttk.Button(users_submenu_frame, text="Consultar Usuario", 
                   command=lambda: [clear_frame(main_content_frame), user_management.consultar_usuario_internal(main_content_frame)], 
                   style='Submenu.TButton').pack(fill="x", pady=1, padx=15)
        ttk.Button(users_submenu_frame, text="Editar Usuario", 
                   command=lambda: [clear_frame(main_content_frame), user_management.editar_usuario_internal(main_content_frame)], 
                   style='Submenu.TButton').pack(fill="x", pady=1, padx=15)
        ttk.Button(users_submenu_frame, text="Eliminar Usuario", 
                   command=lambda: [clear_frame(main_content_frame), user_management.eliminar_usuario_internal(main_content_frame)], 
                   style='Submenu.TButton').pack(fill="x", pady=1, padx=15)
        ttk.Button(users_submenu_frame, text="Consultar Listado General",
                   command=lambda: [clear_frame(main_content_frame), user_management.consultar_usuarios_general_internal(main_content_frame)],
                   style='Submenu.TButton').pack(fill="x", pady=1, padx=15)


        # --- Proveedores y su submenú ---
        btn_proveedores = ttk.Button(sidebar_frame, text="Proveedores", 
                                     command=lambda: toggle_submenu_visibility(providers_submenu_frame, btn_proveedores), 
                                     style='Sidebar.TButton')
        btn_proveedores.pack(fill="x", pady=5, padx=5)

        providers_submenu_frame = ttk.Frame(sidebar_frame, style='Sidebar.TFrame')
        submenu_data_dict["providers"] = (providers_submenu_frame, btn_proveedores)
        ttk.Button(providers_submenu_frame, text="Registrar Proveedor", 
                   command=lambda: [clear_frame(main_content_frame), supplier_management.registrar_proveedor_internal(main_content_frame)], 
                   style='Submenu.TButton').pack(fill="x", pady=1, padx=15)
        ttk.Button(providers_submenu_frame, text="Consultar Proveedor", 
                   command=lambda: [clear_frame(main_content_frame), supplier_management.consultar_proveedor_internal(main_content_frame)], 
                   style='Submenu.TButton').pack(fill="x", pady=1, padx=15)
        ttk.Button(providers_submenu_frame, text="Editar Proveedor", 
                   command=lambda: [clear_frame(main_content_frame), supplier_management.editar_proveedor_internal(main_content_frame)], 
                   style='Submenu.TButton').pack(fill="x", pady=1, padx=15)
        ttk.Button(providers_submenu_frame, text="Eliminar Proveedor", 
                   command=lambda: [clear_frame(main_content_frame), supplier_management.eliminar_proveedor_internal(main_content_frame)], 
                   style='Submenu.TButton').pack(fill="x", pady=1, padx=15)
        ttk.Button(providers_submenu_frame, text="Consultar Listado General",
                   command=lambda: [clear_frame(main_content_frame), supplier_management.consultar_proveedores_general_internal(main_content_frame)],
                   style='Submenu.TButton').pack(fill="x", pady=1, padx=15)

        # --- Reportes y su submenú ---
        btn_reportes = ttk.Button(sidebar_frame, text="Reportes", 
                                  command=lambda: toggle_submenu_visibility(reports_submenu_frame, btn_reportes), 
                                  style='Sidebar.TButton')
        btn_reportes.pack(fill="x", pady=5, padx=5)

        reports_submenu_frame = ttk.Frame(sidebar_frame, style='Sidebar.TFrame')
        submenu_data_dict["reports"] = (reports_submenu_frame, btn_reportes)
        ttk.Button(reports_submenu_frame, text="Generar Reporte", 
                   command=lambda: [clear_frame(main_content_frame), report_generation.generar_reporte_internal(main_content_frame, current_id_usuario)], 
                   style='Submenu.TButton').pack(fill="x", pady=1, padx=15)
    
    # "Cerrar Sesión" button
    # El comando ahora llama a la nueva función `logout`
    ttk.Button(sidebar_frame, text="Cerrar Sesión", 
               command=logout, style='Sidebar.TButton').pack(fill="x", pady=15, padx=5) 

    # Inicialmente, ocultar todos los submenús
    for frame, _ in submenu_data_dict.values():
        frame.pack_forget()

    # Mostrar la pantalla de bienvenida al inicio
    show_welcome_screen()

    # Configurar el protocolo de cierre de ventana para también mostrar el login
    menu_window.protocol("WM_DELETE_WINDOW", logout)

    menu_window.mainloop()