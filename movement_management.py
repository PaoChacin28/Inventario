# movement_management.py
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# Asume que db_connection.py está en la misma carpeta
from db_connection import conectar_db 

# Función auxiliar para limpiar el frame
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# --- Funciones de Gestión de Movimientos ---

def registrar_movimiento_internal(parent_frame, id_usuario):
    clear_frame(parent_frame) # Limpia el frame padre antes de construir la nueva UI

    # Título
    ttk.Label(parent_frame, text="Registrar Nuevo Movimiento", style='ContentTitle.TLabel').pack(pady=20)

    # Frame para los campos de entrada
    input_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    input_frame.pack(padx=20, pady=10, fill="both", expand=True)

    input_frame.columnconfigure(0, weight=1)
    input_frame.columnconfigure(1, weight=3) 

    # Campo: Tipo de Movimiento (Entrada/Salida)
    ttk.Label(input_frame, text="Tipo de Movimiento:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    tipo_movimiento_combobox = ttk.Combobox(input_frame, values=["Entrada", "Salida"], state="readonly", font=("Arial", 10), width=28)
    tipo_movimiento_combobox.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
    tipo_movimiento_combobox.set("Entrada") # Valor por defecto

    # Campo: Código de Producto (ahora solo busca por código)
    ttk.Label(input_frame, text="Código de Producto:", style='ContentLabel.TLabel').grid(row=1, column=0, sticky="w", pady=5, padx=5)
    codigo_producto_entry = ttk.Entry(input_frame, font=("Arial", 10), width=30) # Renombrado para mayor claridad
    codigo_producto_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
    
    # Campo: Cantidad
    ttk.Label(input_frame, text="Cantidad:", style='ContentLabel.TLabel').grid(row=2, column=0, sticky="w", pady=5, padx=5)
    cantidad_entry = ttk.Entry(input_frame, font=("Arial", 10), width=30)
    cantidad_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

    def guardar_movimiento():
        tipo = tipo_movimiento_combobox.get()
        codigo_producto = codigo_producto_entry.get() # Obtener el código de producto
        cantidad_str = cantidad_entry.get()
        fecha_actual = datetime.now().date() # Fecha del movimiento (automática)

        if not all([tipo, codigo_producto, cantidad_str]): # Validar el nuevo campo
            messagebox.showwarning("Campos Incompletos", "Por favor, complete todos los campos.")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                messagebox.showerror("Cantidad Inválida", "La cantidad debe ser un número positivo.")
                return
        except ValueError:
            messagebox.showerror("Cantidad Inválida", "La cantidad debe ser un número entero.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            db.start_transaction()

            # 1. Obtener el ID del producto y su cantidad actual usando SOLO el codigo_producto
            cursor.execute("SELECT id_producto, cantidad FROM producto WHERE codigo_producto = %s", (codigo_producto,))
            producto_data = cursor.fetchone()

            if not producto_data:
                messagebox.showerror("Producto No Encontrado", "No se encontró un producto con el código proporcionado.")
                db.rollback() 
                return
            
            id_producto_real = producto_data[0] 
            cantidad_actual = producto_data[1]

            nueva_cantidad = cantidad_actual

            if tipo == "Entrada":
                nueva_cantidad += cantidad
            elif tipo == "Salida":
                if cantidad > cantidad_actual:
                    messagebox.showerror("Stock Insuficiente", f"No hay suficiente stock para la salida. Cantidad disponible: {cantidad_actual}")
                    db.rollback() 
                    return
                nueva_cantidad -= cantidad
            
            # 2. Actualizar la cantidad del producto
            cursor.execute("UPDATE producto SET cantidad = %s WHERE id_producto = %s", (nueva_cantidad, id_producto_real))

            # 3. Registrar el movimiento
            sql_movimiento = "INSERT INTO movimiento (tipo, cantidad, fecha, id_producto, id_usuario) VALUES (%s, %s, %s, %s, %s)"
            val_movimiento = (tipo, cantidad, fecha_actual, id_producto_real, id_usuario)
            cursor.execute(sql_movimiento, val_movimiento)
            
            db.commit() 
            messagebox.showinfo("Éxito", f"Movimiento de '{tipo}' registrado correctamente. Nuevo stock: {nueva_cantidad}")

            # Limpiar campos
            codigo_producto_entry.delete(0, tk.END)
            cantidad_entry.delete(0, tk.END)
            tipo_movimiento_combobox.set("Entrada") 

        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al registrar movimiento: {err}")
            db.rollback() 
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
            db.rollback() 
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    # Botón para registrar el movimiento
    ttk.Button(parent_frame, text="Registrar Movimiento", command=guardar_movimiento, style='Accent.TButton').pack(pady=20)


# --- Consultar Inventario General (dentro del mismo frame) ---
def consultar_inventario_general_internal(parent_frame):
    clear_frame(parent_frame) # Limpia el frame padre

    ttk.Label(parent_frame, text="Inventario General de Productos", style='ContentTitle.TLabel').pack(pady=20)

    # Frame para contener el Treeview y sus Scrollbars
    tree_frame = ttk.Frame(parent_frame)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10) # Mayor padding para mejor estética

    # Crear el Treeview para mostrar los datos
    tree = ttk.Treeview(tree_frame, columns=("ID", "Código", "Nombre", "Tipo", "Ingreso", "Vencimiento", "Precio", "Cantidad", "Proveedor ID"), show="headings", style='Treeview.Treeview')

    # Definir los encabezados de las columnas
    tree.heading("ID", text="ID", anchor=tk.W)
    tree.heading("Código", text="Código", anchor=tk.W)
    tree.heading("Nombre", text="Nombre", anchor=tk.W)
    tree.heading("Tipo", text="Tipo", anchor=tk.W)
    tree.heading("Ingreso", text="F. Ingreso", anchor=tk.W)
    tree.heading("Vencimiento", text="F. Venc.", anchor=tk.W)
    tree.heading("Precio", text="Precio", anchor=tk.W)
    tree.heading("Cantidad", text="Cantidad", anchor=tk.W)
    tree.heading("Proveedor ID", text="ID Prov.", anchor=tk.W)

    # Definir el ancho de las columnas (ajusta según necesidad)
    tree.column("ID", width=50, stretch=tk.NO)
    tree.column("Código", width=100, stretch=tk.NO)
    tree.column("Nombre", width=180, stretch=tk.NO)
    tree.column("Tipo", width=80, stretch=tk.NO)
    tree.column("Ingreso", width=100, stretch=tk.NO)
    tree.column("Vencimiento", width=100, stretch=tk.NO)
    tree.column("Precio", width=80, stretch=tk.NO)
    tree.column("Cantidad", width=80, stretch=tk.NO)
    tree.column("Proveedor ID", width=80, stretch=tk.NO)

    tree.pack(side="left", fill="both", expand=True)

    # Añadir Scrollbars
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x')
    tree.configure(xscrollcommand=hsb.set)

    def cargar_productos():
        # Limpiar Treeview antes de cargar nuevos datos
        for item in tree.get_children():
            tree.delete(item)

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True) # Para acceder a los campos por nombre
        try:
            sql = "SELECT * FROM producto ORDER BY nombre ASC"
            cursor.execute(sql)
            productos = cursor.fetchall()

            if productos:
                for prod in productos:
                    tree.insert("", tk.END, values=(
                        prod['id_producto'],
                        prod['codigo_producto'],
                        prod['nombre'],
                        prod['tipo'],
                        prod['fecha_ingreso'],
                        prod['fecha_vencimiento'],
                        prod['precio'],
                        prod['cantidad'],
                        prod['id_proveedor']
                    ))
            else:
                messagebox.showinfo("Inventario Vacío", "No hay productos registrados en el inventario.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al consultar el inventario: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()
    
    cargar_productos() # Cargar los productos al mostrar esta sección
    
    # Botón para refrescar la lista
    ttk.Button(parent_frame, text="Refrescar Lista", command=cargar_productos, style='TButton').pack(pady=10)


# --- NUEVA FUNCIÓN: Consultar Movimientos Realizados ---
def consultar_movimientos_internal(parent_frame):
    clear_frame(parent_frame)

    ttk.Label(parent_frame, text="Movimientos Realizados", style='ContentTitle.TLabel').pack(pady=20)

    # Frame para contener el Treeview
    tree_frame = ttk.Frame(parent_frame)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Crear el Treeview
    columns = ("ID Mov.", "Tipo", "Cantidad", "Fecha", "Cód. Producto", "Nombre Producto", "Usuario")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style='Treeview.Treeview')

    # Definir encabezados de columnas
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)
    
    # Ajustar anchos específicos
    tree.column("ID Mov.", width=60, stretch=tk.NO)
    tree.column("Tipo", width=80, stretch=tk.NO)
    tree.column("Cantidad", width=80, stretch=tk.NO)
    tree.column("Fecha", width=100, stretch=tk.NO)
    tree.column("Cód. Producto", width=120, stretch=tk.NO)
    tree.column("Nombre Producto", width=180, stretch=tk.NO)
    tree.column("Usuario", width=120, stretch=tk.NO)

    tree.pack(side="left", fill="both", expand=True)

    # Añadir Scrollbars
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x')
    tree.configure(xscrollcommand=hsb.set)

    def cargar_movimientos():
        for item in tree.get_children():
            tree.delete(item)

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True)
        try:
            sql = """
            SELECT 
                m.id_movimiento, 
                m.tipo, 
                m.cantidad, 
                m.fecha, 
                p.codigo_producto, 
                p.nombre AS nombre_producto,
                u.usuario AS nombre_usuario
            FROM movimiento m
            JOIN producto p ON m.id_producto = p.id_producto
            JOIN usuario u ON m.id_usuario = u.id_usuario
            ORDER BY m.fecha DESC, m.id_movimiento DESC
            """
            cursor.execute(sql)
            movimientos = cursor.fetchall()

            if movimientos:
                for mov in movimientos:
                    tree.insert("", tk.END, values=(
                        mov['id_movimiento'],
                        mov['tipo'],
                        mov['cantidad'],
                        mov['fecha'],
                        mov['codigo_producto'],
                        mov['nombre_producto'],
                        mov['nombre_usuario']
                    ))
            else:
                messagebox.showinfo("Sin Movimientos", "No se han registrado movimientos aún.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al consultar los movimientos: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()
    
    cargar_movimientos() # Cargar los movimientos al iniciar la vista
    
    ttk.Button(parent_frame, text="Refrescar Movimientos", command=cargar_movimientos, style='TButton').pack(pady=10)