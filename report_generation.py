# report_management.py
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime, timedelta

# Asume que db_connection.py está en la misma carpeta
from db_connection import conectar_db 

# Función auxiliar para limpiar el frame
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# --- Funciones de Gestión de Reportes ---

def generar_reporte_internal(parent_frame, id_usuario):
    clear_frame(parent_frame) # Limpia el frame padre antes de construir la nueva UI

    # Título
    ttk.Label(parent_frame, text="Generar Reportes", style='ContentTitle.TLabel').pack(pady=20)

    # Frame para los controles del reporte
    control_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    control_frame.pack(padx=20, pady=10, fill="x")

    ttk.Label(control_frame, text="Tipo de Reporte:", style='ContentLabel.TLabel').pack(side="left", padx=5)
    
    reporte_tipos = ["Stock mínimo", "Productos Por Vencer"]
    tipo_reporte_combobox = ttk.Combobox(control_frame, values=reporte_tipos, state="readonly", font=("Arial", 10), width=30)
    tipo_reporte_combobox.pack(side="left", padx=5, expand=True, fill="x")
    tipo_reporte_combobox.set("Stock mínimo") # Valor por defecto

    # Frame para el Treeview (donde se mostrarán los resultados)
    report_display_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    report_display_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Configuración del Treeview para mostrar los resultados del reporte
    columns = ("ID Producto", "Código", "Nombre", "Tipo", "Cantidad", "Fecha Vencimiento", "Precio")
    report_tree = ttk.Treeview(report_display_frame, columns=columns, show="headings", style='Treeview.Treeview')

    # Definir encabezados de columnas
    for col in columns:
        report_tree.heading(col, text=col)
        report_tree.column(col, anchor="center", width=100) # Ancho por defecto

    # Ajustes de ancho específicos para algunas columnas
    report_tree.column("ID Producto", width=80)
    report_tree.column("Código", width=120)
    report_tree.column("Nombre", width=150)
    report_tree.column("Fecha Vencimiento", width=120)
    report_tree.column("Cantidad", width=80)
    report_tree.column("Precio", width=80)

    report_tree.pack(side="left", fill="both", expand=True)

    # Scrollbar para el Treeview
    scrollbar = ttk.Scrollbar(report_display_frame, orient="vertical", command=report_tree.yview)
    scrollbar.pack(side="right", fill="y")
    report_tree.configure(yscrollcommand=scrollbar.set)

    def generar_y_mostrar_reporte():
        tipo_seleccionado = tipo_reporte_combobox.get()
        
        if not tipo_seleccionado:
            messagebox.showwarning("Selección Incompleta", "Por favor, seleccione un tipo de reporte.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True) # Para obtener resultados como diccionarios
        try:
            # Limpiar Treeview antes de cargar nuevos datos
            for item in report_tree.get_children():
                report_tree.delete(item)

            if tipo_seleccionado == "Stock mínimo":
                # Definimos un umbral de stock bajo, por ejemplo, 10 unidades
                stock_minimo_umbral = 10 
                sql = "SELECT id_producto, codigo_producto, nombre, tipo, cantidad, fecha_vencimiento, precio FROM producto WHERE cantidad <= %s ORDER BY cantidad ASC"
                cursor.execute(sql, (stock_minimo_umbral,))
                report_title_display.config(text=f"Reporte de Stock Mínimo (Cantidad <= {stock_minimo_umbral})") # Actualizar título
            elif tipo_seleccionado == "Productos Por Vencer":
                # Productos que vencen en los próximos 30 días
                fecha_limite = datetime.now().date() + timedelta(days=30)
                sql = "SELECT id_producto, codigo_producto, nombre, tipo, cantidad, fecha_vencimiento, precio FROM producto WHERE fecha_vencimiento <= %s ORDER BY fecha_vencimiento ASC"
                cursor.execute(sql, (fecha_limite,))
                report_title_display.config(text=f"Reporte de Productos por Vencer (en los próximos 30 días)") # Actualizar título
            
            resultados = cursor.fetchall()

            if not resultados:
                messagebox.showinfo("Reporte Vacío", f"No se encontraron productos para el reporte de '{tipo_seleccionado}'.")
                report_title_display.config(text=f"Reporte de {tipo_seleccionado} (No hay datos)")
                return

            for row in resultados:
                report_tree.insert("", "end", values=(
                    row['id_producto'],
                    row['codigo_producto'],
                    row['nombre'],
                    row['tipo'],
                    row['cantidad'],
                    row['fecha_vencimiento'], # La fecha ya es un objeto date
                    f"{row['precio']:.2f}" # Formatear precio a 2 decimales
                ))

            # --- Registrar la generación del reporte en la tabla 'reporte' ---
            sql_registro_reporte = "INSERT INTO reporte (fecha_generacion, tipo_reporte, id_usuario) VALUES (%s, %s, %s)"
            val_registro_reporte = (datetime.now().date(), tipo_seleccionado, id_usuario)
            cursor.execute(sql_registro_reporte, val_registro_reporte)
            db.commit()
            messagebox.showinfo("Reporte Generado", f"El reporte de '{tipo_seleccionado}' ha sido generado y registrado.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al generar reporte: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()
    
    # Título dinámico para el reporte (se actualiza al generar)
    report_title_display = ttk.Label(parent_frame, text="Detalles del Reporte", style='ContentSubtitle.TLabel')
    report_title_display.pack(pady=(10, 5))

    # Botón para generar el reporte
    ttk.Button(parent_frame, text="Generar Reporte", command=generar_y_mostrar_reporte, style='Accent.TButton').pack(pady=20)