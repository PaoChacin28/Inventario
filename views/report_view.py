# views/report_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import controllers.report_controller as report_controller

def clear_frame(frame):
    """Limpia todos los widgets de un frame."""
    for widget in frame.winfo_children(): widget.destroy()

def show_generate_report_form(parent_frame, user_id):
    """Dibuja la interfaz para la generación de reportes con la tabla corregida."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Generar Reportes", style='ContentTitle.TLabel').pack(pady=20)
    
    # --- Frame para los controles de generación ---
    control_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    control_frame.pack(padx=20, pady=10, fill="x", anchor="n")
    control_frame.columnconfigure(0, weight=1) # Para centrar el contenido
    
    field_container = ttk.Frame(control_frame, style='MainContent.TFrame')
    field_container.grid(row=0, column=0, sticky="n", ipadx=100)
    
    # Widgets de control
    ttk.Label(field_container, text="Tipo de Reporte", style='ContentLabel.TLabel').pack(anchor="w")
    report_types = ["Stock mínimo", "Productos Por Vencer"]
    type_combobox = ttk.Combobox(field_container, values=report_types, state="readonly")
    type_combobox.set(report_types[0])
    type_combobox.pack(fill="x", pady=(2, 10))
    
    # El botón ahora está junto a su control
    ttk.Button(field_container, text="Generar Reporte", command=lambda: generar_action(), style='Action.TButton').pack()

    # --- Título y Contenedor de la tabla ---
    report_title_label = ttk.Label(parent_frame, text="Resultados del Reporte", style='ContentLabel.TLabel')
    report_title_label.pack(pady=(20, 5), anchor="n")

    results_container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    results_container.pack(padx=10, pady=10, fill="both", expand=True)

    # --- CORRECCIÓN: Definición de columnas y configuración ---
    # 1. Crear los widgets
    cols = ("Código", "Nombre", "Tipo", "Unidad", "Cantidad", "Vencimiento")
    tree = ttk.Treeview(results_container, columns=cols, show="headings")
    vsb = ttk.Scrollbar(results_container, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(parent_frame, orient="horizontal", command=tree.xview)
    
    # 2. Configurar los widgets
    tree.heading("Código", text="Código")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Tipo", text="Tipo")
    tree.heading("Unidad", text="Unidad")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Vencimiento", text="Vencimiento")

    tree.column("Código", width=120, stretch=tk.NO, anchor='w')
    tree.column("Nombre", width=300) # Columna flexible
    tree.column("Tipo", width=100, stretch=tk.NO, anchor='center')
    tree.column("Unidad", width=100, stretch=tk.NO, anchor='center')
    tree.column("Cantidad", width=80, stretch=tk.NO, anchor='center')
    tree.column("Vencimiento", width=120, stretch=tk.NO, anchor='center')
    
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # 3. Empaquetar los widgets
    action_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    action_frame.pack(side='bottom', pady=(5,0), fill='x') # Contenedor para botones inferiores (si los hubiera)
    hsb.pack(side='bottom', fill='x', padx=10, pady=(0, 5))
    vsb.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)
    
    def generar_action():
        report_data = report_controller.handle_generate_report(type_combobox.get(), user_id)
        for item in tree.get_children(): tree.delete(item)
        report_title_label.config(text=f"Resultados para: {type_combobox.get()}")
        if report_data is not None:
            for row in report_data:
                tree.insert("", "end", values=(
                    row['codigo_producto'],
                    row['nombre'],
                    row['tipo'],
                    row.get('unidad_medida', 'N/A'), # Añadimos la unidad
                    row['cantidad'],
                    row.get('fecha_vencimiento', 'N/A')
                ))