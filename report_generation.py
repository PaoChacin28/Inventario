# report_management.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk # Para Treeview y Combobox
from datetime import datetime, timedelta # Para manejar fechas
import mysql.connector
from db_connection import conectar_db

# --- Funciones de Utilidad (para estilizar ventanas) ---
def setup_window(window, title, geometry="750x550"):
    window.title(title)
    window.geometry(geometry)
    window.configure(bg="#e0f8f7") # Fondo claro
    window.transient(window.master) # Hace que la ventana sea modal
    window.grab_set() # Captura todos los eventos
    return window

def create_input_field(parent, label_text, entry_width=30, show_char=None):
    frame = ttk.Frame(parent, bg="#e0f8f7")
    frame.pack(pady=3, fill="x", padx=10)
    ttk.Label(frame, text=label_text, bg="#e0f8f7", font=("Arial", 10)).pack(side="left", padx=5)
    entry = ttk.Entry(frame, width=entry_width, font=("Arial", 10), show=show_char)
    entry.pack(side="right", expand=True, fill="x", padx=5)
    return entry

# --- Función de Generación de Reportes ---

def generar_reporte(id_usuario):
    win = setup_window(ttk.Toplevel(), "Generar Reporte de Inventario")

    ttk.Label(win, text="Opciones de Reporte", font=("Arial", 14, "bold"), bg="#e0f8f7").pack(pady=15)

    # Selección del tipo de reporte
    frame_tipo_reporte = ttk.Frame(win, bg="#e0f8f7")
    frame_tipo_reporte.pack(pady=5, fill="x", padx=10)
    ttk.Label(frame_tipo_reporte, text="Tipo de Reporte:", bg="#e0f8f7", font=("Arial", 10)).pack(side="left", padx=5)
    cb_tipo_reporte = ttk.Combobox(frame_tipo_reporte, values=["Stock mínimo", "Productos Por Vencer"], state="readonly", font=("Arial", 10))
    cb_tipo_reporte.set("Stock mínimo") # Valor por defecto
    cb_tipo_reporte.pack(side="right", expand=True, fill="x", padx=5)

    # Campos específicos para cada tipo de reporte
    frame_stock_minimo = ttk.Frame(win, bg="#e0f8f7")
    e_cantidad_minima = create_input_field(frame_stock_minimo, "Cantidad Mínima (Stock):")
    
    frame_productos_vencer = ttk.Frame(win, bg="#e0f8f7")
    e_dias_vencer = create_input_field(frame_productos_vencer, "Días para Vencer:")

    # Mostrar/ocultar campos según el tipo de reporte seleccionado
    def on_report_type_selected(event=None):
        if cb_tipo_reporte.get() == "Stock mínimo":
            frame_productos_vencer.pack_forget()
            frame_stock_minimo.pack(pady=5, fill="x", padx=10)
        elif cb_tipo_reporte.get() == "Productos Por Vencer":
            frame_stock_minimo.pack_forget()
            frame_productos_vencer.pack(pady=5, fill="x", padx=10)
        
        # Asegurarse de que el Treeview se reconfigure al cambiar de opciones
        # No es estrictamente necesario aquí, pero buena práctica si el contenido del Treeview cambiara drásticamente
        # antes de generar el reporte.

    cb_tipo_reporte.bind("<<ComboboxSelected>>", on_report_type_selected)
    on_report_type_selected() # Llamar al inicio para configurar la vista inicial

    # Configuración del Treeview para mostrar resultados del reporte
    tree_frame = ttk.Frame(win, bg="#e0f8f7")
    tree_frame.pack(pady=10, fill="both", expand=True, padx=10)

    # Columnas del Treeview (se ajustarán según el tipo de reporte si es necesario)
    # Por ahora, un conjunto general de columnas para productos
    report_columns = ("ID", "Código", "Nombre", "Tipo", "Cantidad", "Precio", "Fecha Vencimiento", "Proveedor")
    tree = ttk.Treeview(tree_frame, columns=report_columns, show="headings", selectmode="browse")

    for col in report_columns:
        tree.heading(col, text=col, anchor="w")
        tree.column(col, width=80, anchor="w") # Ancho por defecto

    tree.column("ID", width=40)
    tree.column("Nombre", width=150)
    tree.column("Fecha Vencimiento", width=120)

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x')
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.pack(fill="both", expand=True)

    def generar_y_guardar_reporte():
        for item in tree.get_children():
            tree.delete(item) # Limpiar resultados anteriores

        reporte_generado = []
        tipo_reporte_seleccionado = cb_tipo_reporte.get()
        sql_query = ""
        report_title = ""

        db = conectar_db()
        if db is None:
            return
        cursor = db.cursor(dictionary=True)

        try:
            if tipo_reporte_seleccionado == "Stock mínimo":
                try:
                    cantidad_minima = int(e_cantidad_minima.get())
                    if cantidad_minima < 0:
                        messagebox.showwarning("Entrada Inválida", "La cantidad mínima no puede ser negativa.")
                        return
                except ValueError:
                    messagebox.showwarning("Entrada Inválida", "Por favor, ingrese un número entero para la cantidad mínima.")
                    return
                
                report_title = f"Reporte de Stock Mínimo (Cantidad < {cantidad_minima})"
                sql_query = """
                SELECT p.id_producto, p.codigo_producto, p.nombre, p.tipo, p.cantidad, p.precio, p.fecha_vencimiento, prov.nombre AS nombre_proveedor
                FROM producto p
                JOIN proveedor prov ON p.id_proveedor = prov.id_proveedor
                WHERE p.cantidad < %s
                ORDER BY p.cantidad ASC;
                """
                cursor.execute(sql_query, (cantidad_minima,))

            elif tipo_reporte_seleccionado == "Productos Por Vencer":
                try:
                    dias_vencer = int(e_dias_vencer.get())
                    if dias_vencer < 0:
                        messagebox.showwarning("Entrada Inválida", "Los días para vencer no pueden ser negativos.")
                        return
                except ValueError:
                    messagebox.showwarning("Entrada Inválida", "Por favor, ingrese un número entero para los días a vencer.")
                    return
                
                fecha_limite = datetime.now().date() + timedelta(days=dias_vencer)
                report_title = f"Reporte de Productos por Vencer (en los próximos {dias_vencer} días)"
                sql_query = """
                SELECT p.id_producto, p.codigo_producto, p.nombre, p.tipo, p.cantidad, p.precio, p.fecha_vencimiento, prov.nombre AS nombre_proveedor
                FROM producto p
                JOIN proveedor prov ON p.id_proveedor = prov.id_proveedor
                WHERE p.fecha_vencimiento <= %s AND p.fecha_vencimiento >= CURDATE()
                ORDER BY p.fecha_vencimiento ASC;
                """
                cursor.execute(sql_query, (fecha_limite,))
            
            resultados = cursor.fetchall()

            if not resultados:
                messagebox.showinfo("Sin Resultados", f"No se encontraron productos para el '{tipo_reporte_seleccionado}'.")
                return

            for row in resultados:
                tree.insert("", "end", values=(
                    row['id_producto'],
                    row['codigo_producto'],
                    row['nombre'],
                    row['tipo'],
                    row['cantidad'],
                    row['precio'],
                    row['fecha_vencimiento'], # La fecha ya es un objeto date de Python
                    row['nombre_proveedor']
                ))
            
            # Guardar el evento de generación de reporte en la base de datos
            fecha_generacion = datetime.now().date()
            sql_insert_reporte = "INSERT INTO reporte (fecha_generacion, tipo_reporte, id_usuario) VALUES (%s, %s, %s)"
            cursor.execute(sql_insert_reporte, (fecha_generacion, tipo_reporte_seleccionado, id_usuario))
            db.commit()
            messagebox.showinfo("Reporte Generado", f"{report_title} generado y registrado.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al generar el reporte: {err}")
            if db.is_connected():
                db.rollback()
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    ttk.Button(win, text="Generar Reporte", command=generar_y_guardar_reporte,
              font=("Arial", 10, "bold"), bg="#007bff", fg="white", width=20, cursor="hand2").pack(pady=20)
    win.mainloop()