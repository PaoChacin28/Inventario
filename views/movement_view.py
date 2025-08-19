

# views/movement_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import controllers.movement_controller as movement_controller

def clear_frame(frame):
    """Limpia todos los widgets de un frame."""
    for widget in frame.winfo_children(): widget.destroy()

def show_register_movement_form(parent_frame, user_id):
    """Dibuja el formulario dinámico para registrar cualquier tipo de movimiento."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Registrar Movimiento de Inventario", style='ContentTitle.TLabel').pack(pady=20)
    
    form_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    form_frame.pack(padx=20, pady=10, fill="x", anchor="n")
    form_frame.columnconfigure(0, weight=1)
    
    fields_container = ttk.Frame(form_frame, style='MainContent.TFrame')
    fields_container.grid(row=0, column=0, sticky="n", ipadx=150)
    
    ttk.Label(fields_container, text="Tipo de Movimiento*", style='ContentLabel.TLabel').pack(anchor="w")
    type_combo = ttk.Combobox(fields_container, values=["Entrada", "Salida", "Ajuste"], state="readonly")
    type_combo.pack(fill="x", pady=(2, 10))

    # --- FRAMES DINÁMICOS ---
    entry_frame = ttk.Frame(fields_container, style='MainContent.TFrame')
    exit_adjustment_frame = ttk.Frame(fields_container, style='MainContent.TFrame')
    
    # --- WIDGETS PARA 'ENTRADA' ---
    products_list = movement_controller.handle_get_products_for_selection() or []
    product_map = {f"{p['id_producto']} - {p['nombre']}": p['id_producto'] for p in products_list}
    ttk.Label(entry_frame, text="Producto a Ingresar*", style='ContentLabel.TLabel').pack(anchor="w")
    entry_product_combo = ttk.Combobox(entry_frame, values=list(product_map.keys()), state="readonly")
    entry_product_combo.pack(fill="x", pady=(2, 5))
    ttk.Label(entry_frame, text="Tag del Nuevo Lote*", style='ContentLabel.TLabel').pack(anchor="w")
    entry_tag_entry = ttk.Entry(entry_frame)
    entry_tag_entry.pack(fill="x", pady=(2, 5))
    ttk.Label(entry_frame, text="Cantidad Inicial*", style='ContentLabel.TLabel').pack(anchor="w")
    entry_qty_entry = ttk.Entry(entry_frame)
    entry_qty_entry.pack(fill="x", pady=(2, 5))
    ttk.Label(entry_frame, text="Unidad de Medida*", style='ContentLabel.TLabel').pack(anchor="w")
    entry_unit_combo = ttk.Combobox(entry_frame, values=["Unidades", "Kilos"], state="readonly")
    entry_unit_combo.set("Unidades")
    entry_unit_combo.pack(fill="x", pady=(2, 5))
    ttk.Label(entry_frame, text="Fecha de Vencimiento (Opcional)", style='ContentLabel.TLabel').pack(anchor="w")
    entry_date_entry = DateEntry(entry_frame, date_pattern='yyyy-mm-dd')
    entry_date_entry.pack(fill="x", pady=(2, 5))
    
    # --- WIDGETS PARA 'SALIDA' Y 'AJUSTE' ---
    lots_list = movement_controller.handle_get_active_lots_for_selection() or []
    lot_map = {f"{l['tag_lote']} ({l['nombre_producto']}) - Stock: {l['cantidad_actual']}": l['id_lote'] for l in lots_list}
    ttk.Label(exit_adjustment_frame, text="Seleccionar Lote Existente*", style='ContentLabel.TLabel').pack(anchor="w")
    exit_lot_combo = ttk.Combobox(exit_adjustment_frame, values=list(lot_map.keys()), state="readonly")
    exit_lot_combo.pack(fill="x", pady=(2, 5))
    ttk.Label(exit_adjustment_frame, text="Cantidad*", style='ContentLabel.TLabel').pack(anchor="w")
    exit_qty_entry = ttk.Entry(exit_adjustment_frame)
    exit_qty_entry.pack(fill="x", pady=(2, 5))
    desc_label = ttk.Label(exit_adjustment_frame, text="Descripción del Ajuste*", style='ContentLabel.TLabel')
    desc_entry = ttk.Entry(exit_adjustment_frame)

    # --- BOTONES DE ACCIÓN (que se mostrarán/ocultarán) ---
    button_frame = ttk.Frame(form_frame, style='MainContent.TFrame')
    button_frame.grid(row=1, column=0, pady=20)
    
    def guardar_entrada():
        product_id = product_map.get(entry_product_combo.get())
        data = {'product_id': product_id, 'tag_lote': entry_tag_entry.get().strip(),
                'cantidad': entry_qty_entry.get().strip(), 'unidad': entry_unit_combo.get(),
                'fecha_vencimiento': entry_date_entry.get_date(), 'user_id': user_id}
        if movement_controller.handle_register_entry(data):
            show_all_movements_list(parent_frame, user_id)

    def guardar_salida_o_ajuste(mov_type):
        selected_lot_display = exit_lot_combo.get()
        if not selected_lot_display:
            messagebox.showwarning("Selección Requerida", "Por favor, seleccione un lote de la lista.")
            return
        lote_id = lot_map.get(selected_lot_display)
        if movement_controller.handle_register_exit_or_adjustment(
            id_lote=lote_id, cantidad_str=exit_qty_entry.get().strip(), user_id=user_id,
            movement_type=mov_type, descripcion=desc_entry.get().strip()):
            show_all_movements_list(parent_frame, user_id)

    btn_entrada = ttk.Button(button_frame, text="Registrar Entrada", command=guardar_entrada, style='Action.TButton')
    btn_salida = ttk.Button(button_frame, text="Registrar Salida", command=lambda: guardar_salida_o_ajuste('Salida'), style='Action.TButton')
    btn_ajuste = ttk.Button(button_frame, text="Registrar Ajuste", command=lambda: guardar_salida_o_ajuste('Ajuste'), style='Action.TButton')
    btn_cancelar = ttk.Button(button_frame, text="Cancelar", command=lambda: show_all_movements_list(parent_frame, user_id), style='Delete.TButton')
    
    def on_type_change(event):
        # Ocultar todos los frames y botones de acción
        entry_frame.pack_forget()
        exit_adjustment_frame.pack_forget()
        desc_label.pack_forget(); desc_entry.pack_forget()
        btn_entrada.pack_forget(); btn_salida.pack_forget(); btn_ajuste.pack_forget()
        btn_cancelar.pack_forget() # Ocultar también el de cancelar para reordenarlo

        selected_type = type_combo.get()
        if selected_type == "Entrada":
            entry_frame.pack(fill="x", pady=5)
            btn_entrada.pack(side='left', padx=5)
        elif selected_type == "Salida":
            exit_adjustment_frame.pack(fill="x", pady=5)
            btn_salida.pack(side='left', padx=5)
        elif selected_type == "Ajuste":
            exit_adjustment_frame.pack(fill="x", pady=5)
            desc_label.pack(anchor="w"); desc_entry.pack(fill="x", pady=(2, 5))
            btn_ajuste.pack(side='left', padx=5)
        
        # El botón de cancelar siempre se muestra después del botón de acción
        btn_cancelar.pack(side='left', padx=5)

    type_combo.bind("<<ComboboxSelected>>", on_type_change)
    on_type_change(None) # Llamada inicial para configurar la vista

def show_all_movements_list(parent_frame, user_id):
    """
    Dibuja la vista principal de Movimientos: historial, filtro y botones de acción.
    """
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Historial de Movimientos", style='ContentTitle.TLabel').pack(pady=10)
    
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
    
    # --- Creación y Configuración de la Tabla y Scrollbars ---
    # 1. Crear widgets
    cols = ("Fecha", "Producto", "Tipo", "Tag / Lote", "Cantidad", "Descripción", "Usuario Responsable")
    tree = ttk.Treeview(container, columns=cols, show="headings", selectmode="browse")
    vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(parent_frame, orient="horizontal", command=tree.xview)
    action_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    
    # 2. Configurar widgets (columnas y vinculación de scroll)
    for col in cols: 
        tree.heading(col, text=col)
    tree.column("Fecha", width=160, stretch=tk.NO, anchor='center')
    tree.column("Producto", width=300) # Columna flexible
    tree.column("Tipo", width=80, stretch=tk.NO, anchor='center')
    tree.column("Tag / Lote", width=150, stretch=tk.NO, anchor='w')
    tree.column("Cantidad", width=80, stretch=tk.NO, anchor='center')
    tree.column("Descripción", width=250)
    tree.column("Usuario Responsable", width=200, stretch=tk.NO, anchor='w')
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # 3. Empaquetar en el orden visual correcto
    action_frame.pack(side='bottom', pady=(5,0), fill='x')
    hsb.pack(side='bottom', fill='x', padx=10, pady=(0, 5))
    vsb.pack(side='right', fill='y')
    tree.pack(side="left", fill="both", expand=True)
    
    # --- Lógica de Datos y Eventos ---
    all_movements = []

    def _populate_tree(data_list):
        for i in tree.get_children(): 
            tree.delete(i)
        for mov in data_list:
            # Formatear la fecha para que sea legible
            fecha = mov['fecha'].strftime('%Y-%m-%d %H:%M:%S')
            
            # Usar .get() para manejar de forma segura valores NULOS de la BD
            tree.insert("", "end", values=(
                fecha, 
                mov.get('producto_nombre') or 'N/A', 
                mov.get('tipo') or 'N/A', 
                mov.get('tag_lote') or 'N/A', 
                mov.get('cantidad') or 0, 
                mov.get('descripcion') or '', 
                mov.get('usuario_nombre') or 'N/A'
            ))

    def _on_search_change(*args):
        search_term = search_var.get().lower()
        if not search_term: 
            _populate_tree(all_movements)
        else:
            # Filtrar por nombre de producto o por tag/lote
            filtered = [
                m for m in all_movements 
                if search_term in (m.get('producto_nombre') or '').lower() or 
                   (m.get('tag_lote') and search_term in (m.get('tag_lote') or '').lower())
            ]
            _populate_tree(filtered)

    search_var.trace_add("write", _on_search_change)
    
    def _load_initial_data():
        nonlocal all_movements
        # --- CORRECCIÓN DE TIPEO ---
        all_movements = movement_controller.handle_get_all_movements() # Corregido
        _populate_tree(all_movements)
        
    # --- Botones de Acción ---
    def on_add_record():
        show_register_movement_form(parent_frame, user_id)

    ttk.Button(action_frame, text="Registrar Nuevo Movimiento", command=on_add_record, style='Action.TButton').pack(side='left', padx=10)
    

    _load_initial_data()