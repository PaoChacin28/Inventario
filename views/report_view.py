# views/report_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import traceback
import os
import controllers.report_controller as report_controller

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# En views/report_view.py

# ... (tus otras importaciones no cambian) ...

def show_generate_report_form(parent_frame, user_id):
    clear_frame(parent_frame)
    
    # --- LAYOUT DE 3 PARTES (SIN CAMBIOS) ---
    control_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    control_frame.pack(side='top', fill='x', padx=10, pady=(10, 0))

    bottom_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    bottom_frame.pack(side='bottom', fill='x', padx=10, pady=10)
    
    # --- SOLUCIÓN: El contenedor de la tabla y el HSB van juntos ---
    # Esto asegura que el HSB esté directamente debajo de la tabla que controla
    table_container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    table_container.pack(fill="both", expand=True, padx=10, pady=10)

    # --- CONTENIDO DE LA SECCIÓN SUPERIOR (SIN CAMBIOS) ---
    # ... (Todo tu código para el título, combobox y filtros va aquí) ...
    ttk.Label(control_frame, text="Generar Reportes", style='ContentTitle.TLabel').pack(pady=(10, 20))
    field_container = ttk.Frame(control_frame, style='MainContent.TFrame')
    field_container.pack(pady=10)
    ttk.Label(field_container, text="Tipo de Reporte", style='ContentLabel.TLabel').pack(anchor="w")
    report_types = ["Stock General", "Stock Mínimo", "Próximos a Vencer", "Movimientos por Fecha", 
                    "Trazabilidad de Lote", "Movimientos por Producto", "Entradas por Proveedor"]
    type_combobox = ttk.Combobox(field_container, values=report_types, state="readonly", width=50)
    type_combobox.set(report_types[0])
    type_combobox.pack(fill="x", pady=(2, 10))
    filters_frame = ttk.Frame(field_container, style='MainContent.TFrame')
    filters_frame.pack(fill='x', pady=5)
    report_data = []
    report_headers = {}
    try:
        date_filter_frame = ttk.Frame(filters_frame, style='MainContent.TFrame')
        ttk.Label(date_filter_frame, text="Fecha Inicio:").pack(side="left"); 
        start_date_entry = DateEntry(date_filter_frame, date_pattern='yyyy-mm-dd', width=12); start_date_entry.pack(side="left", padx=5)
        ttk.Label(date_filter_frame, text="Fecha Fin:").pack(side="left"); 
        end_date_entry = DateEntry(date_filter_frame, date_pattern='yyyy-mm-dd', width=12); end_date_entry.pack(side="left", padx=5)
        lot_filter_frame = ttk.Frame(filters_frame, style='MainContent.TFrame')
        ttk.Label(lot_filter_frame, text="Lote:").pack(anchor='w'); 
        lots_list = report_controller.get_active_lots_for_selection() or []
        lot_map = {f"{l['tag_lote']} ({l['nombre_producto']}) - Stock: {l['cantidad_actual']}": l['id_lote'] for l in lots_list}
        lot_combo = ttk.Combobox(lot_filter_frame, values=list(lot_map.keys()), state="readonly", width=50); lot_combo.pack(fill='x')
        product_filter_frame = ttk.Frame(filters_frame, style='MainContent.TFrame')
        ttk.Label(product_filter_frame, text="Producto:").pack(anchor='w'); 
        products_list = report_controller.get_products_for_selection() or []
        product_map = {f"{p.get('codigo_producto', p['id_producto'])} - {p['nombre']}": p['id_producto'] for p in products_list}
        product_combo = ttk.Combobox(product_filter_frame, values=list(product_map.keys()), state="readonly", width=50); product_combo.pack(fill='x')
        provider_filter_frame = ttk.Frame(filters_frame, style='MainContent.TFrame')
        ttk.Label(provider_filter_frame, text="Proveedor:").pack(anchor='w'); 
        providers_list = report_controller.get_providers_for_selection() or []
        provider_map = {p['nombre']: p['id_proveedor'] for p in providers_list}
        provider_combo = ttk.Combobox(provider_filter_frame, values=list(provider_map.keys()), state="readonly", width=50); provider_combo.pack(fill='x')
    except Exception:
        traceback.print_exc()
        messagebox.showerror("Error de Carga", "No se pudieron cargar los datos para los filtros. Revise la consola.")
        return
    def on_report_type_change(event):
        for frame in [date_filter_frame, lot_filter_frame, product_filter_frame, provider_filter_frame]: frame.pack_forget()
        selected = type_combobox.get()
        if selected in ["Movimientos por Fecha", "Movimientos por Producto", "Entradas por Proveedor"]: date_filter_frame.pack(fill='x', pady=5)
        if selected == "Trazabilidad de Lote": lot_filter_frame.pack(fill='x', pady=5)
        if selected == "Movimientos por Producto": product_filter_frame.pack(fill='x', pady=5)
        if selected == "Entradas por Proveedor": provider_filter_frame.pack(fill='x', pady=5)
    type_combobox.bind("<<ComboboxSelected>>", on_report_type_change)

    # --- SECCIÓN INFERIOR Y CENTRAL ---

    # El frame de botones va en la sección inferior
    action_frame = ttk.Frame(bottom_frame, style='MainContent.TFrame')
    action_frame.pack(pady=(5,0))
    
    # Creamos el HSB DENTRO del nuevo 'table_container'
    hsb = ttk.Scrollbar(table_container, orient="horizontal")
    hsb.pack(side='bottom', fill='x')

    # La tabla y el VSB también van DENTRO del 'table_container'
    tree = ttk.Treeview(table_container, show="headings", xscrollcommand=hsb.set)
    vsb = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    hsb.config(command=tree.xview)
    
    vsb.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    def generate_report_action():
        nonlocal report_data, report_headers
        selected_report = type_combobox.get()
        params = {}
        # ... (código de recolección de params) ...
        if selected_report in ["Movimientos por Fecha", "Movimientos por Producto", "Entradas por Proveedor"]:
            params = {'start_date': start_date_entry.get_date(), 'end_date': end_date_entry.get_date()}
        if selected_report == "Trazabilidad de Lote": params['lote_id'] = lot_map.get(lot_combo.get())
        if selected_report == "Movimientos por Producto": params['product_id'] = product_map.get(product_combo.get())
        if selected_report == "Entradas por Proveedor": params['provider_id'] = provider_map.get(provider_combo.get())
        
        report_data = report_controller.get_report_data(selected_report, params)
        for i in tree.get_children(): tree.delete(i)
        tree['columns'] = ()
        export_button.config(state="disabled")

        if report_data:
            report_headers = {k: k.replace('_', ' ').title() for k in report_data[0].keys()}
            tree['columns'] = list(report_headers.keys())
            tree.column("#0", width=0, stretch=tk.NO)

            # --- LÓGICA DE COLUMNAS RESTAURADA Y CORRECTA ---
            # Identificamos las columnas que queremos que sean flexibles
            flexible_columns = ['Producto Nombre', 'Descripcion', 'Usuario Nombre', 'Nombre']

            for key, name in report_headers.items():
                tree.heading(key, text=name)
                # Si la columna NO es flexible, le damos un ancho fijo y NO se estira.
                if name not in flexible_columns:
                    tree.column(key, anchor='center', width=120, stretch=tk.NO)
                else:
                    # Si ES flexible, le damos un ancho mínimo pero SÍ permitimos que se estire.
                    tree.column(key, anchor='w', minwidth=150, width=250)
            
            for row in report_data:
                values = [str(row.get(key, '')) for key in report_headers.keys()]
                tree.insert("", "end", values=values)

            export_button.config(state="normal")
        elif report_data is not None:
             messagebox.showinfo("Reporte Vacío", "La consulta no arrojó resultados.")

    def export_action():
        # ... (Tu lógica de exportar no cambia)
        report_title = type_combobox.get()
        if not report_data: messagebox.showwarning("Sin Datos", "Primero debe generar un reporte con datos."); return
        path = report_controller.preview_report_as_pdf(report_data, report_headers, report_title)
        if path: messagebox.showinfo("Exportación Exitosa", "El reporte se ha abierto en su visor de PDF.\nDesde allí puede guardarlo o imprimirlo.")

    # --- Botones ---
    ttk.Button(field_container, text="Generar Reporte", command=generate_report_action, style='Action.TButton').pack(pady=15)
    export_button = ttk.Button(action_frame, text="Exportar PDF", command=export_action, state="disabled", style='Action.TButton')
    export_button.pack(side='right')
    on_report_type_change(None)