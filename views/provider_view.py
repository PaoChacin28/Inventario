# views/provider_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import controllers.provider_controller as provider_controller

def clear_frame(frame):
    """Limpia todos los widgets de un frame."""
    for widget in frame.winfo_children(): widget.destroy()

def show_register_provider_form(parent_frame):
    """Dibuja el formulario para registrar un nuevo proveedor."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Registrar Nuevo Proveedor", style='ContentTitle.TLabel').pack(pady=20)
    
    form_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    form_frame.pack(padx=20, pady=10, fill="x", anchor="n")
    form_frame.columnconfigure(0, weight=1)
    
    fields_container = ttk.Frame(form_frame, style='MainContent.TFrame')
    fields_container.grid(row=0, column=0, sticky="n", ipadx=150)

    entries = {}
    field_labels = {"nombre": "Nombre", "rif": "RIF", "telefono": "Teléfono (Opcional)", "direccion": "Dirección (Opcional)"}

    for key, label_text in field_labels.items():
        field_frame = ttk.Frame(fields_container, style='MainContent.TFrame')
        field_frame.pack(fill="x", pady=5)
        ttk.Label(field_frame, text=label_text, style='ContentLabel.TLabel').pack(anchor="w")
        widget = ttk.Entry(field_frame)
        widget.pack(fill="x")
        entries[key] = widget
        
    def guardar_action():
        data = {key: widget.get().strip() for key, widget in entries.items()}
        if provider_controller.handle_add_provider(**data):
            show_all_providers_list(parent_frame)

    button_frame = ttk.Frame(form_frame, style='MainContent.TFrame')
    button_frame.grid(row=1, column=0, pady=20)
    ttk.Button(button_frame, text="Guardar Proveedor", command=guardar_action, style='Action.TButton').pack(side='left', padx=5)
    ttk.Button(button_frame, text="Cancelar", command=lambda: show_all_providers_list(parent_frame), style='Delete.TButton').pack(side='left', padx=5)
    
def show_edit_provider_form(parent_frame, provider_rif_to_edit):
    """Dibuja el formulario para editar un proveedor específico."""
    clear_frame(parent_frame)
    provider_data = provider_controller.handle_find_provider(provider_rif_to_edit)
    if not provider_data:
        messagebox.showerror("Error", f"No se encontraron datos para el proveedor con RIF '{provider_rif_to_edit}'.")
        show_all_providers_list(parent_frame)
        return
        
    ttk.Label(parent_frame, text=f"Editando Proveedor: {provider_data['nombre']}", style='ContentTitle.TLabel').pack(pady=20)
    
    form_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    form_frame.pack(padx=20, pady=10, fill="x", anchor="n")
    form_frame.columnconfigure(0, weight=1)
    
    fields_container = ttk.Frame(form_frame, style='MainContent.TFrame')
    fields_container.grid(row=0, column=0, sticky="n", ipadx=150)

    entries = {}
    field_labels = {"nombre": "Nombre", "rif": "RIF", "telefono": "Teléfono", "direccion": "Dirección"}

    for key, label_text in field_labels.items():
        field_frame = ttk.Frame(fields_container, style='MainContent.TFrame')
        field_frame.pack(fill="x", pady=5)
        ttk.Label(field_frame, text=label_text, style='ContentLabel.TLabel').pack(anchor="w")
        widget = ttk.Entry(field_frame)
        widget.insert(0, provider_data.get(key) or "")
        widget.pack(fill="x")
        entries[key] = widget
            
    def actualizar_action():
        data = {key: widget.get().strip() for key, widget in entries.items()}
        if provider_controller.handle_update_provider(provider_data['id_proveedor'], **data):
            show_all_providers_list(parent_frame)

    button_frame = ttk.Frame(form_frame, style='MainContent.TFrame')
    button_frame.grid(row=1, column=0, pady=20)
    ttk.Button(button_frame, text="Actualizar Proveedor", command=actualizar_action, style='Action.TButton').pack(side='left', padx=5)
    ttk.Button(button_frame, text="Cancelar", command=lambda: show_all_providers_list(parent_frame), style='Delete.TButton').pack(side='left', padx=5)

def show_delete_provider_form(parent_frame):
    """Dibuja la interfaz para buscar y confirmar la eliminación de un proveedor."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Eliminar Proveedor", style='ContentTitle.TLabel').pack(pady=20)

    search_frame_container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    search_frame_container.pack(padx=20, pady=10, fill="x", anchor="n")
    search_frame_container.columnconfigure(0, weight=1)
    
    search_field_frame = ttk.Frame(search_frame_container, style='MainContent.TFrame')
    search_field_frame.grid(row=0, column=0, sticky="n", ipadx=100)
    
    ttk.Label(search_field_frame, text="RIF del Proveedor a Eliminar", style='ContentLabel.TLabel').pack(anchor="w")
    search_entry = ttk.Entry(search_field_frame)
    search_entry.pack(fill="x", side="left", expand=True)

    details_container_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    current_provider_rif = None

    def buscar_y_cargar_action():
        nonlocal current_provider_rif
        for widget in details_container_frame.winfo_children(): widget.destroy()
        
        provider_data = provider_controller.handle_find_provider(search_entry.get().strip())
        
        if provider_data:
            current_provider_rif = provider_data['rif']
            details_container_frame.pack(padx=20, pady=10, fill="x", anchor="n")
            details_box = ttk.LabelFrame(details_container_frame, text="Verifique los datos del proveedor", style='TLabelFrame')
            details_box.pack(pady=10, ipadx=20, ipady=10)
            ttk.Label(details_box, text=f"Nombre: {provider_data['nombre']}", style='ContentLabel.TLabel').pack(anchor="w", padx=10, pady=2)
            ttk.Label(details_box, text=f"Teléfono: {provider_data.get('telefono') or 'N/A'}", style='ContentLabel.TLabel').pack(anchor="w", padx=10, pady=2)
            
            def eliminar_action():
                if provider_controller.handle_delete_provider(current_provider_rif):
                    search_entry.delete(0, tk.END)
                    for widget in details_container_frame.winfo_children(): widget.destroy()

            ttk.Button(details_box, text=f"Confirmar Eliminación", command=eliminar_action, style='Delete.TButton').pack(pady=20)

    ttk.Button(search_field_frame, text="Buscar", command=buscar_y_cargar_action, style='Search.TButton').pack(side="left", padx=(5,0))

def show_all_providers_list(parent_frame):
    """Dibuja la vista principal de proveedores: lista, filtro y botones de acción."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Gestión de Proveedores", style='ContentTitle.TLabel').pack(pady=10)
    
    search_bar_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    search_bar_frame.pack(fill='x', padx=10, pady=5)
    ttk.Label(search_bar_frame, text="Filtrar:", style='ContentLabel.TLabel').pack(side='left', padx=(0, 5))
    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_bar_frame, textvariable=search_var)
    search_entry.pack(side='left', fill='x', expand=True)

    container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    container.pack(fill="both", expand=True, padx=10, pady=10)
    
    cols = ( "Nombre", "RIF", "Teléfono", "Dirección")
    tree = ttk.Treeview(container, columns=cols, show="headings", selectmode="browse")
    for col in cols: tree.heading(col, text=col)
    tree.column("Nombre", width=250); tree.column("Dirección", width=350)
    vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.pack(side="left", fill="both", expand=True)

    action_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    action_frame.pack(side='bottom', pady=(5,0), fill='x')
    hsb = ttk.Scrollbar(parent_frame, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x', padx=10, pady=(0, 5))
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    all_providers = []

    def _populate_tree(data_list):
        for i in tree.get_children(): tree.delete(i)
        for p in data_list:
            tree.insert("", "end", values=( p['nombre'], p['rif'], p['telefono'] or "N/A", p['direccion'] or "N/A"))

    def _on_search_change(*args):
        search_term = search_var.get().lower()
        if not search_term: _populate_tree(all_providers)
        else:
            filtered = [p for p in all_providers if search_term in p['nombre'].lower() or search_term in p['rif'].lower()]
            _populate_tree(filtered)

    search_var.trace_add("write", _on_search_change)
    
    def _load_initial_data():
        nonlocal all_providers
        all_providers = provider_controller.handle_get_all_providers()
        _populate_tree(all_providers)
        
    def on_add_record():
        show_register_provider_form(parent_frame)

    def on_edit_record():
        selected_items = tree.selection()
        if not selected_items: messagebox.showwarning("Sin selección", "Por favor, seleccione un proveedor para editar."); return
        selected_item = selected_items[0]
        provider_rif = tree.item(selected_item)['values'][1] # RIF es la 3ra columna (índice 2)
        show_edit_provider_form(parent_frame, provider_rif)

    def on_delete_record():
        selected_items = tree.selection()
        if not selected_items: messagebox.showwarning("Sin selección", "Por favor, seleccione un proveedor para eliminar."); return
        selected_item = selected_items[0]
        provider_rif = tree.item(selected_item)['values'][1] # RIF es la 3ra columna (índice 2)
        if provider_controller.handle_delete_provider(provider_rif): _load_initial_data()

    ttk.Button(action_frame, text="Añadir Nuevo Proveedor", command=on_add_record, style='Action.TButton').pack(side='left', padx=10)
    ttk.Button(action_frame, text="Eliminar Seleccionado", command=on_delete_record, style='Delete.TButton').pack(side='right', padx=10)
    ttk.Button(action_frame, text="Editar Seleccionado", command=on_edit_record, style='Action.TButton').pack(side='right')

    _load_initial_data()