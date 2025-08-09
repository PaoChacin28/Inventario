# views/user_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import controllers.user_controller as user_controller

def clear_frame(frame):
    """Limpia todos los widgets de un frame."""
    for widget in frame.winfo_children(): widget.destroy()

def show_register_user_form(parent_frame):
    """Dibuja el formulario para registrar un nuevo usuario."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Registrar Nuevo Usuario", style='ContentTitle.TLabel').pack(pady=20)
    
    form_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    form_frame.pack(padx=20, pady=10, fill="x", anchor="n")
    form_frame.columnconfigure(0, weight=1)
    
    fields_container = ttk.Frame(form_frame, style='MainContent.TFrame')
    fields_container.grid(row=0, column=0, sticky="n", ipadx=150)

    entries = {}
    field_labels = {"nombre_completo": "Nombre Completo", "usuario": "Nombre de Usuario", 
                    "contrasena": "Contraseña", "rol": "Rol"}

    for key, label_text in field_labels.items():
        field_frame = ttk.Frame(fields_container, style='MainContent.TFrame')
        field_frame.pack(fill="x", pady=5)
        ttk.Label(field_frame, text=label_text, style='ContentLabel.TLabel').pack(anchor="w")
        
        widget = None
        if key == "rol": widget = ttk.Combobox(field_frame, values=["Administrador", "Operador"], state="readonly"); widget.set("Operador")
        elif key == "contrasena": widget = ttk.Entry(field_frame, show="*")
        else: widget = ttk.Entry(field_frame)
        
        widget.pack(fill="x")
        entries[key] = widget

    def guardar_action():
        if user_controller.handle_register_user(
            nombre_completo=entries['nombre_completo'].get().strip(),
            usuario=entries['usuario'].get().strip(),
            contrasena=entries['contrasena'].get().strip(),
            rol=entries['rol'].get()
        ):
            show_all_users_list(parent_frame)

    button_frame = ttk.Frame(form_frame, style='MainContent.TFrame')
    button_frame.grid(row=1, column=0, pady=20)
    ttk.Button(button_frame, text="Guardar Usuario", command=guardar_action, style='Action.TButton').pack(side='left', padx=5)
    ttk.Button(button_frame, text="Cancelar", command=lambda: show_all_users_list(parent_frame), style='Delete.TButton').pack(side='left', padx=5)

def show_edit_user_form(parent_frame, username_to_edit):
    """Dibuja el formulario para editar un usuario específico."""
    clear_frame(parent_frame)
    user_data = user_controller.handle_find_user(username_to_edit)
    if not user_data:
        messagebox.showerror("Error", f"No se encontraron datos para el usuario '{username_to_edit}'.")
        show_all_users_list(parent_frame)
        return
        
    ttk.Label(parent_frame, text=f"Editando Usuario: {user_data['nombre_completo']}", style='ContentTitle.TLabel').pack(pady=20)
    
    form_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    form_frame.pack(padx=20, pady=10, fill="x", anchor="n")
    form_frame.columnconfigure(0, weight=1)
    
    fields_container = ttk.Frame(form_frame, style='MainContent.TFrame')
    fields_container.grid(row=0, column=0, sticky="n", ipadx=150)

    entries = {}
    field_labels = {"nombre_completo": "Nombre Completo", "rol": "Rol", 
                    "contrasena": "Nueva Contraseña (dejar en blanco para no cambiar)"}

    for key, label_text in field_labels.items():
        field_frame = ttk.Frame(fields_container, style='MainContent.TFrame')
        field_frame.pack(fill="x", pady=5)
        ttk.Label(field_frame, text=label_text, style='ContentLabel.TLabel').pack(anchor="w")
        
        widget = None
        if key == "rol": widget = ttk.Combobox(field_frame, values=["Administrador", "Operador"], state="readonly")
        elif key == "contrasena": widget = ttk.Entry(field_frame, show="*")
        else: widget = ttk.Entry(field_frame)
        
        if key != "contrasena": widget.insert(0, user_data.get(key, ''))
        if key == "rol": widget.set(user_data.get(key, 'Operador'))
        
        widget.pack(fill="x")
        entries[key] = widget
            
    def actualizar_action():
        if user_controller.handle_update_user(
            user_id=user_data['id_usuario'],
            nombre_completo=entries['nombre_completo'].get().strip(),
            rol=entries['rol'].get(),
            nueva_contrasena=entries['contrasena'].get().strip()
        ):
            show_all_users_list(parent_frame)

    button_frame = ttk.Frame(form_frame, style='MainContent.TFrame')
    button_frame.grid(row=1, column=0, pady=20)
    ttk.Button(button_frame, text="Actualizar Usuario", command=actualizar_action, style='Action.TButton').pack(side='left', padx=5)
    ttk.Button(button_frame, text="Cancelar", command=lambda: show_all_users_list(parent_frame), style='Delete.TButton').pack(side='left', padx=5)

def show_all_users_list(parent_frame):
    """Dibuja la vista principal de usuarios: lista, filtro y botones de acción."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Gestión de Usuarios", style='ContentTitle.TLabel').pack(pady=10)
    
    search_bar_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    search_bar_frame.pack(fill='x', padx=10, pady=5)
    ttk.Label(search_bar_frame, text="Filtrar:", style='ContentLabel.TLabel').pack(side='left', padx=(0, 5))
    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_bar_frame, textvariable=search_var)
    search_entry.pack(side='left', fill='x', expand=True)

    container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    container.pack(fill="both", expand=True, padx=10, pady=10)
    
    # --- CORRECCIÓN DE COLUMNAS ---
    cols = ("Nombre Completo", "Usuario", "Rol")
    tree = ttk.Treeview(container, columns=cols, show="headings", selectmode="browse")
    for col in cols: tree.heading(col, text=col)
    
    # Ahora la configuración de columna coincide con la definición
    tree.column("Nombre Completo", width=300)
    tree.column("Usuario", width=150)
    tree.column("Rol", width=120)
    
    vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.pack(side="left", fill="both", expand=True)

    action_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    action_frame.pack(side='bottom', pady=(5,0), fill='x')
    hsb = ttk.Scrollbar(parent_frame, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x', padx=10, pady=(0, 5))
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    all_users = []

    def _populate_tree(data_list):
        for i in tree.get_children(): tree.delete(i)
        # Ahora insertamos el ID
        for user in data_list:
            tree.insert("", "end", values=( user['nombre_completo'], user['usuario'], user['rol']))

    def _on_search_change(*args):
        search_term = search_var.get().lower()
        if not search_term: _populate_tree(all_users)
        else:
            filtered = [u for u in all_users if search_term in u['nombre_completo'].lower() or search_term in u['usuario'].lower()]
            _populate_tree(filtered)

    search_var.trace_add("write", _on_search_change)
    
    def _load_initial_data():
        nonlocal all_users
        all_users = user_controller.handle_get_all_users()
        _populate_tree(all_users)

    def on_add_record():
        show_register_user_form(parent_frame)

    def on_edit_record():
        selected_items = tree.selection()
        if not selected_items: messagebox.showwarning("Sin selección", "Por favor, seleccione un usuario para editar."); return
        selected_item = selected_items[0]
        # --- CORRECCIÓN DE ÍNDICE ---
        # El username está en la columna 2 (índice 1)
        username = tree.item(selected_item)['values'][1]
        show_edit_user_form(parent_frame, username)

    def on_delete_record():
        selected_items = tree.selection()
        if not selected_items: messagebox.showwarning("Sin selección", "Por favor, seleccione un usuario para eliminar."); return
        selected_item = selected_items[0]
        # --- CORRECCIÓN DE ÍNDICE ---
        username = tree.item(selected_item)['values'][1]
        if user_controller.handle_delete_user(username): _load_initial_data()

    ttk.Button(action_frame, text="Añadir Nuevo Usuario", command=on_add_record, style='Action.TButton').pack(side='left', padx=10)
    ttk.Button(action_frame, text="Eliminar Seleccionado", command=on_delete_record, style='Delete.TButton').pack(side='right', padx=10)
    ttk.Button(action_frame, text="Editar Seleccionado", command=on_edit_record, style='Action.TButton').pack(side='right')

    _load_initial_data()