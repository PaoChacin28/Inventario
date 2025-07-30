# main_menu.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk 
import mysql.connector 

# Importar módulos de gestión (asumimos que serán modificados para aceptar un frame padre)
import product_management
import user_management
import supplier_management
import movement_management
import report_generation

def clear_frame(frame):
    """Limpia todos los widgets dentro de un frame."""
    for widget in frame.winfo_children():
        widget.destroy()

def abrir_menu_principal(rol, id_usuario):
    menu = tk.Toplevel()
    menu.title("Sistema de Inventario - Menú Principal")
    
    # Adaptar el tamaño de la pantalla
    screen_width = menu.winfo_screenwidth()
    screen_height = menu.winfo_screenheight()

    window_width = int(screen_width * 0.8)
    window_height = int(screen_height * 0.8)

    x_pos = int((screen_width - window_width) / 2)
    y_pos = int((screen_height - window_height) / 2)

    menu.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

    style = ttk.Style(menu)
    style.theme_use('clam') 

    # --- Configurar la imagen de fondo ---
    try:
        # Asegúrate de tener una imagen de fondo para el menú principal, por ejemplo 'fondo_main.png'
        # ¡IMPORTANTE! Ajusta la ruta y el nombre del archivo de tu imagen
        imagen_original = Image.open("JPG.jpg") 
        imagen_redimensionada = imagen_original.resize((window_width, window_height), Image.LANCZOS)
        imagen_fondo = ImageTk.PhotoImage(imagen_redimensionada)

        label_fondo = tk.Label(menu, image=imagen_fondo)
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        label_fondo.image = imagen_fondo 

    except FileNotFoundError:
        messagebox.showwarning("Advertencia", "No se encontró la imagen de fondo 'fondo_main.png'. Se usará un color de fondo.")
        menu.configure(bg="#f0f8ff") 
    except Exception as e:
        messagebox.showerror("Error de Imagen", f"Error al cargar la imagen de fondo: {e}. Se usará un color de fondo.")
        menu.configure(bg="#f0f8ff") 

    # --- Creación de los Frames principales para la navegación vertical ---
    sidebar_width = 220 # Ancho fijo para la barra lateral

        # Sidebar Frame
    # Ahora con un background sólido y opaco (gris claro)
    style.configure('Sidebar.TFrame', background='#f0f0f0', borderwidth=0) 
    sidebar_frame = ttk.Frame(menu, width=sidebar_width, style='Sidebar.TFrame')
    sidebar_frame.pack(side="left", fill="y", padx=5, pady=5)
    sidebar_frame.pack_propagate(False) 

    # Main Content Frame
    # Ahora con un background sólido y opaco (blanco)
    style.configure('MainContent.TFrame', background="#f0f0f0", borderwidth=10) 
    main_content_frame = ttk.Frame(menu, style='MainContent.TFrame')
    main_content_frame.pack(side="right", fill="both", expand=True, padx=100, pady=100)

    # Estilos para los botones de la barra lateral
    style.configure('Sidebar.TButton', font=("Arial", 12, "bold"), padding=10, 
                    background="#ff0000", foreground='white') # Botones más vistosos
    style.map('Sidebar.TButton',
              background=[('active', "#770505")], # Color al pasar el ratón
              foreground=[('active', 'white')])

    # Estilo para los títulos y etiquetas dentro del main_content_frame
    # Asegúrate que el background de los Labels dentro del main_content_frame sea el mismo que el del frame
    style.configure('ContentTitle.TLabel', font=("Arial", 24, "bold"), padding=10, 
                    background='#f0f0f0', foreground='black') # Fondo blanco, texto negro
    style.configure('ContentLabel.TLabel', font=("Arial", 12), 
                    background='#f0f0f0', foreground='black') # Fondo blanco, texto negro


    # --- Funciones para mostrar contenido en el main_content_frame ---
    def show_welcome_screen():
        clear_frame(main_content_frame)
        ttk.Label(main_content_frame, text=f"Bienvenido(a), {rol}!", style='ContentTitle.TLabel').pack(pady=50)
        ttk.Label(main_content_frame, text="Selecciona una opción del menú lateral.", style='ContentLabel.TLabel').pack(pady=20)
        
    def show_product_management():
        clear_frame(main_content_frame)
        ttk.Label(main_content_frame, text="Gestión de Productos", style='ContentTitle.TLabel').pack(pady=20)
        
        # Aquí crearías los botones para las acciones de producto que se mostrarán en el content_frame
        # Estos botones llamarán a las funciones internas que has modificado en product_management.py
        product_buttons_frame = ttk.Frame(main_content_frame)
        product_buttons_frame.pack(pady=20)
        
        ttk.Button(product_buttons_frame, text="Registrar Producto", command=lambda: product_management.registrar_producto_internal(main_content_frame), style='Sidebar.TButton').pack(fill="x", pady=5)
        ttk.Button(product_buttons_frame, text="Consultar Producto Específico", command=lambda: product_management.consultar_producto_internal(main_content_frame), style='Sidebar.TButton').pack(fill="x", pady=5)
        ttk.Button(product_buttons_frame, text="Editar Producto", command=lambda: product_management.editar_producto_internal(main_content_frame), style='Sidebar.TButton').pack(fill="x", pady=5)
        ttk.Button(product_buttons_frame, text="Eliminar Producto", command=lambda: product_management.eliminar_producto_internal(main_content_frame), style='Sidebar.TButton').pack(fill="x", pady=5)
        

    def show_user_management():
        clear_frame(main_content_frame)
        ttk.Label(main_content_frame, text="Gestión de Usuarios", style='ContentTitle.TLabel').pack(pady=20)
        user_buttons_frame = ttk.Frame(main_content_frame)
        user_buttons_frame.pack(pady=20)
        ttk.Button(user_buttons_frame, text="Registrar Usuario", command=lambda: user_management.registrar_usuario_internal(main_content_frame), style='Sidebar.TButton').pack(fill="x", pady=5)
        ttk.Button(user_buttons_frame, text="Consultar Usuario", command=lambda: user_management.consultar_usuario_internal(main_content_frame), style='Sidebar.TButton').pack(fill="x", pady=5)
        ttk.Button(user_buttons_frame, text="Editar Usuario", command=lambda: user_management.editar_usuario_internal(main_content_frame), style='Sidebar.TButton').pack(fill="x", pady=5)
        ttk.Button(user_buttons_frame, text="Eliminar Usuario", command=lambda: user_management.eliminar_usuario_internal(main_content_frame), style='Sidebar.TButton').pack(fill="x", pady=5)

    def show_provider_management():
        clear_frame(main_content_frame)
        ttk.Label(main_content_frame, text="Gestión de Proveedores", style='ContentTitle.TLabel').pack(pady=20)
        provider_buttons_frame = ttk.Frame(main_content_frame)
        provider_buttons_frame.pack(pady=20)
        ttk.Button(provider_buttons_frame, text="Registrar Proveedor", command=lambda: supplier_management.registrar_proveedor_internal(main_content_frame), style='Sidebar.TButton').pack(fill="x", pady=5)
        ttk.Button(provider_buttons_frame, text="Consultar Proveedor", command=lambda: supplier_management.consultar_proveedor_internal(main_content_frame), style='Sidebar.TButton').pack(fill="x", pady=5)
        ttk.Button(provider_buttons_frame, text="Editar Proveedor", command=lambda: supplier_management.editar_proveedor_internal(main_content_frame), style='Sidebar.TButton').pack(fill="x", pady=5)
        ttk.Button(provider_buttons_frame, text="Eliminar Proveedor", command=lambda: supplier_management.eliminar_proveedor_internal(main_content_frame), style='Sidebar.TButton').pack(fill="x", pady=5)

    def show_movement_management():
        clear_frame(main_content_frame)
        ttk.Label(main_content_frame, text="Gestión de Movimientos", style='ContentTitle.TLabel').pack(pady=20)
        movement_buttons_frame = ttk.Frame(main_content_frame)
        movement_buttons_frame.pack(pady=20)
        ttk.Button(movement_buttons_frame, text="Registrar Movimiento", command=lambda: movement_management.registrar_movimiento_internal(main_content_frame, id_usuario), style='Sidebar.TButton').pack(fill="x", pady=5)
        ttk.Button(movement_buttons_frame, text="Consultar Inventario General", command=lambda: product_management.consultar_inventario_general_internal(main_content_frame), style='Sidebar.TButton').pack(fill="x", pady=5)
        
        
    def show_report_management():
        clear_frame(main_content_frame)
        ttk.Label(main_content_frame, text="Reportes", style='ContentTitle.TLabel').pack(pady=20)
        report_buttons_frame = ttk.Frame(main_content_frame)
        report_buttons_frame.pack(pady=20)
        ttk.Button(report_buttons_frame, text="Generar Reporte", command=lambda: report_generation.generar_reporte_internal(main_content_frame, id_usuario), style='Sidebar.TButton').pack(fill="x", pady=5)


    # --- Botones de la barra lateral ---
    ttk.Button(sidebar_frame, text="Inicio", command=show_welcome_screen, style='Sidebar.TButton').pack(fill="x", pady=5, padx=5)
    ttk.Button(sidebar_frame, text="Productos", command=show_product_management, style='Sidebar.TButton').pack(fill="x", pady=5, padx=5)
    
    if rol == "Administrador":
        ttk.Button(sidebar_frame, text="Usuarios", command=show_user_management, style='Sidebar.TButton').pack(fill="x", pady=5, padx=5)
        ttk.Button(sidebar_frame, text="Proveedores", command=show_provider_management, style='Sidebar.TButton').pack(fill="x", pady=5, padx=5)
    
    ttk.Button(sidebar_frame, text="Movimientos", command=show_movement_management, style='Sidebar.TButton').pack(fill="x", pady=5, padx=5)
    ttk.Button(sidebar_frame, text="Reportes", command=show_report_management, style='Sidebar.TButton').pack(fill="x", pady=5, padx=5)
    ttk.Button(sidebar_frame, text="Cerrar Sesión", command=menu.destroy, style='Sidebar.TButton').pack(fill="x", pady=15, padx=5) # Botón para salir

    # Mostrar la pantalla de bienvenida al inicio
    show_welcome_screen()

    menu.mainloop()