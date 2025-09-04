# views/main_view.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from views import user_view, provider_view, product_view, movement_view, report_view
from views import help_view
from utils.validation import resource_path

content_frame = None

def _clear_frame(frame):
    for widget in frame.winfo_children(): widget.destroy()

def create_main_menu_window(rol, user_id, login_window_ref, login_action_ref, clear_login_fields_ref):
    global content_frame
    
    main_window = tk.Toplevel(login_window_ref)
    main_window.title("Sistema de Inventario - Menú Principal")
    main_window.state('zoomed')

    main_window.grid_columnconfigure(1, weight=1)
    main_window.grid_rowconfigure(0, weight=1)

    sidebar_frame = ttk.Frame(main_window, width=230, style='Sidebar.TFrame')
    sidebar_frame.grid(row=0, column=0, sticky="ns", padx=5, pady=5)
    sidebar_frame.grid_propagate(False)

    # --- NUEVA ESTRUCTURA DE LAYOUT CON GRID ---
    main_area = ttk.Frame(main_window, style='MainContent.TFrame')
    main_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    
    main_area.rowconfigure(1, weight=1)
    main_area.columnconfigure(0, weight=1)

    header_frame = ttk.Frame(main_area, style='MainContent.TFrame', height=60)
    header_frame.grid(row=0, column=0, sticky="ew")
    header_frame.grid_propagate(False)

    content_frame = ttk.Frame(main_area, style='MainContent.TFrame')
    content_frame.grid(row=1, column=0, sticky="nsew")
    
    # --- LÓGICA DEL LOGO PEQUEÑO ---
    try:
        logo_path = resource_path("images/logo_empresa.png")
        logo_original = Image.open(logo_path)
        logo_redimensionado = logo_original.resize((150, 50), Image.LANCZOS)
        logo_tk = ImageTk.PhotoImage(logo_redimensionado)
        logo_label = ttk.Label(header_frame, image=logo_tk, style='ContentBackground.TLabel')
        logo_label.image = logo_tk
        logo_label.pack(side='right', padx=10)
    except Exception as e:
        print(f"No se pudo cargar el logo para el header: {e}")

    # --- FUNCIONES DE CONTROL DEL HEADER ---
    def show_header():
        header_frame.grid()

    def hide_header():
        header_frame.grid_remove()

    # --- FUNCIONES DE NAVEGACIÓN ---
    def _show_welcome_screen(current_rol):
        hide_header()
        _clear_frame(content_frame)
        try:
            img_path = resource_path("images/logo_empresa.png")
            logo_img_grande = ImageTk.PhotoImage(Image.open(img_path).resize((350, 150), Image.LANCZOS))
            logo_label_grande = ttk.Label(content_frame, image=logo_img_grande, style='ContentBackground.TLabel')
            logo_label_grande.image = logo_img_grande
            logo_label_grande.pack(pady=(50, 20))
        except Exception as e:
            print(f"No se pudo cargar el logo de la empresa: {e}")
        ttk.Label(content_frame, text=f"Bienvenido(a), {current_rol}!", style='ContentTitle.TLabel').pack(pady=10)
        ttk.Label(content_frame, text="Selecciona una opción del menú lateral para comenzar.", style='ContentLabel.TLabel').pack(pady=20)

    def navigate_to_products():
        show_header()
        product_view.show_all_products_list(content_frame)

    def navigate_to_movements():
        show_header()
        movement_view.show_all_movements_list(parent_frame=content_frame, user_id=user_id)
        
    def navigate_to_users():
        show_header()
        user_view.show_all_users_list(content_frame)

    def navigate_to_providers():
        show_header()
        provider_view.show_all_providers_list(content_frame)

    def navigate_to_reports():
        show_header()
        report_view.show_generate_report_form(content_frame, user_id)

    # --- BOTONES DEL MENÚ ---
    def add_menu_button(text, command):
        ttk.Button(sidebar_frame, text=text, command=command, style='Sidebar.TButton').pack(fill="x", pady=5, padx=5)
    
    add_menu_button("Inicio", lambda: _show_welcome_screen(rol))
    add_menu_button("Productos", navigate_to_products)
    add_menu_button("Movimientos", navigate_to_movements)
    
    if rol == "Administrador":
        add_menu_button("Usuarios", navigate_to_users)
        add_menu_button("Proveedores", navigate_to_providers)
        add_menu_button("Reportes", navigate_to_reports)
        add_menu_button("Manual de Usuario", lambda: help_view.show_full_manual_in_frame(content_frame))

    # NOTA: Asegúrate de que tu help_view tenga una función show_help_manual (o renómbrala a show_help_popup)
    add_menu_button("Ayuda", lambda: help_view.show_help_manual(main_window))
    
    # --- CAMBIO 2: LÓGICA DE CIERRE DE SESIÓN ACTUALIZADA ---
    def logout_action():
        main_window.destroy()
        
        # Primero, limpiamos los campos de la ventana de login.
        clear_login_fields_ref()
        
        # Luego, mostramos la ventana ya limpia.
        login_window_ref.deiconify()
        
        # Y finalmente, re-vinculamos la tecla Enter.
        login_window_ref.bind('<Return>', login_action_ref)
    
    add_menu_button("Cerrar Sesión", logout_action)

    # --- Estado Inicial ---
    _show_welcome_screen(rol)
    main_window.protocol("WM_DELETE_WINDOW", logout_action)