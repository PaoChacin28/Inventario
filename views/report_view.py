# views/report_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from utils import exporter
import controllers.report_controller as report_controller

def clear_frame(frame):
    """Limpia todos los widgets de un frame."""
    for widget in frame.winfo_children(): widget.destroy()

def show_generate_report_form(parent_frame, user_id):
    """Dibuja la interfaz dinámica para la generación y exportación de reportes."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Generar Reportes", style='ContentTitle.TLabel').pack(pady=20)
    
    # --- Frame de Controles (basado en tu layout funcional) ---
    control_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    control_frame.pack(padx=20, pady=10, fill="x", anchor="n")
    control_frame.columnconfigure(0, weight=1)
    
    field_container = ttk.Frame(control_frame, style='MainContent.TFrame')
    field_container.grid(row=0, column=0, sticky="n", ipadx=150)
    
    ttk.Label(field_container, text="Tipo de Reporte", style='ContentLabel.TLabel').pack(anchor="w")
    report_types = ["Stock Mínimo", "Próximos a Vencer", "Movimientos por Fecha", 
                    "Trazabilidad de Lote", "Movimientos por Producto", "Entradas por Proveedor"]
    type_combobox = ttk.Combobox(field_container, values=report_types, state="readonly", width=40)
    type_combobox.set(report_types[0])
    type_combobox.pack(fill="x", pady=(2, 10))

    # --- Contenedor para filtros dinámicos ---
    filters_frame = ttk.Frame(field_container, style='MainContent.TFrame')
    filters_frame.pack(fill='x')
    
    report_data = []
    report_headers = {}
    
    # --- WIDGETS DE FILTROS (con nombres de variable únicos) ---
    try:
        date_filter_frame = ttk.Frame(filters_frame, style='MainContent.TFrame'); 
        ttk.Label(date_filter_frame, text="Fecha Inicio:").pack(side="left"); 
        start_date_entry = DateEntry(date_filter_frame, date_pattern='yyyy-mm-dd', width=12); 
        start_date_entry.pack(side="left", padx=5); 
        ttk.Label(date_filter_frame, text="Fecha Fin:").pack(side="left"); 
        end_date_entry = DateEntry(date_filter_frame, date_pattern='yyyy-mm-dd', width=12); 
        end_date_entry.pack(side="left", padx=5)

        lot_filter_frame = ttk.Frame(filters_frame, style='MainContent.TFrame'); 
        ttk.Label(lot_filter_frame, text="Lote:").pack(anchor='w'); 
        lots_list = report_controller.get_active_lots_for_selection() or []; 
        lot_map = {f"{l['tag_lote']} ({l['nombre_producto']}) - Stock: {l['cantidad_actual']}": l['id_lote'] for l in lots_list}; 
        lot_combo = ttk.Combobox(lot_filter_frame, values=list(lot_map.keys()), state="readonly"); 
        lot_combo.pack(fill='x')

        product_filter_frame = ttk.Frame(filters_frame, style='MainContent.TFrame'); 
        ttk.Label(product_filter_frame, text="Producto:").pack(anchor='w'); 
        products_list = report_controller.get_products_for_selection() or []; 
        product_map = {f"{p['id_producto']} - {p['nombre']}": p['id_producto'] for p in products_list}; 
        product_combo = ttk.Combobox(product_filter_frame, values=list(product_map.keys()), state="readonly"); 
        product_combo.pack(fill='x')

        provider_filter_frame = ttk.Frame(filters_frame, style='MainContent.TFrame'); 
        ttk.Label(provider_filter_frame, text="Proveedor:").pack(anchor='w'); 
        providers_list = report_controller.get_providers_for_selection() or []; 
        provider_map = {p['nombre']: p['id_proveedor'] for p in providers_list}; 
        provider_combo = ttk.Combobox(provider_filter_frame, values=list(provider_map.keys()), state="readonly"); 
        provider_combo.pack(fill='x')
    except Exception as e:
        messagebox.showerror("Error de Carga", f"No se pudieron cargar los datos para los filtros.\nError: {e}")
        return

    def on_report_type_change(event):
        for frame in [date_filter_frame, lot_filter_frame, product_filter_frame, provider_filter_frame]: frame.pack_forget()
        selected = type_combobox.get()
        if selected in ["Movimientos por Fecha", "Movimientos por Producto", "Entradas por Proveedor"]: date_filter_frame.pack()
        if selected == "Trazabilidad de Lote": lot_filter_frame.pack()
        if selected == "Movimientos por Producto": product_filter_frame.pack()
        if selected == "Entradas por Proveedor": provider_filter_frame.pack()
    type_combobox.bind("<<ComboboxSelected>>", on_report_type_change)

    # --- Contenedor de la tabla ---
    results_container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    results_container.pack(padx=10, pady=10, fill="both", expand=True)
    
    tree = ttk.Treeview(results_container, show="headings")
    vsb = ttk.Scrollbar(results_container, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(parent_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    action_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    action_frame.pack(side='bottom', pady=(5,0), fill='x')
    hsb.pack(side='bottom', fill='x', padx=10, pady=(0, 5))
    vsb.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    def generate_report_action():
        nonlocal report_data, report_headers
        selected_report = type_combobox.get()
        params = {}
        report_headers = {}

        if selected_report in ["Movimientos por Fecha", "Movimientos por Producto", "Entradas por Proveedor"]:
            params = {'start_date': start_date_entry.get_date(), 'end_date': end_date_entry.get_date()}
        if selected_report == "Trazabilidad de Lote": params['lote_id'] = lot_map.get(lot_combo.get())
        if selected_report == "Movimientos por Producto": params['product_id'] = product_map.get(product_combo.get())
        if selected_report == "Entradas por Proveedor": params['provider_id'] = provider_map.get(provider_combo.get())
        
        report_data = report_controller.get_report_data(selected_report, params)
        
        for i in tree.get_children(): tree.delete(i)
        tree['columns'] = () # Limpiar columnas anteriores

        if report_data is not None:
            if not report_data:
                messagebox.showinfo("Reporte Vacío", "La consulta no arrojó resultados para los filtros seleccionados.")
            else:
                report_headers = {k: k.replace('_', ' ').title() for k in report_data[0].keys()}
                tree['columns'] = list(report_headers.keys())
                tree.column("#0", width=0, stretch=tk.NO)
                for key, name in report_headers.items():
                    tree.heading(key, text=name)
                    tree.column(key, anchor='w', width=150)
                
                for row in report_data:
                    values_to_insert = [str(row.get(key, '')) for key in report_headers.keys()]
                    tree.insert("", "end", values=values_to_insert)
            
            export_button.config(state="normal" if report_data else "disabled")
        else:
            export_button.config(state="disabled")
        
    def export_report_action():
        exporter.export_to_csv(report_data, report_headers, default_filename=type_combobox.get().replace(" ", "_"))

    ttk.Button(field_container, text="Generar Reporte", command=generate_report_action, style='Action.TButton').pack(pady=10)
    export_button = ttk.Button(action_frame, text="Exportar Reporte", command=export_report_action, state="disabled", style='Search.TButton')
    export_button.pack(side='right', padx=10)
    
    on_report_type_change(None) # Configurar filtros iniciales