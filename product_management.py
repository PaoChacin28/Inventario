# product_management.py
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# Asume que db_connection.py está en la misma carpeta
from db_connection import conectar_db 

# Función auxiliar para limpiar el frame (puede ser útil en cada módulo o importarse si está en un util.py)
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# --- Funciones de Gestión de Productos ---

def registrar_producto_internal(parent_frame):
    clear_frame(parent_frame) # Limpia el frame padre antes de construir la nueva UI

    # Configurar estilos para los botones de acción dentro de los formularios
    style = ttk.Style(parent_frame)
    style.configure('Action.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#4CAF50", foreground='white', borderwidth=0, relief="flat") # Un verde para "Guardar"
    style.map('Action.TButton', background=[('active', "#45A049")])

    style.configure('Delete.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#f44336", foreground='white', borderwidth=0, relief="flat") # Un rojo para "Eliminar"
    style.map('Delete.TButton', background=[('active', "#DA190B")])

    style.configure('Search.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#2196F3", foreground='white', borderwidth=0, relief="flat") # Un azul para "Buscar"
    style.map('Search.TButton', background=[('active', "#0B7CDA")])


    # Título
    ttk.Label(parent_frame, text="Registrar Nuevo Producto", style='ContentTitle.TLabel').pack(pady=20)

    # Frame para los campos de entrada para mejor organización
    input_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    input_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Usar grid para los campos del formulario para un mejor control del layout
    input_frame.columnconfigure(0, weight=1)
    input_frame.columnconfigure(1, weight=3) # Dar más espacio a las entradas

    # Campo: Código de Producto
    ttk.Label(input_frame, text="Código de Producto:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    codigo_producto_entry = ttk.Entry(input_frame, font=("Arial", 10), width=30)
    codigo_producto_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

    # Campo: Nombre
    ttk.Label(input_frame, text="Nombre:", style='ContentLabel.TLabel').grid(row=1, column=0, sticky="w", pady=5, padx=5)
    nombre_entry = ttk.Entry(input_frame, font=("Arial", 10), width=30)
    nombre_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

    # Campo: Tipo (Carnicos, Viveres)
    ttk.Label(input_frame, text="Tipo:", style='ContentLabel.TLabel').grid(row=2, column=0, sticky="w", pady=5, padx=5)
    tipo_combobox = ttk.Combobox(input_frame, values=["Carnicos", "Viveres"], state="readonly", font=("Arial", 10), width=28)
    tipo_combobox.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
    tipo_combobox.set("Carnicos") # Valor por defecto

    # Campo: Fecha de Ingreso
    ttk.Label(input_frame, text="Fecha de Ingreso (YYYY-MM-DD):", style='ContentLabel.TLabel').grid(row=3, column=0, sticky="w", pady=5, padx=5)
    fecha_ingreso_entry = ttk.Entry(input_frame, font=("Arial", 10), width=30)
    fecha_ingreso_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=5)
    fecha_ingreso_entry.insert(0, datetime.now().strftime("%Y-%m-%d")) # Fecha actual por defecto

    # Campo: Fecha de Vencimiento
    ttk.Label(input_frame, text="Fecha de Vencimiento (YYYY-MM-DD):", style='ContentLabel.TLabel').grid(row=4, column=0, sticky="w", pady=5, padx=5)
    fecha_vencimiento_entry = ttk.Entry(input_frame, font=("Arial", 10), width=30)
    fecha_vencimiento_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=5)

    # Campo: Precio
    ttk.Label(input_frame, text="Precio:", style='ContentLabel.TLabel').grid(row=5, column=0, sticky="w", pady=5, padx=5)
    precio_entry = ttk.Entry(input_frame, font=("Arial", 10), width=30)
    precio_entry.grid(row=5, column=1, sticky="ew", pady=5, padx=5)

    # Campo: Cantidad
    ttk.Label(input_frame, text="Cantidad:", style='ContentLabel.TLabel').grid(row=6, column=0, sticky="w", pady=5, padx=5)
    cantidad_entry = ttk.Entry(input_frame, font=("Arial", 10), width=30)
    cantidad_entry.grid(row=6, column=1, sticky="ew", pady=5, padx=5)

    # Campo: ID Proveedor (asumiendo que necesitas el ID)
    ttk.Label(input_frame, text="ID Proveedor:", style='ContentLabel.TLabel').grid(row=7, column=0, sticky="w", pady=5, padx=5)
    id_proveedor_entry = ttk.Entry(input_frame, font=("Arial", 10), width=30)
    id_proveedor_entry.grid(row=7, column=1, sticky="ew", pady=5, padx=5)


    def guardar_producto():
        codigo_producto = codigo_producto_entry.get().strip()
        nombre = nombre_entry.get().strip()
        tipo = tipo_combobox.get().strip()
        fecha_ingreso_str = fecha_ingreso_entry.get().strip()
        fecha_vencimiento_str = fecha_vencimiento_entry.get().strip()
        precio_str = precio_entry.get().strip()
        cantidad_str = cantidad_entry.get().strip()
        id_proveedor_str = id_proveedor_entry.get().strip()

        # Validación de campos obligatorios
        missing_fields = []
        if not codigo_producto:
            missing_fields.append("Código de Producto")
        if not nombre:
            missing_fields.append("Nombre")
        if not tipo:
            missing_fields.append("Tipo")
        if not fecha_ingreso_str:
            missing_fields.append("Fecha de Ingreso")
        if not fecha_vencimiento_str:
            missing_fields.append("Fecha de Vencimiento")
        if not precio_str:
            missing_fields.append("Precio")
        if not cantidad_str:
            missing_fields.append("Cantidad")
        if not id_proveedor_str:
            missing_fields.append("ID Proveedor")

        if missing_fields:
            messagebox.showwarning("Campos Incompletos", 
                                   "Los siguientes campos son obligatorios y no pueden estar vacíos:\n\n- " + 
                                   "\n- ".join(missing_fields))
            return

        try:
            # Validaciones de tipo de datos
            fecha_ingreso = datetime.strptime(fecha_ingreso_str, "%Y-%m-%d").date()
            fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d").date()
            precio = float(precio_str)
            cantidad = int(cantidad_str)
            id_proveedor = int(id_proveedor_str) 

            if precio <= 0:
                messagebox.showerror("Error de Valores", "El precio debe ser un número positivo mayor que cero.")
                return
            if cantidad < 0: # Cantidad puede ser 0 al inicio, pero no negativa
                messagebox.showerror("Error de Valores", "La cantidad no puede ser un número negativo.")
                return
            if fecha_vencimiento < fecha_ingreso:
                messagebox.showerror("Error de Fechas", "La fecha de vencimiento no puede ser anterior a la fecha de ingreso.")
                return


        except ValueError as e:
            messagebox.showerror("Error de Formato", f"Verifique el formato de los datos:\n\n- Fechas: YYYY-MM-DD\n- Precio: Numérico (ej. 10.50)\n- Cantidad: Número entero\n- ID Proveedor: Número entero\n\nDetalle del error: {e}")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            sql = "INSERT INTO producto (codigo_producto, nombre, tipo, fecha_ingreso, fecha_vencimiento, precio, cantidad, id_proveedor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (codigo_producto, nombre, tipo, fecha_ingreso, fecha_vencimiento, precio, cantidad, id_proveedor)
            cursor.execute(sql, val)
            db.commit()
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")
            
            # Limpiar los campos después de registrar
            codigo_producto_entry.delete(0, tk.END)
            nombre_entry.delete(0, tk.END)
            tipo_combobox.set("Carnicos") # Resetear a valor por defecto
            fecha_ingreso_entry.delete(0, tk.END)
            fecha_ingreso_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            fecha_vencimiento_entry.delete(0, tk.END)
            precio_entry.delete(0, tk.END)
            cantidad_entry.delete(0, tk.END)
            id_proveedor_entry.delete(0, tk.END)

        except mysql.connector.Error as err:
            if err.errno == 1062: # Código de error para entrada duplicada (UNIQUE constraint)
                messagebox.showerror("Error de Registro", "El código de producto ya existe. Por favor, use un código diferente.")
            elif err.errno == 1452: # Código de error para FK constraint fail (Proveedor no existe)
                 messagebox.showerror("Error de Registro", "El ID de Proveedor no existe o es inválido. Por favor, asegúrese de que el proveedor exista.")
            else:
                messagebox.showerror("Error de Base de Datos", f"Error al registrar producto: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    # Botón de Guardar
    ttk.Button(parent_frame, text="Guardar Producto", command=guardar_producto, style='Action.TButton').pack(pady=20)


def consultar_producto_internal(parent_frame):
    clear_frame(parent_frame)
    style = ttk.Style(parent_frame)
    style.configure('Action.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#4CAF50", foreground='white', borderwidth=0, relief="flat") 
    style.map('Action.TButton', background=[('active', "#45A049")])
    style.configure('Search.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#2196F3", foreground='white', borderwidth=0, relief="flat") 
    style.map('Search.TButton', background=[('active', "#0B7CDA")])


    ttk.Label(parent_frame, text="Consultar Producto Específico", style='ContentTitle.TLabel').pack(pady=20)

    search_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    search_frame.pack(padx=20, pady=10, fill="x")
    search_frame.columnconfigure(0, weight=1)
    search_frame.columnconfigure(1, weight=3)
    search_frame.columnconfigure(2, weight=1)

    ttk.Label(search_frame, text="Código de Producto:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    codigo_search_entry = ttk.Entry(search_frame, font=("Arial", 10), width=30)
    codigo_search_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

    details_frame = ttk.LabelFrame(parent_frame, text="Detalles del Producto", style='MainContent.TFrame')
    details_frame.pack(padx=20, pady=10, fill="both", expand=True)
    details_frame.columnconfigure(0, weight=1)
    details_frame.columnconfigure(1, weight=3)

    # Variables para mostrar los detalles del producto
    id_producto_var = tk.StringVar()
    nombre_var = tk.StringVar()
    tipo_var = tk.StringVar()
    fecha_ingreso_var = tk.StringVar()
    fecha_vencimiento_var = tk.StringVar()
    precio_var = tk.StringVar()
    cantidad_var = tk.StringVar()
    id_proveedor_var = tk.StringVar()

    ttk.Label(details_frame, text="ID:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=id_producto_var, style='ContentLabel.TLabel').grid(row=0, column=1, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, text="Nombre:", style='ContentLabel.TLabel').grid(row=1, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=nombre_var, style='ContentLabel.TLabel').grid(row=1, column=1, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, text="Tipo:", style='ContentLabel.TLabel').grid(row=2, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=tipo_var, style='ContentLabel.TLabel').grid(row=2, column=1, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, text="Fecha Ingreso:", style='ContentLabel.TLabel').grid(row=3, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=fecha_ingreso_var, style='ContentLabel.TLabel').grid(row=3, column=1, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, text="Fecha Vencimiento:", style='ContentLabel.TLabel').grid(row=4, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=fecha_vencimiento_var, style='ContentLabel.TLabel').grid(row=4, column=1, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, text="Precio:", style='ContentLabel.TLabel').grid(row=5, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=precio_var, style='ContentLabel.TLabel').grid(row=5, column=1, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, text="Cantidad:", style='ContentLabel.TLabel').grid(row=6, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=cantidad_var, style='ContentLabel.TLabel').grid(row=6, column=1, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, text="ID Proveedor:", style='ContentLabel.TLabel').grid(row=7, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=id_proveedor_var, style='ContentLabel.TLabel').grid(row=7, column=1, sticky="w", pady=2, padx=5)

    def buscar_producto():
        codigo_producto = codigo_search_entry.get().strip()
        if not codigo_producto:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese el código del producto a buscar.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM producto WHERE codigo_producto = %s"
            cursor.execute(sql, (codigo_producto,))
            producto = cursor.fetchone()

            if producto:
                id_producto_var.set(producto['id_producto'])
                nombre_var.set(producto['nombre'])
                tipo_var.set(producto['tipo'])
                fecha_ingreso_var.set(producto['fecha_ingreso'])
                fecha_vencimiento_var.set(producto['fecha_vencimiento'])
                precio_var.set(f"{producto['precio']:.2f}")
                cantidad_var.set(producto['cantidad'])
                id_proveedor_var.set(producto['id_proveedor'] if producto['id_proveedor'] else "N/A")
                messagebox.showinfo("Producto Encontrado", f"Producto '{producto['nombre']}' encontrado.")
            else:
                id_producto_var.set("")
                nombre_var.set("")
                tipo_var.set("")
                fecha_ingreso_var.set("")
                fecha_vencimiento_var.set("")
                precio_var.set("")
                cantidad_var.set("")
                id_proveedor_var.set("")
                messagebox.showwarning("No Encontrado", f"No se encontró ningún producto con el código '{codigo_producto}'.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al buscar producto: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    ttk.Button(search_frame, text="Buscar", command=buscar_producto, style='Search.TButton').grid(row=0, column=2, sticky="ew", pady=5, padx=5)


def editar_producto_internal(parent_frame):
    clear_frame(parent_frame)
    style = ttk.Style(parent_frame)
    style.configure('Action.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#4CAF50", foreground='white', borderwidth=0, relief="flat") 
    style.map('Action.TButton', background=[('active', "#45A049")])
    style.configure('Search.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#2196F3", foreground='white', borderwidth=0, relief="flat") 
    style.map('Search.TButton', background=[('active', "#0B7CDA")])


    ttk.Label(parent_frame, text="Editar Producto", style='ContentTitle.TLabel').pack(pady=20)

    search_edit_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    search_edit_frame.pack(padx=20, pady=10, fill="x")
    search_edit_frame.columnconfigure(0, weight=1)
    search_edit_frame.columnconfigure(1, weight=3)
    search_edit_frame.columnconfigure(2, weight=1)

    ttk.Label(search_edit_frame, text="Código de Producto a Editar:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    codigo_edit_search_entry = ttk.Entry(search_edit_frame, font=("Arial", 10), width=30)
    codigo_edit_search_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

    # Frame para los campos de edición, inicialmente oculto o vacío
    edit_form_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    edit_form_frame.pack(padx=20, pady=10, fill="both", expand=True)
    edit_form_frame.columnconfigure(0, weight=1)
    edit_form_frame.columnconfigure(1, weight=3)

    # Campos de entrada para la edición (variables asociadas)
    nombre_edit_entry = ttk.Entry(edit_form_frame, font=("Arial", 10), width=30)
    tipo_edit_combobox = ttk.Combobox(edit_form_frame, values=["Carnicos", "Viveres"], state="readonly", font=("Arial", 10), width=28)
    fecha_ingreso_edit_entry = ttk.Entry(edit_form_frame, font=("Arial", 10), width=30)
    fecha_vencimiento_edit_entry = ttk.Entry(edit_form_frame, font=("Arial", 10), width=30)
    precio_edit_entry = ttk.Entry(edit_form_frame, font=("Arial", 10), width=30)
    cantidad_edit_entry = ttk.Entry(edit_form_frame, font=("Arial", 10), width=30)
    id_proveedor_edit_entry = ttk.Entry(edit_form_frame, font=("Arial", 10), width=30)
    
    # Label para el ID de producto que no se edita, pero se muestra
    ttk.Label(edit_form_frame, text="ID de Producto:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    id_producto_display_label = ttk.Label(edit_form_frame, text="", style='ContentLabel.TLabel')
    id_producto_display_label.grid(row=0, column=1, sticky="w", pady=5, padx=5)

    ttk.Label(edit_form_frame, text="Nombre:", style='ContentLabel.TLabel').grid(row=1, column=0, sticky="w", pady=5, padx=5)
    nombre_edit_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(edit_form_frame, text="Tipo:", style='ContentLabel.TLabel').grid(row=2, column=0, sticky="w", pady=5, padx=5)
    tipo_edit_combobox.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(edit_form_frame, text="Fecha Ingreso (YYYY-MM-DD):", style='ContentLabel.TLabel').grid(row=3, column=0, sticky="w", pady=5, padx=5)
    fecha_ingreso_edit_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(edit_form_frame, text="Fecha Vencimiento (YYYY-MM-DD):", style='ContentLabel.TLabel').grid(row=4, column=0, sticky="w", pady=5, padx=5)
    fecha_vencimiento_edit_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(edit_form_frame, text="Precio:", style='ContentLabel.TLabel').grid(row=5, column=0, sticky="w", pady=5, padx=5)
    precio_edit_entry.grid(row=5, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(edit_form_frame, text="Cantidad:", style='ContentLabel.TLabel').grid(row=6, column=0, sticky="w", pady=5, padx=5)
    cantidad_edit_entry.grid(row=6, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(edit_form_frame, text="ID Proveedor:", style='ContentLabel.TLabel').grid(row=7, column=0, sticky="w", pady=5, padx=5)
    id_proveedor_edit_entry.grid(row=7, column=1, sticky="ew", pady=5, padx=5)

    btn_actualizar = ttk.Button(edit_form_frame, text="Actualizar Producto", style='Action.TButton')
    btn_actualizar.grid(row=8, column=0, columnspan=2, pady=15)
    btn_actualizar.grid_remove() # Ocultar inicialmente

    current_product_id = None # Para almacenar el ID del producto que se está editando

    def cargar_datos_producto():
        nonlocal current_product_id
        codigo_producto = codigo_edit_search_entry.get().strip()
        if not codigo_producto:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese el código del producto a editar.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM producto WHERE codigo_producto = %s"
            cursor.execute(sql, (codigo_producto,))
            producto = cursor.fetchone()

            if producto:
                current_product_id = producto['id_producto']
                id_producto_display_label.config(text=producto['id_producto'])
                nombre_edit_entry.delete(0, tk.END)
                nombre_edit_entry.insert(0, producto['nombre'])
                tipo_edit_combobox.set(producto['tipo'])
                fecha_ingreso_edit_entry.delete(0, tk.END)
                fecha_ingreso_edit_entry.insert(0, producto['fecha_ingreso'])
                fecha_vencimiento_edit_entry.delete(0, tk.END)
                fecha_vencimiento_edit_entry.insert(0, producto['fecha_vencimiento'])
                precio_edit_entry.delete(0, tk.END)
                precio_edit_entry.insert(0, producto['precio'])
                cantidad_edit_entry.delete(0, tk.END)
                cantidad_edit_entry.insert(0, producto['cantidad'])
                id_proveedor_edit_entry.delete(0, tk.END)
                id_proveedor_edit_entry.insert(0, producto['id_proveedor'] if producto['id_proveedor'] else "")
                
                btn_actualizar.grid() # Mostrar el botón de actualizar
                edit_form_frame.pack(padx=20, pady=10, fill="both", expand=True) # Asegurarse de que el frame de edición esté visible
                messagebox.showinfo("Producto Encontrado", f"Datos del producto '{producto['nombre']}' cargados para edición.")
            else:
                messagebox.showwarning("No Encontrado", f"No se encontró ningún producto con el código '{codigo_producto}'.")
                # Limpiar y ocultar campos si no se encuentra
                id_producto_display_label.config(text="")
                nombre_edit_entry.delete(0, tk.END)
                tipo_edit_combobox.set("Carnicos")
                fecha_ingreso_edit_entry.delete(0, tk.END)
                fecha_vencimiento_edit_entry.delete(0, tk.END)
                precio_edit_entry.delete(0, tk.END)
                cantidad_edit_entry.delete(0, tk.END)
                id_proveedor_edit_entry.delete(0, tk.END)
                btn_actualizar.grid_remove() # Ocultar el botón de actualizar
                current_product_id = None
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al cargar producto para edición: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    def actualizar_producto():
        if current_product_id is None:
            messagebox.showwarning("Advertencia", "No hay producto cargado para actualizar.")
            return

        nombre = nombre_edit_entry.get().strip()
        tipo = tipo_edit_combobox.get().strip()
        fecha_ingreso_str = fecha_ingreso_edit_entry.get().strip()
        fecha_vencimiento_str = fecha_vencimiento_edit_entry.get().strip()
        precio_str = precio_edit_entry.get().strip()
        cantidad_str = cantidad_edit_entry.get().strip()
        id_proveedor_str = id_proveedor_edit_entry.get().strip()

        # Validación de campos obligatorios
        missing_fields = []
        if not nombre:
            missing_fields.append("Nombre")
        if not tipo:
            missing_fields.append("Tipo")
        if not fecha_ingreso_str:
            missing_fields.append("Fecha de Ingreso")
        if not fecha_vencimiento_str:
            missing_fields.append("Fecha de Vencimiento")
        if not precio_str:
            missing_fields.append("Precio")
        if not cantidad_str:
            missing_fields.append("Cantidad")
        if not id_proveedor_str:
            missing_fields.append("ID Proveedor")

        if missing_fields:
            messagebox.showwarning("Campos Incompletos", 
                                   "Los siguientes campos son obligatorios y no pueden estar vacíos:\n\n- " + 
                                   "\n- ".join(missing_fields))
            return


        try:
            fecha_ingreso = datetime.strptime(fecha_ingreso_str, "%Y-%m-%d").date()
            fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d").date()
            precio = float(precio_str)
            cantidad = int(cantidad_str)
            id_proveedor = int(id_proveedor_str)

            if precio <= 0:
                messagebox.showerror("Error de Valores", "El precio debe ser un número positivo mayor que cero.")
                return
            if cantidad < 0:
                messagebox.showerror("Error de Valores", "La cantidad no puede ser un número negativo.")
                return
            if fecha_vencimiento < fecha_ingreso:
                messagebox.showerror("Error de Fechas", "La fecha de vencimiento no puede ser anterior a la fecha de ingreso.")
                return

        except ValueError as e:
            messagebox.showerror("Error de Formato", f"Verifique el formato de los datos:\n\n- Fechas: YYYY-MM-DD\n- Precio: Numérico (ej. 10.50)\n- Cantidad: Número entero\n- ID Proveedor: Número entero\n\nDetalle del error: {e}")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            sql = """
                UPDATE producto 
                SET nombre = %s, tipo = %s, fecha_ingreso = %s, fecha_vencimiento = %s, 
                    precio = %s, cantidad = %s, id_proveedor = %s
                WHERE id_producto = %s
            """
            val = (nombre, tipo, fecha_ingreso, fecha_vencimiento, precio, cantidad, id_proveedor, current_product_id)
            cursor.execute(sql, val)
            db.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            else:
                messagebox.showwarning("Advertencia", "No se realizó ninguna actualización (los datos eran los mismos o el producto no existe).")
        except mysql.connector.Error as err:
            if err.errno == 1452: # Código de error para FK constraint fail (Proveedor no existe)
                 messagebox.showerror("Error de Actualización", "El ID de Proveedor no existe o es inválido. Por favor, asegúrese de que el proveedor exista.")
            else:
                messagebox.showerror("Error de Base de Datos", f"Error al actualizar producto: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()
        
        # Después de actualizar, puedes recargar los datos o limpiar el formulario
        codigo_edit_search_entry.delete(0, tk.END)
        id_producto_display_label.config(text="")
        nombre_edit_entry.delete(0, tk.END)
        tipo_edit_combobox.set("Carnicos")
        fecha_ingreso_edit_entry.delete(0, tk.END)
        fecha_vencimiento_edit_entry.delete(0, tk.END)
        precio_edit_entry.delete(0, tk.END)
        cantidad_edit_entry.delete(0, tk.END)
        id_proveedor_edit_entry.delete(0, tk.END)
        btn_actualizar.grid_remove()
        current_product_id = None


    ttk.Button(search_edit_frame, text="Cargar Producto", command=cargar_datos_producto, style='Search.TButton').grid(row=0, column=2, sticky="ew", pady=5, padx=5)
    btn_actualizar.config(command=actualizar_producto) # Asignar la función al botón


def eliminar_producto_internal(parent_frame):
    clear_frame(parent_frame)
    style = ttk.Style(parent_frame)
    style.configure('Delete.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#f44336", foreground='white', borderwidth=0, relief="flat") 
    style.map('Delete.TButton', background=[('active', "#DA190B")])
    style.configure('Search.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#2196F3", foreground='white', borderwidth=0, relief="flat") 
    style.map('Search.TButton', background=[('active', "#0B7CDA")])


    ttk.Label(parent_frame, text="Eliminar Producto", style='ContentTitle.TLabel').pack(pady=20)

    delete_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    delete_frame.pack(padx=20, pady=10, fill="x")
    delete_frame.columnconfigure(0, weight=1)
    delete_frame.columnconfigure(1, weight=3)
    delete_frame.columnconfigure(2, weight=1)

    ttk.Label(delete_frame, text="Código de Producto a Eliminar:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    codigo_delete_entry = ttk.Entry(delete_frame, font=("Arial", 10), width=30)
    codigo_delete_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

    def eliminar_producto():
        codigo_producto = codigo_delete_entry.get().strip()
        if not codigo_producto:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese el código del producto a eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", 
                                      f"¿Está seguro de que desea eliminar el producto con código '{codigo_producto}'?\nEsta acción es irreversible.")
        if not confirm:
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            sql = "DELETE FROM producto WHERE codigo_producto = %s"
            cursor.execute(sql, (codigo_producto,))
            db.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Producto con código '{codigo_producto}' eliminado correctamente.")
                codigo_delete_entry.delete(0, tk.END) # Limpiar el campo
            else:
                messagebox.showwarning("No Encontrado", f"No se encontró ningún producto con el código '{codigo_producto}'.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al eliminar producto: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    ttk.Button(delete_frame, text="Eliminar Producto", command=eliminar_producto, style='Delete.TButton').grid(row=0, column=2, sticky="ew", pady=5, padx=5)


    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Consultar Inventario General", style='ContentTitle.TLabel').pack(pady=20)
    
    # Crear un Frame para contener el Treeview y el botón de refrescar
    inventory_container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    inventory_container.pack(fill="both", expand=True, padx=10, pady=10)

    # Crear el Treeview para mostrar los datos
    tree = ttk.Treeview(inventory_container, columns=("ID", "Código", "Nombre", "Tipo", "Ingreso", "Vencimiento", "Precio", "Cantidad", "Proveedor ID"), show="headings")

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
    vsb = ttk.Scrollbar(inventory_container, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    hsb = ttk.Scrollbar(parent_frame, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x', padx=10) # Adjuntado al parent_frame para que esté debajo del Treeview
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
                # Si no hay productos, informar al usuario directamente en el Treeview o con un mensaje
                # Se puede añadir una etiqueta aquí, o dejar el Treeview vacío.
                pass # El Treeview simplemente aparecerá vacío si no hay datos.

        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al consultar el inventario: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()
    
    cargar_productos() # Cargar los productos al construir la UI

    # Botón para refrescar la lista
    ttk.Button(parent_frame, text="Refrescar Lista", command=cargar_productos, style='Action.TButton').pack(pady=10)