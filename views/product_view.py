# views/product_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from utils.scrollable_frame import ScrollableFrame
import controllers.product_controller as product_controller
import controllers.provider_controller as provider_controller
import controllers.movement_controller as movement_controller
from utils import validation # Importamos para la validación del código

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def show_register_product_form(parent_frame):
    """Dibuja el formulario para registrar un producto, centrado como los demás."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Registrar Nuevo Producto", style='ContentTitle.TLabel').pack(pady=20)
    
    # --- PATRÓN DE CENTRADO EXACTO DE TUS OTROS FORMULARIOS ---
    
    # 1. El 'form_frame' principal que usará grid.
    form_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    form_frame.pack(padx=20, pady=10, fill="x", anchor="n")
    form_frame.columnconfigure(0, weight=1) # Columna central expansiva

    # 2. El 'fields_container' con ancho fijo que se centrará en la grilla.
    fields_container = ttk.Frame(form_frame, style='MainContent.TFrame')
    fields_container.grid(row=0, column=0, sticky="n", ipadx=150)

    # 3. El 'button_frame' que también se centrará en la grilla.
    button_frame = ttk.Frame(form_frame, style='MainContent.TFrame')
    button_frame.grid(row=1, column=0, pady=20)

    # De aquí en adelante, todo el contenido se coloca en los contenedores correspondientes.

    # --- Sección de Datos del Producto ---
    ttk.Label(fields_container, text="Datos del Producto", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10,0))
    ttk.Separator(fields_container, orient='horizontal').pack(fill='x', pady=(2, 10))

    entries = {}
    field_labels = {"codigo_producto": "Código Producto:* (ej. CAR-001)", "nombre": "Nombre:*", "tipo": "Tipo:*"}
    for key, label_text in field_labels.items():
        field_frame = ttk.Frame(fields_container, style='MainContent.TFrame')
        field_frame.pack(fill="x", pady=5, padx=10)
        ttk.Label(field_frame, text=label_text, style='ContentLabel.TLabel').pack(anchor="w")
        widget = None
        if key == "tipo": widget = ttk.Combobox(field_frame, values=["Carnicos", "Viveres"], state="readonly"); widget.set("Carnicos")
        else: widget = ttk.Entry(field_frame)
        widget.pack(fill="x")
        entries[key] = widget

    # --- Sección de Asociación de Proveedores ---
    ttk.Label(fields_container, text="Asociar Proveedores (Opcional)", font=("Arial", 11, "bold")).pack(anchor="w", pady=(20,0))
    ttk.Separator(fields_container, orient='horizontal').pack(fill='x', pady=(2, 10))
    
    provider_widgets_container = ttk.Frame(fields_container)
    provider_widgets_container.pack(fill="x", expand=True, padx=10)

    provider_combobox_list = []
    all_providers_list = provider_controller.handle_get_providers_for_selection()
    provider_map = {p['nombre']: p['id_proveedor'] for p in all_providers_list}
    all_provider_names = sorted(list(provider_map.keys()))

    def _update_provider_options(*args):
        selected_providers = {combo.get() for combo in provider_combobox_list if combo.get()}
        for combo in provider_combobox_list:
            current_selection = combo.get()
            available_options = [name for name in all_provider_names if name not in selected_providers]
            if current_selection:
                available_options.append(current_selection)
                available_options.sort()
            combo['values'] = available_options

    def add_provider_combobox():
        combo_frame = ttk.Frame(provider_widgets_container)
        combo_frame.pack(fill="x", pady=2)
        new_combo = ttk.Combobox(combo_frame, state="readonly")
        new_combo.pack(side="left", fill="x", expand=True)
        provider_combobox_list.append(new_combo)
        new_combo.bind("<<ComboboxSelected>>", _update_provider_options)
        def remove_this_combobox():
            provider_combobox_list.remove(new_combo)
            combo_frame.destroy()
            _update_provider_options()
        remove_btn = ttk.Button(combo_frame, text="X", command=remove_this_combobox, width=2, style='Small.Delete.TButton')
        remove_btn.pack(side="left", padx=(5,0))
        _update_provider_options()

    add_controls_frame = ttk.Frame(fields_container)
    add_controls_frame.pack(fill="x", pady=(10, 5), padx=10)
    ttk.Button(add_controls_frame, text="Añadir Campo de Proveedor", command=add_provider_combobox, style='Small.Action.TButton').pack()
    add_provider_combobox() # Añadimos el primer campo por defecto

    def guardar_todo_action():
        product_data = {key: widget.get().strip() for key, widget in entries.items()}
        if not validation.is_valid_product_code(product_data['codigo_producto']):
            messagebox.showerror("Formato Inválido", "El formato del Código de Producto es inválido.\nDebe ser algo como 'CAR-001'.")
            return
        success, new_product_id = product_controller.handle_add_product(product_data)
        if success:
            selected_provider_ids = {provider_map.get(combo.get()) for combo in provider_combobox_list if combo.get()}
            associations_count = sum(1 for prov_id in selected_provider_ids if product_controller.handle_associate_provider(new_product_id, prov_id))
            messagebox.showinfo("Éxito", f"Producto '{product_data['nombre']}' guardado.\n{associations_count} proveedores asociados.")
            show_all_products_list(parent_frame)

    # Los botones se empaquetan en su propio frame centrado
    ttk.Button(button_frame, text="Guardar Producto y Asociaciones", command=guardar_todo_action, style='Action.TButton').pack(side='left', padx=5)
    ttk.Button(button_frame, text="Cancelar", command=lambda: show_all_products_list(parent_frame), style='Delete.TButton').pack(side='left', padx=5)

def show_edit_product_form(parent_frame, product_code):
    """Dibuja el formulario de gestión completa para editar un producto, centrado y sin scroll."""
    clear_frame(parent_frame)
    
    # --- 1. CARGA DE DATOS INICIAL (sin cambios) ---
    product_data = product_controller.handle_find_product(product_code)
    if not product_data:
        messagebox.showerror("Error", f"No se pudieron cargar los datos para el producto '{product_code}'.")
        show_all_products_list(parent_frame)
        return

    initial_associated_providers = product_controller.handle_get_providers_for_product(product_data['id_producto'])
    all_providers_list = provider_controller.handle_get_providers_for_selection()
    provider_map = {p['nombre']: p['id_proveedor'] for p in all_providers_list}
    all_provider_names = sorted(list(provider_map.keys()))

    # --- 2. LAYOUT CENTRADO ESTÁNDAR (SIN SCROLL) ---
    ttk.Label(parent_frame, text=f"Editando Producto: {product_data['nombre']}", style='ContentTitle.TLabel').pack(pady=20)
    
    # El 'form_frame' principal que usará grid para centrar su contenido.
    form_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    form_frame.pack(padx=20, pady=10, fill="x", anchor="n")
    form_frame.columnconfigure(0, weight=1) # Columna central expansiva

    # El 'fields_container' con ancho fijo que se centrará.
    fields_container = ttk.Frame(form_frame, style='MainContent.TFrame')
    fields_container.grid(row=0, column=0, sticky="n", ipadx=150)

    # El 'button_frame' que también se centrará.
    button_frame = ttk.Frame(form_frame, style='MainContent.TFrame')
    button_frame.grid(row=1, column=0, pady=20)

    # --- 3. SECCIÓN DE DATOS DEL PRODUCTO (Precargada) ---
    ttk.Label(fields_container, text="Datos del Producto", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10,0))
    ttk.Separator(fields_container, orient='horizontal').pack(fill='x', pady=(2, 10))

    entries = {}
    field_labels = {"codigo_producto": "Código Producto (No editable)", "nombre": "Nombre", "tipo": "Tipo"}
    for key, label_text in field_labels.items():
        field_frame = ttk.Frame(fields_container, style='MainContent.TFrame')
        field_frame.pack(fill="x", pady=5, padx=10)
        ttk.Label(field_frame, text=label_text, style='ContentLabel.TLabel').pack(anchor="w")
        widget = None
        if key == "tipo": widget = ttk.Combobox(field_frame, values=["Carnicos", "Viveres"], state="readonly")
        else: widget = ttk.Entry(field_frame)
        
        widget.insert(0, product_data.get(key, ''))
        if key == "tipo": widget.set(product_data.get(key, ''))
        if key == "codigo_producto": widget.config(state='readonly')
        
        widget.pack(fill="x")
        entries[key] = widget

    # --- 4. SECCIÓN DE GESTIÓN DE PROVEEDORES (Precargada) ---
    ttk.Label(fields_container, text="Gestionar Proveedores Asociados", font=("Arial", 11, "bold")).pack(anchor="w", pady=(20,0))
    ttk.Separator(fields_container, orient='horizontal').pack(fill='x', pady=(2, 10))
    
    provider_widgets_container = ttk.Frame(fields_container)
    provider_widgets_container.pack(fill="x", expand=True, padx=10)

    provider_combobox_list = []

    def _update_provider_options(*args):
        selected_providers = {combo.get() for combo in provider_combobox_list if combo.get()}
        for combo in provider_combobox_list:
            current_selection = combo.get()
            available_options = [name for name in all_provider_names if name not in selected_providers]
            if current_selection:
                available_options.append(current_selection)
                available_options.sort()
            combo['values'] = available_options

    def add_provider_combobox(provider_to_set=None):
        combo_frame = ttk.Frame(provider_widgets_container)
        combo_frame.pack(fill="x", pady=2)
        new_combo = ttk.Combobox(combo_frame, state="readonly")
        new_combo.pack(side="left", fill="x", expand=True)
        provider_combobox_list.append(new_combo)
        new_combo.bind("<<ComboboxSelected>>", _update_provider_options)
        
        if provider_to_set: new_combo.set(provider_to_set)

        def remove_this_combobox():
            provider_combobox_list.remove(new_combo)
            combo_frame.destroy()
            _update_provider_options()
        remove_btn = ttk.Button(combo_frame, text="X", command=remove_this_combobox, width=2, style='Small.Delete.TButton')
        remove_btn.pack(side="left", padx=(5,0))
        _update_provider_options()

    # Precargamos los proveedores existentes
    for provider in initial_associated_providers:
        add_provider_combobox(provider['nombre'])

    # Si no hay proveedores asociados, añadimos un campo vacío
    if not initial_associated_providers:
        add_provider_combobox()

    add_controls_frame = ttk.Frame(fields_container)
    add_controls_frame.pack(fill="x", pady=(10, 5), padx=10)
    ttk.Button(add_controls_frame, text="Añadir Campo de Proveedor", command=lambda: add_provider_combobox(), style='Small.Action.TButton').pack()

    def actualizar_todo_action():
        updated_product_data = {'nombre': entries['nombre'].get().strip(), 'tipo': entries['tipo'].get()}
        final_provider_ids = {provider_map.get(combo.get()) for combo in provider_combobox_list if combo.get()}
        
        if product_controller.handle_update_product_and_associations(
            product_id=product_data['id_producto'],
            product_data=updated_product_data,
            final_provider_ids=final_provider_ids
        ):
            show_all_products_list(parent_frame)

    # --- 5. BOTONES DE ACCIÓN (en su frame centrado) ---
    ttk.Button(button_frame, text="Actualizar Producto", command=actualizar_todo_action, style='Action.TButton').pack(side='left', padx=5)
    ttk.Button(button_frame, text="Cancelar", command=lambda: show_all_products_list(parent_frame), style='Delete.TButton').pack(side='left', padx=5)
    
    
    
def show_product_lots_details(parent_frame, product_data):
    """Muestra una tabla con todos los lotes de un producto específico."""
    clear_frame(parent_frame)
    product_id = product_data['id_producto']
    product_name = product_data['nombre']

    ttk.Label(parent_frame, text=f"Lotes para: {product_name}", style='ContentTitle.TLabel').pack(pady=10)
    
    # Se usa el layout de 3 partes para asegurar que la tabla sea ajustable
    bottom_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    bottom_frame.pack(side='bottom', fill='x', padx=10, pady=10)
    
    container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    container.pack(fill="both", expand=True, padx=10, pady=10)
    
    cols = ("Tag Lote", "Stock Inicial", "Stock Actual", "Unidad", "Fecha Ingreso", "Fecha Vencimiento")
    tree = ttk.Treeview(container, columns=cols, show="headings")
    vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    for col in cols: tree.heading(col, text=col)
    tree.column("Tag Lote", width=200); tree.column("Stock Actual", anchor='center')
    
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

    ttk.Button(bottom_frame, text="< Volver a la Lista de Productos", 
               command=lambda: show_all_products_list(parent_frame), 
               style='Action.TButton').pack(side='left')
    
    _load_lots_data()

def show_product_providers_details(parent_frame, product_data):
    """Muestra una tabla de solo lectura con los proveedores asociados a un producto."""
    clear_frame(parent_frame)
    product_id = product_data['id_producto']
    product_name = product_data['nombre']

    ttk.Label(parent_frame, text=f"Proveedores para: {product_name}", style='ContentTitle.TLabel').pack(pady=10)
    
    bottom_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    bottom_frame.pack(side='bottom', fill='x', padx=10, pady=10)
    
    container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    container.pack(fill="both", expand=True, padx=10, pady=10)
    
    cols = ("Nombre", "RIF", "Teléfono", "Dirección")
    tree = ttk.Treeview(container, columns=cols, show="headings")
    vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    
    for col in cols: tree.heading(col, text=col)
    tree.column("Nombre", width=250)
    tree.column("RIF", width=120, anchor='center')
    tree.column("Teléfono", width=120, anchor='center')
    tree.column("Dirección", width=350)
    
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side='right', fill='y')
    tree.pack(fill="both", expand=True)

    def _load_associated_providers():
        for i in tree.get_children(): tree.delete(i)
        associated_list = product_controller.handle_get_providers_for_product(product_id)
        for p in associated_list:
            tree.insert("", "end", values=(p['nombre'], p['rif'], p.get('telefono') or 'N/A', p.get('direccion') or 'N/A'))

    ttk.Button(bottom_frame, text="< Volver a la Lista de Productos", 
               command=lambda: show_all_products_list(parent_frame), 
               style='Action.TButton').pack(side='left')
    
    _load_associated_providers()
    
def show_all_products_list(parent_frame):
    """Dibuja la vista principal de productos con layout ajustable."""
    clear_frame(parent_frame)
    
    # Layout de 3 partes
    top_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    top_frame.pack(side='top', fill='x', padx=10, pady=10)

    bottom_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    bottom_frame.pack(side='bottom', fill='x', padx=10, pady=10)
    
    container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    container.pack(fill="both", expand=True, padx=10)

    # Contenido de la parte superior
    ttk.Label(top_frame, text="Gestión de Productos", style='ContentTitle.TLabel').pack(pady=10)
    search_bar_frame = ttk.Frame(top_frame, style='MainContent.TFrame')
    search_bar_frame.pack(fill='x', pady=5)
    ttk.Label(search_bar_frame, text="Filtrar:", style='ContentLabel.TLabel').pack(side='left', padx=(0, 5))
    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_bar_frame, textvariable=search_var)
    search_entry.pack(side='left', fill='x', expand=True)

    # Contenido de la parte central (tabla)
    cols = ("Código", "Nombre", "Tipo", "Stock Total")
    tree = ttk.Treeview(container, columns=cols, show="headings", selectmode="browse")
    vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    for col in cols: tree.heading(col, text=col)
    tree.column("Código", width=120, stretch=tk.NO)
    tree.column("Nombre", width=300) # Columna flexible
    tree.column("Tipo", width=150, stretch=tk.NO)
    tree.column("Stock Total", width=120, stretch=tk.NO, anchor='center')
    
    vsb.pack(side='right', fill='y')
    tree.pack(fill="both", expand=True)
    
    all_products = []

    def _populate_tree(data_list):
        for i in tree.get_children(): tree.delete(i)
        for prod in data_list:
            stock = prod.get('stock_total', 0.0)
            tree.insert("", "end", values=(
                prod['codigo_producto'], prod['nombre'], prod['tipo'], f"{stock:.3f}"
            ), iid=prod['id_producto'])

    def _on_search_change(*args):
        search_term = search_var.get().lower()
        if not search_term: _populate_tree(all_products)
        else:
            filtered = [p for p in all_products if search_term in p['nombre'].lower() or search_term in p['codigo_producto'].lower()]
            _populate_tree(filtered)

    search_var.trace_add("write", _on_search_change)
    
    def _load_initial_data():
        nonlocal all_products
        all_products = product_controller.handle_get_all_products_with_stock()
        _populate_tree(all_products)
        
    def on_add_record():
        show_register_product_form(parent_frame)

    def on_edit_record():
        selected_items = tree.selection()
        if not selected_items: messagebox.showwarning("Sin selección", "Por favor, seleccione un producto para editar."); return
        product_code = tree.item(selected_items[0])['values'][0]
        show_edit_product_form(parent_frame, product_code)

    def on_deactivate_record():
        selected_items = tree.selection()
        if not selected_items: messagebox.showwarning("Sin selección", "Por favor, seleccione un producto para desactivar."); return
        product_code = tree.item(selected_items[0])['values'][0]
        if product_controller.handle_deactivate_product(product_code): _load_initial_data()
    
    def on_view_lots():
        selected_items = tree.selection()
        if not selected_items: messagebox.showwarning("Sin selección", "Por favor, seleccione un producto para ver sus lotes."); return
        product_id = int(selected_items[0])
        product_data = next((p for p in all_products if p['id_producto'] == product_id), None)
        if product_data: show_product_lots_details(parent_frame, product_data)
        
    def on_view_providers():
        selected_items = tree.selection()
        if not selected_items: messagebox.showwarning("Sin selección", "Por favor, seleccione un producto para ver sus proveedores."); return
        product_id = int(selected_items[0])
        product_data = next((p for p in all_products if p['id_producto'] == product_id), None)
        if product_data: show_product_providers_details(parent_frame, product_data)

    # Contenido de la parte inferior (botones)
    ttk.Button(bottom_frame, text="Añadir Producto", command=on_add_record, style='Action.TButton').pack(side='left', padx=(0, 5))
    ttk.Button(bottom_frame, text="Ver Lotes", command=on_view_lots, style='Search.TButton').pack(side='left', padx=5)
    ttk.Button(bottom_frame, text="Ver Proveedores", command=on_view_providers, style='Search.TButton').pack(side='left', padx=5)
    ttk.Button(bottom_frame, text="Desactivar Seleccionado", command=on_deactivate_record, style='Delete.TButton').pack(side='right')
    ttk.Button(bottom_frame, text="Editar Seleccionado", command=on_edit_record, style='Action.TButton').pack(side='right', padx=5)
    
    _load_initial_data()