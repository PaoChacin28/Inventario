# views/movement_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import controllers.movement_controller as movement_controller

def clear_frame(frame):
    for widget in frame.winfo_children(): widget.destroy()

def show_register_movement_form(parent_frame, user_id):
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Registrar Movimiento de Inventario", style='ContentTitle.TLabel').pack(pady=20)
    
    form_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    form_frame.pack(padx=20, pady=10, fill="x", anchor="n")
    form_frame.columnconfigure(0, weight=1)
    
    fields_container = ttk.Frame(form_frame, style='MainContent.TFrame')
    fields_container.grid(row=0, column=0, sticky="n", ipadx=150)
    
    ttk.Label(fields_container, text="Tipo de Movimiento", style='ContentLabel.TLabel').pack(anchor="w")
    type_combo = ttk.Combobox(fields_container, values=["Entrada", "Salida", "Ajuste"], state="readonly")
    type_combo.pack(fill="x", pady=(2, 10))

    entry_frame = ttk.Frame(fields_container, style='MainContent.TFrame')
    exit_adjustment_frame = ttk.Frame(fields_container, style='MainContent.TFrame')
    
    # --- WIDGETS PARA 'ENTRADA' ---
    products_list = movement_controller.handle_get_products_for_selection()
    product_map = {f"{p['id_producto']} - {p['nombre']}": p['id_producto'] for p in products_list}
    ttk.Label(entry_frame, text="Producto a Ingresar", style='ContentLabel.TLabel').pack(anchor="w")
    entry_product_combo = ttk.Combobox(entry_frame, values=list(product_map.keys()), state="readonly")
    entry_product_combo.pack(fill="x", pady=(2, 5))
    ttk.Label(entry_frame, text="Tag del Nuevo Lote (Único)", style='ContentLabel.TLabel').pack(anchor="w")
    entry_tag_entry = ttk.Entry(entry_frame)
    entry_tag_entry.pack(fill="x", pady=(2, 5))
    ttk.Label(entry_frame, text="Cantidad Inicial", style='ContentLabel.TLabel').pack(anchor="w")
    entry_qty_entry = ttk.Entry(entry_frame)
    entry_qty_entry.pack(fill="x", pady=(2, 5))
    ttk.Label(entry_frame, text="Unidad de Medida", style='ContentLabel.TLabel').pack(anchor="w")
    entry_unit_combo = ttk.Combobox(entry_frame, values=["Unidades", "Kilos"], state="readonly")
    entry_unit_combo.set("Unidades")
    entry_unit_combo.pack(fill="x", pady=(2, 5))
    ttk.Label(entry_frame, text="Fecha de Vencimiento (Opcional)", style='ContentLabel.TLabel').pack(anchor="w")
    entry_date_entry = DateEntry(entry_frame, date_pattern='yyyy-mm-dd', firstweekday='sunday', showweeknumbers=False)
    entry_date_entry.pack(fill="x", pady=(2, 5))
    
    # --- WIDGETS PARA 'SALIDA' Y 'AJUSTE' ---
    lots_list = movement_controller.handle_get_active_lots_for_selection()
    lot_map = {f"{l['tag_lote']} ({l['nombre_producto']}) - Stock: {l['cantidad_actual']}": l['id_lote'] for l in lots_list}
    ttk.Label(exit_adjustment_frame, text="Seleccionar Lote Existente", style='ContentLabel.TLabel').pack(anchor="w")
    exit_lot_combo = ttk.Combobox(exit_adjustment_frame, values=list(lot_map.keys()), state="readonly")
    exit_lot_combo.pack(fill="x", pady=(2, 5))
    ttk.Label(exit_adjustment_frame, text="Cantidad", style='ContentLabel.TLabel').pack(anchor="w")
    exit_qty_entry = ttk.Entry(exit_adjustment_frame)
    exit_qty_entry.pack(fill="x", pady=(2, 5))
    desc_label = ttk.Label(exit_adjustment_frame, text="Descripción del Ajuste (Obligatoria)", style='ContentLabel.TLabel')
    desc_entry = ttk.Entry(exit_adjustment_frame)

    def on_type_change(event):
        entry_frame.pack_forget()
        exit_adjustment_frame.pack_forget()
        desc_label.pack_forget()
        desc_entry.pack_forget()
        selected_type = type_combo.get()
        if selected_type == "Entrada":
            entry_frame.pack(fill="x", pady=5)
        elif selected_type in ["Salida", "Ajuste"]:
            exit_adjustment_frame.pack(fill="x", pady=5)
            if selected_type == "Ajuste":
                desc_label.pack(anchor="w")
                desc_entry.pack(fill="x", pady=(2, 5))
                
    type_combo.bind("<<ComboboxSelected>>", on_type_change)
    on_type_change(None)

    def guardar_action():
        selected_type = type_combo.get()
        success = False
        if selected_type == "Entrada":
            product_id = product_map.get(entry_product_combo.get())
            data = {'product_id': product_id, 'tag_lote': entry_tag_entry.get().strip(),
                    'cantidad': entry_qty_entry.get().strip(), 'unidad': entry_unit_combo.get(),
                    'fecha_vencimiento': entry_date_entry.get_date(), 'user_id': user_id}
            success = movement_controller.handle_register_entry(data)
        elif selected_type in ["Salida", "Ajuste"]:
            lote_id = lot_map.get(exit_lot_combo.get())
            success = movement_controller.handle_register_exit_or_adjustment(
                id_lote=lote_id, cantidad_str=exit_qty_entry.get().strip(),
                user_id=user_id, movement_type=selected_type, descripcion=desc_entry.get().strip())
        if success:
            show_all_movements_list(parent_frame, user_id)

    button_frame = ttk.Frame(form_frame, style='MainContent.TFrame')
    button_frame.grid(row=1, column=0, pady=20)
    ttk.Button(button_frame, text="Registrar Movimiento", command=guardar_action, style='Action.TButton').pack(side='left', padx=5)
    ttk.Button(button_frame, text="Cancelar", command=lambda: show_all_movements_list(parent_frame, user_id), style='Delete.TButton').pack(side='left', padx=5)
def show_all_movements_list(parent_frame, user_id):
    """Dibuja la tabla de historial de movimientos, ahora como vista principal de Movimientos."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Historial de Movimientos", style='ContentTitle.TLabel').pack(pady=10)
    
    search_bar_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    search_bar_frame.pack(fill='x', padx=10, pady=5)
    ttk.Label(search_bar_frame, text="Filtrar:", style='ContentLabel.TLabel').pack(side='left', padx=(0, 5))
    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_bar_frame, textvariable=search_var)
    search_entry.pack(side='left', fill='x', expand=True)

    container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    container.pack(fill="both", expand=True, padx=10, pady=10)
    
    cols = ("Fecha", "Producto", "Tipo", "Tag / Lote", "Cantidad", "Descripción", "Usuario Responsable")
    tree = ttk.Treeview(container, columns=cols, show="headings", selectmode="browse")
    vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(parent_frame, orient="horizontal", command=tree.xview)
    
    for col in cols: tree.heading(col, text=col)
    tree.column("Fecha", width=160, stretch=tk.NO); tree.column("Producto", width=300)
    tree.column("Descripción", width=250); tree.column("Usuario Responsable", width=200, stretch=tk.NO)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    action_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    action_frame.pack(side='bottom', pady=(5,0), fill='x')
    hsb.pack(side='bottom', fill='x', padx=10, pady=(0, 5))
    vsb.pack(side='right', fill='y')
    tree.pack(side="left", fill="both", expand=True)

    all_movements = []

    def _populate_tree(data_list):
        for i in tree.get_children(): tree.delete(i)
        for mov in data_list:
            fecha = mov['fecha'].strftime('%Y-%m-%d %H:%M:%S')
            tree.insert("", "end", values=(fecha, mov['producto_nombre'], mov['tipo'], mov.get('tag') or 'N/A', mov['cantidad'], mov.get('descripcion') or '', mov['usuario_nombre']))

    def _on_search_change(*args):
        search_term = search_var.get().lower()
        if not search_term: _populate_tree(all_movements)
        else:
            filtered = [m for m in all_movements if search_term in m['producto_nombre'].lower() or (m.get('tag') and search_term in m.get('tag').lower())]
            _populate_tree(filtered)

    search_var.trace_add("write", _on_search_change)
    
    def _load_initial_data():
        nonlocal all_movements
        all_movements = movement_controller.handle_get_all_movements()
        _populate_tree(all_movements)
        
    # --- CORRECCIÓN: Botones de Acción para Movimientos ---
    def on_add_record():
        show_register_movement_form(parent_frame, user_id)

    # El historial no tiene edición ni eliminación, solo registro y refresco.
    ttk.Button(action_frame, text="Registrar Nuevo Movimiento", command=on_add_record, style='Action.TButton').pack(side='left', padx=10)
    ttk.Button(action_frame, text="Refrescar Lista", command=_load_initial_data, style='Action.TButton').pack(side='right', padx=10)

    _load_initial_data()