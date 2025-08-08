# views/main_view.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Importar TODAS las vistas que se mostrarán en el menú
from views import user_view, provider_view, product_view, movement_view, report_view

# Variables globales para esta vista
main_content_frame = None
submenu_data_dict = {}

def _clear_frame(frame):
    for widget in frame.winfo_children(): widget.destroy()

def _toggle_submenu(target_frame, target_button):
    for frame, _ in submenu_data_dict.values():
        if frame == target_frame and not frame.winfo_ismapped():
            frame.pack(fill="x", pady=(0, 5), padx=5, after=target_button)
        else:
            frame.pack_forget()

def _show_welcome_screen(current_rol):
    _clear_frame(main_content_frame)
    try:
        img_path = "images/logo_empresa.png"
        logo_img = ImageTk.PhotoImage(Image.open(img_path).resize((350, 150), Image.LANCZOS))
        logo_label = ttk.Label(main_content_frame, image=logo_img, style='ContentBackground.TLabel')
        logo_label.image = logo_img
        logo_label.pack(pady=(50, 20))
    except Exception as e:
        print(f"No se pudo cargar el logo de la empresa: {e}")

    ttk.Label(main_content_frame, text=f"Bienvenido(a), {current_rol}!", style='ContentTitle.TLabel').pack(pady=10)
    ttk.Label(main_content_frame, text="Selecciona una opción del menú lateral para comenzar.", style='ContentLabel.TLabel').pack(pady=20)

def create_main_menu_window(rol, user_id, login_window_ref):
    global main_content_frame, submenu_data_dict
    
    main_window = tk.Toplevel(login_window_ref)
    main_window.title("Sistema de Inventario - Menú Principal")
    main_window.state('zoomed')

    # --- YA NO SE NECESITA CONFIGURAR ESTILOS AQUÍ ---
    # El bloque `style = ttk.Style(main_window)` y todas las
    # llamadas a `style.configure` y `style.map` han sido eliminadas.
    # Los estilos ya están cargados en la aplicación.

    # --- Layout principal con Grid ---
    main_window.grid_columnconfigure(1, weight=1)
    main_window.grid_rowconfigure(0, weight=1)

    # --- Barra Lateral (Sidebar) ---
    sidebar_frame = ttk.Frame(main_window, width=230, style='Sidebar.TFrame')
    sidebar_frame.grid(row=0, column=0, sticky="ns", padx=5, pady=5)
    sidebar_frame.grid_propagate(False)

    # --- Contenido Principal ---
    main_content_frame = ttk.Frame(main_window, style='MainContent.TFrame')
    main_content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # --- Creación de Menús y Submenús ---
    submenu_data_dict = {}

    def add_menu_button(text, command):
        btn = ttk.Button(sidebar_frame, text=text, command=command, style='Sidebar.TButton')
        btn.pack(fill="x", pady=5, padx=5)
        return btn

    def add_submenu_button(parent_frame, text, command):
        ttk.Button(parent_frame, text=text, command=command, style='Submenu.TButton').pack(fill="x", pady=1, padx=15)
    
    # --- BOTONES (El resto del código es igual) ---
    add_menu_button("Inicio", lambda: _show_welcome_screen(rol))

    products_submenu = ttk.Frame(sidebar_frame, style='Sidebar.TFrame')
    btn_prod = add_menu_button("Productos", lambda: _toggle_submenu(products_submenu, btn_prod))
    submenu_data_dict["prod"] = (products_submenu, btn_prod)
    add_submenu_button(products_submenu, "Registrar", lambda: product_view.show_register_product_form(main_content_frame))
    add_submenu_button(products_submenu, "Editar/Consultar", lambda: product_view.show_edit_product_form(main_content_frame))
    add_submenu_button(products_submenu, "Eliminar", lambda: product_view.show_delete_product_form(main_content_frame))
    
    inv_submenu = ttk.Frame(sidebar_frame, style='Sidebar.TFrame')
    btn_inv = add_menu_button("Inventario", lambda: _toggle_submenu(inv_submenu, btn_inv))
    submenu_data_dict["inv"] = (inv_submenu, btn_inv)
    add_submenu_button(inv_submenu, "Registrar Movimiento", lambda: movement_view.show_register_movement_form(main_content_frame, user_id))
    add_submenu_button(inv_submenu, "Historial Movimientos", lambda: movement_view.show_all_movements_list(main_content_frame))
    add_submenu_button(inv_submenu, "Stock General", lambda: movement_view.show_general_inventory_list(main_content_frame))

    if rol == "Administrador":
        users_submenu = ttk.Frame(sidebar_frame, style='Sidebar.TFrame')
        btn_users = add_menu_button("Usuarios", lambda: _toggle_submenu(users_submenu, btn_users))
        submenu_data_dict["users"] = (users_submenu, btn_users)
        add_submenu_button(users_submenu, "Registrar", lambda: user_view.show_register_user_form(main_content_frame))
        add_submenu_button(users_submenu, "Editar/Consultar", lambda: user_view.show_edit_user_form(main_content_frame))
        add_submenu_button(users_submenu, "Eliminar", lambda: user_view.show_delete_user_form(main_content_frame))
        add_submenu_button(users_submenu, "Listado General", lambda: user_view.show_all_users_list(main_content_frame))

        prov_submenu = ttk.Frame(sidebar_frame, style='Sidebar.TFrame')
        btn_prov = add_menu_button("Proveedores", lambda: _toggle_submenu(prov_submenu, btn_prov))
        submenu_data_dict["prov"] = (prov_submenu, btn_prov)
        add_submenu_button(prov_submenu, "Registrar", lambda: provider_view.show_register_provider_form(main_content_frame))
        add_submenu_button(prov_submenu, "Editar/Consultar", lambda: provider_view.show_edit_provider_form(main_content_frame))
        add_submenu_button(prov_submenu, "Eliminar", lambda: provider_view.show_delete_provider_form(main_content_frame))
        add_submenu_button(prov_submenu, "Listado General", lambda: provider_view.show_all_providers_list(main_content_frame))
        
        rep_submenu = ttk.Frame(sidebar_frame, style='Sidebar.TFrame')
        btn_rep = add_menu_button("Reportes", lambda: _toggle_submenu(rep_submenu, btn_rep))
        submenu_data_dict["rep"] = (rep_submenu, btn_rep)
        add_submenu_button(rep_submenu, "Generar Reporte", lambda: report_view.show_generate_report_form(main_content_frame, user_id))

    def logout_action():
        main_window.destroy()
        login_window_ref.deiconify()
    
    add_menu_button("Cerrar Sesión", logout_action)

    for frame, _ in submenu_data_dict.values(): frame.pack_forget()
    _show_welcome_screen(rol)

    main_window.protocol("WM_DELETE_WINDOW", logout_action)