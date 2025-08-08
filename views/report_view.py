# views/report_view.py
import tkinter as tk
from tkinter import ttk
import controllers.report_controller as report_controller

def clear_frame(frame):
    for widget in frame.winfo_children(): widget.destroy()

def show_generate_report_form(parent_frame, user_id):
    """Dibuja la interfaz para la generación de reportes."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Generar Reportes", style='ContentTitle.TLabel').pack(pady=20)

    # --- Controles ---
    control_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    control_frame.pack(padx=20, pady=10, fill="x")

    ttk.Label(control_frame, text="Tipo de Reporte:", style='ContentLabel.TLabel').pack(side="left", padx=5)
    
    report_types = ["Stock mínimo", "Productos Por Vencer"]
    type_combobox = ttk.Combobox(control_frame, values=report_types, state="readonly", width=30)
    type_combobox.pack(side="left", padx=5, expand=True, fill="x")
    type_combobox.set(report_types[0])

    # --- Título dinámico ---
    report_title_label = ttk.Label(parent_frame, text="Resultados del Reporte", style='ContentLabel.TLabel')
    report_title_label.pack(pady=(10, 5))

    # --- Vista de Resultados (Treeview) ---
    results_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    results_frame.pack(padx=20, pady=10, fill="both", expand=True)

    columns = ("ID", "Código", "Nombre", "Tipo", "Cantidad", "Vencimiento")
    tree = ttk.Treeview(results_frame, columns=columns, show="headings")
    for col in columns: tree.heading(col, text=col)

    # Ajuste de columnas
    tree.column("ID", width=60, anchor='center'); tree.column("Nombre", width=200); tree.column("Cantidad", width=80, anchor='center')

    tree.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    def generar_action():
        """Llama al controlador y muestra los resultados en la tabla."""
        report_type = type_combobox.get()
        
        # El controlador se encarga de los mensajes, aquí solo procesamos los datos
        report_data = report_controller.handle_generate_report(report_type, user_id)
        
        # Limpiar la tabla siempre, antes de mostrar nuevos datos
        for item in tree.get_children():
            tree.delete(item)

        report_title_label.config(text=f"Resultados para: {report_type}")

        # Si el controlador devuelve datos (incluso una lista vacía), los procesamos
        if report_data is not None:
            for row in report_data:
                tree.insert("", "end", values=(
                    row['id_producto'],
                    row['codigo_producto'],
                    row['nombre'],
                    row['tipo'],
                    row['cantidad'],
                    f"{row.get('fecha_vencimiento', 'N/A'):.2f}" # Usar .get por si no aplica
                ))

    # --- Botón de Acción ---
    ttk.Button(parent_frame, text="Generar Reporte", command=generar_action, style='Action.TButton').pack(pady=20)