# views/product_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
import controllers.product_controller as product_controller
import controllers.provider_controller as provider_controller
import controllers.movement_controller as movement_controller

def clear_frame(frame):
    """Limpia todos los widgets de un frame."""
    for widget in frame.winfo_children(): widget.destroy()

def show_register_product_form(parent_frame):
    """Dibuja el formulario para definir un nuevo producto (sin stock)."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Definir Nuevo Producto", style='ContentTitle.TLabel').pack(pady=20)
    
    form_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    form_frame.pack(padx=20, pady=10, fill="x", anchor="n")
    form_frame.columnconfigure(0, weight=1)

    fields_container = ttk.Frame(form_frame, style='MainContent.TFrame')
    fields_container.grid(row=0, column=0, sticky="n", ipadx=150)

    entries = {}
    field_labels = {"codigo_producto": "Código Producto", "nombre": "Nombre", "tipo": "Tipo", "proveedor": "Proveedor"}

    providers_list = provider_controller.handle_get_providers_for_selection()
    provider_map = {p['nombre']: p['id_proveedor'] for p in providers_list}

    for key, label_text in field_labels.items():
        field_frame = ttk.Frame(fields_container, style='MainContent.TFrame')
        field_frame.pack(fill="x", pady=5)
        ttk.Label(field_frame, text=label_text, style='ContentLabel.TLabel').pack(anchor="w")
        
        widget = None
        if key == "tipo": widget = ttk.Combobox(field_frame, values=["Carnicos", "Viveres"], state="readonly"); widget.set("Carnicos")
        elif key == "proveedor": widget = ttk.Combobox(field_frame, values=list(provider_map.keys()), state="readonly", height=10)
        else: widget = ttk.Entry(field_frame)
        
        widget.pack(fill="x")
        entries[key] = widget
    
    def guardar_action():
        data = {key: widget.get().strip() for key, widget in entries.items()}
        data['id_proveedor'] = provider_map.get(data.pop('proveedor'))
        
        if product_controller.handle_add_product(data):
            show_all_products_list(parent_frame)

    button_frame = ttk.Frame(form_frame, style='MainContent.TFrame')
    button_frame.grid(row=1, column=0, pady=20)
    ttk.Button(button_frame, text="Guardar Producto", command=guardar_action, style='Action.TButton').pack(side='left', padx=5)
    ttk.Button(button_frame, text="Cancelar", command=lambda: show_all_products_list(parent_frame), style='Delete.TButton').pack(side='left', padx=5)

def show_edit_product_form(parent_frame, product_code):
    """Dibuja el formulario para editar la definición de un producto."""
    clear_frame(parent_frame)
    product_data = product_controller.handle_find_product(product_code)
    if not product_data:
        messagebox.showerror("Error", f"No se pudieron cargar los datos para el producto '{product_code}'.")
        show_all_products_list(parent_frame)
        return
    
    ttk.Label(parent_frame, text=f"Editando Producto: {product_data['nombre']}", style='ContentTitle.TLabel').pack(pady=20)
    
    form_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    form_frame.pack(padx=20, pady=10, fill="x", anchor="n")
    form_frame.columnconfigure(0, weight=1)

    fields_container = ttk.Frame(form_frame, style='MainContent.TFrame')
    fields_container.grid(row=0, column=0, sticky="n", ipadx=150)

    entries = {}
    field_labels = {"nombre": "Nombre", "tipo": "Tipo", "proveedor": "Proveedor"}
    
    providers_list = provider_controller.handle_get_providers_for_selection()
    id_to_name_map = {p['id_proveedor']: p['nombre'] for p in providers_list}
    name_to_id_map = {p['nombre']: p['id_proveedor'] for p in providers_list}
    current_provider_name = id_to_name_map.get(product_data.get('id_proveedor'))

    for key, label_text in field_labels.items():
        field_frame = ttk.Frame(fields_container, style='MainContent.TFrame')
        field_frame.pack(fill="x", pady=5)
        ttk.Label(field_frame, text=label_text, style='ContentLabel.TLabel').pack(anchor="w")
        
        widget = None
        if key == "tipo": widget = ttk.Combobox(field_frame, values=["Carnicos", "Viveres"], state="readonly")
        elif key == "proveedor": widget = ttk.Combobox(field_frame, values=list(name_to_id_map.keys()), state="readonly")
        else: widget = ttk.Entry(field_frame)
        
        if key == 'proveedor': widget.set(current_provider_name or "")
        else: widget.insert(0, product_data.get(key, ''))
        
        widget.pack(fill="x")
        entries[key] = widget

    def actualizar_action():
        data = {key: widget.get().strip() for key, widget in entries.items()}
        data['id_proveedor'] = name_to_id_map.get(data.pop('proveedor'))
        
        if product_controller.handle_update_product(product_data['id_producto'], data):
            show_all_products_list(parent_frame)

    button_frame = ttk.Frame(form_frame, style='MainContent.TFrame')
    button_frame.grid(row=1, column=0, pady=20)
    ttk.Button(button_frame, text="Actualizar Producto", command=actualizar_action, style='Action.TButton').pack(side='left', padx=5)
    ttk.Button(button_frame, text="Cancelar", command=lambda: show_all_products_list(parent_frame), style='Delete.TButton').pack(side='left', padx=5)
    
def show_product_lots_details(parent_frame, product_data):
    """Muestra una tabla con todos los lotes de un producto específico."""
    clear_frame(parent_frame)
    product_id = product_data['id_producto']
    product_name = product_data['nombre']

    ttk.Label(parent_frame, text=f"Lotes para: {product_name}", style='ContentTitle.TLabel').pack(pady=10)
    
    container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    container.pack(fill="both", expand=True, padx=10, pady=10)
    
    cols = ("Tag Lote", "Stock Inicial", "Stock Actual", "Unidad", "Fecha Ingreso", "Fecha Vencimiento")
    tree = ttk.Treeview(container, columns=cols, show="headings")
    for col in cols: tree.heading(col, text=col)

    tree.column("Tag Lote", width=200); tree.column("Stock Actual", anchor='center')
    
    vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(parent_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    action_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    action_frame.pack(side='bottom', pady=(5,0), fill='x')
    hsb.pack(side='bottom', fill='x', padx=10, pady=(0, 5))
    vsb.pack(side='right', fill='y')
    tree.pack(fill="both", expand=True)

    def _load_lots_data():
        lots = movement_controller.handle_get_lots_for_product(product_id)
        for i in tree.get_children(): tree.delete(i)
        for lote in lots:
            tree.insert("", "end", values=(
                lote['tag_lote'], f"{lote['cantidad_inicial']:.3f}", f"{lote['cantidad_actual']:.3f}",
                lote['unidad_medida'], lote['fecha_ingreso'], lote.get('fecha_vencimiento', 'N/A')
            ))

    ttk.Button(action_frame, text="< Volver a la Lista de Productos", 
               command=lambda: show_all_products_list(parent_frame), 
               style='Action.TButton').pack(side='left', padx=10)
    
    _load_lots_data()

def show_all_products_list(parent_frame):
    """
    Dibuja la vista principal de productos: lista, filtro y botones de acción separados.
    """
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Gestión de Productos", style='ContentTitle.TLabel').pack(pady=10)
    
    # --- Barra de búsqueda / filtro ---
    search_bar_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    search_bar_frame.pack(fill='x', padx=10, pady=5)
    ttk.Label(search_bar_frame, text="Filtrar:", style='ContentLabel.TLabel').pack(side='left', padx=(0, 5))
    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_bar_frame, textvariable=search_var)
    search_entry.pack(side='left', fill='x', expand=True)

    # --- Contenedor de la tabla ---
    container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    container.pack(fill="both", expand=True, padx=10, pady=10)
    
    # --- Creación de Widgets de la Tabla ---
    cols = ("Código", "Nombre", "Tipo", "Stock Total", "Proveedor")
    tree = ttk.Treeview(container, columns=cols, show="headings", selectmode="browse")
    vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(parent_frame, orient="horizontal", command=tree.xview)
    
    # --- Configuración de Encabezados y Columnas ---
    for col in cols: 
        tree.heading(col, text=col)
    tree.column("Código", width=120, stretch=tk.NO, anchor='w')
    tree.column("Nombre", width=250) # Columna flexible
    tree.column("Tipo", width=100, stretch=tk.NO, anchor='center')
    tree.column("Stock Total", width=100, stretch=tk.NO, anchor='center')
    tree.column("Proveedor", width=200)
    
    # Vinculamos las scrollbars
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    # --- Empaquetado de Widgets (en el orden visual correcto) ---
    action_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    action_frame.pack(side='bottom', pady=(5,0), fill='x')
    hsb.pack(side='bottom', fill='x', padx=10, pady=(0, 5))
    vsb.pack(side='right', fill='y')
    tree.pack(fill="both", expand=True)
    
    # --- Lógica de Datos y Eventos ---
    all_products = []

    def _populate_tree(data_list):
        for i in tree.get_children(): tree.delete(i)
        for prod in data_list:
            stock = prod.get('stock_total') or 0.0
            tree.insert("", "end", values=(
                prod['codigo_producto'], prod['nombre'], prod['tipo'],
                f"{stock:.3f}", prod.get('nombre_proveedor', 'N/A')
            ), iid=prod['id_producto']) # Usamos el ID del producto como ID de la fila

    def _on_search_change(*args):
        search_term = search_var.get().lower()
        if not search_term: 
            _populate_tree(all_products)
        else:
            filtered_products = []
            for prod in all_products:
                proveedor_nombre = prod.get('nombre_proveedor') or ""
                if (search_term in prod['nombre'].lower() or 
                    search_term in prod['codigo_producto'].lower() or 
                    search_term in proveedor_nombre.lower()):
                    filtered_products.append(prod)
            _populate_tree(filtered_products)

    search_var.trace_add("write", _on_search_change)
    
    def _load_initial_data():
        nonlocal all_products
        all_products = product_controller.handle_get_all_products_with_stock()
        _populate_tree(all_products)
        
    # --- Funciones de los Botones de Acción ---
    def on_add_record():
        show_register_product_form(parent_frame)

    def on_edit_record():
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Sin selección", "Por favor, seleccione un producto para editar.")
            return
        product_code = tree.item(selected_items[0])['values'][0]
        show_edit_product_form(parent_frame, product_code)

    def on_delete_record():
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Sin selección", "Por favor, seleccione un producto para eliminar.")
            return
        product_code = tree.item(selected_items[0])['values'][0]
        if product_controller.handle_delete_product(product_code):
            _load_initial_data()
    
    def on_view_lots():
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Sin selección", "Por favor, seleccione un producto para ver sus lotes.")
            return
        
        product_id = int(selected_items[0])
        product_data = next((p for p in all_products if p['id_producto'] == product_id), None)
        
        if product_data:
            show_product_lots_details(parent_frame, product_data)

    # --- Creación de los Botones de Acción ---
    ttk.Button(action_frame, text="Añadir Nuevo Producto", command=on_add_record, style='Action.TButton').pack(side='left', padx=10)
    ttk.Button(action_frame, text="Eliminar Seleccionado", command=on_delete_record, style='Delete.TButton').pack(side='right', padx=10)
    ttk.Button(action_frame, text="Editar Seleccionado", command=on_edit_record, style='Action.TButton').pack(side='right', padx=10)
    ttk.Button(action_frame, text="Ver Lotes / Detalles", command=on_view_lots, style='Search.TButton').pack(side='right', padx=10)

    _load_initial_data()