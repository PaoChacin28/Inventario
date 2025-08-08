# views/movement_view.py
import tkinter as tk
from tkinter import ttk
import controllers.movement_controller as movement_controller

# (La función clear_frame no cambia)
def clear_frame(frame):
    for widget in frame.winfo_children(): widget.destroy()

# (La función show_register_movement_form no cambia)
def show_register_movement_form(parent_frame, user_id):
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Registrar Movimiento de Inventario", style='ContentTitle.TLabel').pack(pady=20)
    
    frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    frame.pack(padx=20, pady=10, fill="x")
    frame.columnconfigure(1, weight=1)

    products_list = movement_controller.handle_get_products_for_selection()
    product_display_map = {f"{p['id_producto']} - {p['codigo_producto']} - {p['nombre']}": p['id_producto'] for p in products_list}
    
    ttk.Label(frame, text="Producto:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5)
    product_combo = ttk.Combobox(frame, values=list(product_display_map.keys()), state="readonly", height=10)
    product_combo.grid(row=0, column=1, sticky="ew", pady=5)

    ttk.Label(frame, text="Tipo de Movimiento:", style='ContentLabel.TLabel').grid(row=1, column=0, sticky="w", pady=5)
    type_combo = ttk.Combobox(frame, values=["Entrada", "Salida"], state="readonly")
    type_combo.grid(row=1, column=1, sticky="ew", pady=5)

    ttk.Label(frame, text="Cantidad:", style='ContentLabel.TLabel').grid(row=2, column=0, sticky="w", pady=5)
    quantity_entry = ttk.Entry(frame, width=40)
    quantity_entry.grid(row=2, column=1, sticky="ew", pady=5)
    
    def guardar_action():
        selected_display = product_combo.get()
        product_id = product_display_map.get(selected_display)
        
        success = movement_controller.handle_register_movement(
            product_id, type_combo.get(), quantity_entry.get().strip(), user_id
        )
        if success:
            product_combo.set(''); type_combo.set(''); quantity_entry.delete(0, tk.END)

    ttk.Button(parent_frame, text="Registrar Movimiento", command=guardar_action, style='Action.TButton').pack(pady=20)


def show_all_movements_list(parent_frame):
    """Dibuja una tabla con el historial de todos los movimientos."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Historial de Movimientos", style='ContentTitle.TLabel').pack(pady=20)
    
    container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    container.pack(fill="both", expand=True, padx=10, pady=10)
    
    cols = ("Fecha", "Producto", "Tipo", "Cantidad", "Usuario Responsable")
    tree = ttk.Treeview(container, columns=cols, show="headings")
    for col in cols: tree.heading(col, text=col)

    tree.column("Fecha", width=150); tree.column("Producto", width=250); tree.column("Usuario Responsable", width=200)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)
    
    def cargar_datos():
        for i in tree.get_children(): tree.delete(i)
        movements = movement_controller.handle_get_all_movements()
        for mov in movements:
            # --- CORRECCIÓN AQUÍ ---
            # Ahora los datos vienen como 'fecha' y 'tipo' desde el servicio
            fecha = mov['fecha'].strftime('%Y-%m-%d')
            tree.insert("", "end", values=(fecha, mov['producto_nombre'], mov['tipo'], mov['cantidad'], mov['usuario_nombre']))

    ttk.Button(parent_frame, text="Refrescar", command=cargar_datos, style='Action.TButton').pack(pady=10)
    cargar_datos()

# (La función show_general_inventory_list no necesita cambios)
def show_general_inventory_list(parent_frame):
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Inventario General de Productos", style='ContentTitle.TLabel').pack(pady=20)
    
    container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    container.pack(fill="both", expand=True, padx=10, pady=10)
    
    cols = ("Código", "Nombre", "Tipo", "Stock Actual", "Precio", "Vencimiento")
    tree = ttk.Treeview(container, columns=cols, show="headings")
    for col in cols: tree.heading(col, text=col)

    tree.column("Nombre", width=250); tree.column("Stock Actual", anchor='center')

    tree.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    def cargar_datos():
        for i in tree.get_children(): tree.delete(i)
        products = movement_controller.handle_get_general_inventory()
        for prod in products:
            tree.insert("", "end", values=(
                prod['codigo_producto'], prod['nombre'], prod['tipo'], 
                prod['cantidad'], f"{prod['precio']:.2f}", prod.get('fecha_vencimiento', 'N/A')
            ))

    ttk.Button(parent_frame, text="Refrescar Inventario", command=cargar_datos, style='Action.TButton').pack(pady=10)
    cargar_datos()