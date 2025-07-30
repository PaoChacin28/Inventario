# product_management.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from db_connection import conectar_db # Importamos la función de conexión
import mysql.connector

def registrar_producto():
    win = ttk.Toplevel()
    win.title("Registrar Producto")
    win.geometry("450x600")
    # No usamos transient con ventana_login directamente aquí, sino que la abrimos desde main.py

    win.configure(bg="#f0f8ff")
    label_font = ("Arial", 10)
    entry_font = ("Arial", 10)
    button_font = ("Arial", 10, "bold")

    ttk.Label(win, text="Código de Producto:", font=label_font, bg="#f0f8ff").pack(pady=5)
    entry_codigo = ttk.Entry(win, font=entry_font, width=30)
    entry_codigo.pack(pady=2)

    ttk.Label(win, text="Nombre:", font=label_font, bg="#f0f8ff").pack(pady=5)
    entry_nombre = ttk.Entry(win, font=entry_font, width=30)
    entry_nombre.pack(pady=2)

    ttk.Label(win, text="Tipo (Cárnicos/Víveres):", font=label_font, bg="#f0f8ff").pack(pady=5)
    tipo_options = ["Carnicos", "Viveres"]
    combo_tipo = ttk.Combobox(win, values=tipo_options, state="readonly", font=entry_font, width=28)
    combo_tipo.set("Seleccionar")
    combo_tipo.pack(pady=2)

    ttk.Label(win, text="Fecha de Ingreso (YYYY-MM-DD):", font=label_font, bg="#f0f8ff").pack(pady=5)
    entry_fecha_ingreso = ttk.Entry(win, font=entry_font, width=30)
    entry_fecha_ingreso.insert(0, datetime.now().strftime("%Y-%m-%d"))
    entry_fecha_ingreso.pack(pady=2)

    ttk.Label(win, text="Fecha de Vencimiento (YYYY-MM-DD):", font=label_font, bg="#f0f8ff").pack(pady=5)
    entry_fecha_vencimiento = ttk.Entry(win, font=entry_font, width=30)
    entry_fecha_vencimiento.pack(pady=2)

    ttk.Label(win, text="Precio:", font=label_font, bg="#f0f8ff").pack(pady=5)
    entry_precio = ttk.Entry(win, font=entry_font, width=30)
    entry_precio.pack(pady=2)

    ttk.Label(win, text="Cantidad:", font=label_font, bg="#f0f8ff").pack(pady=5)
    entry_cantidad = ttk.Entry(win, font=entry_font, width=30)
    entry_cantidad.pack(pady=2)

    ttk.Label(win, text="ID Proveedor:", font=label_font, bg="#f0f8ff").pack(pady=5)
    entry_id_proveedor = ttk.Entry(win, font=entry_font, width=30)
    entry_id_proveedor.pack(pady=2)

    def guardar_producto():
        codigo_producto = entry_codigo.get()
        nombre = entry_nombre.get()
        tipo = combo_tipo.get()
        fecha_ingreso_str = entry_fecha_ingreso.get()
        fecha_vencimiento_str = entry_fecha_vencimiento.get()
        precio_str = entry_precio.get()
        cantidad_str = entry_cantidad.get()
        id_proveedor_str = entry_id_proveedor.get()

        if not all([codigo_producto, nombre, tipo, fecha_ingreso_str, fecha_vencimiento_str, precio_str, cantidad_str, id_proveedor_str]):
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
            return

        if tipo == "Seleccionar":
            messagebox.showwarning("Tipo de Producto", "Por favor, seleccione un tipo de producto.")
            return

        try:
            fecha_ingreso = datetime.strptime(fecha_ingreso_str, "%Y-%m-%d").date()
            fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d").date()
            precio = float(precio_str)
            cantidad = int(cantidad_str)
            id_proveedor = int(id_proveedor_str)
        except ValueError:
            messagebox.showerror("Error de Formato", "Verifique que las fechas estén en formato YYYY-MM-DD, y que precio/cantidad/ID Proveedor sean números válidos.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            cursor.execute("SELECT id_proveedor FROM proveedor WHERE id_proveedor = %s", (id_proveedor,))
            if cursor.fetchone() is None:
                messagebox.showerror("Error de Proveedor", "El ID de Proveedor ingresado no existe.")
                return

            sql = """
            INSERT INTO producto (codigo_producto, nombre, tipo, fecha_ingreso, fecha_vencimiento, precio, cantidad, id_proveedor)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (codigo_producto, nombre, tipo, fecha_ingreso, fecha_vencimiento, precio, cantidad, id_proveedor))
            db.commit()
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")
            win.destroy()
        except mysql.connector.IntegrityError as err:
            if "Duplicate entry" in str(err) and "for key 'producto.codigo_producto'" in str(err):
                messagebox.showerror("Error de Registro", "Ya existe un producto con este código de producto.")
            else:
                messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al registrar el producto: {err}")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al registrar el producto: {err}")
        finally:
            if 'db' in locals() and db.is_connected():
                cursor.close()
                db.close()

    tk.Button(win, text="Guardar Producto", command=guardar_producto,
              font=button_font, bg="#28a745", fg="white", width=20, cursor="hand2").pack(pady=15)
    win.mainloop()

def consultar_producto():
    """Abre una ventana para consultar un producto específico por ID o código."""
    win = tk.Toplevel()
    win.title("Consultar Producto Específico")
    win.geometry("600x400")
    win.configure(bg="#f0f8ff")

    tk.Label(win, text="Buscar Producto (ID o Código):", bg="#f0f8ff").pack(pady=10)
    search_entry = tk.Entry(win, width=40)
    search_entry.pack(pady=5)

    tree = ttk.Treeview(win, columns=("ID", "Código", "Nombre", "Tipo", "Ingreso", "Vencimiento", "Precio", "Cantidad", "Proveedor ID"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Código", text="Código")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Tipo", text="Tipo")
    tree.heading("Ingreso", text="F. Ingreso")
    tree.heading("Vencimiento", text="F. Venc.")
    tree.heading("Precio", text="Precio")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Proveedor ID", text="ID Prov.")

    tree.column("ID", width=50)
    tree.column("Código", width=90)
    tree.column("Nombre", width=120)
    tree.column("Tipo", width=80)
    tree.column("Ingreso", width=90)
    tree.column("Vencimiento", width=90)
    tree.column("Precio", width=70)
    tree.column("Cantidad", width=70)
    tree.column("Proveedor ID", width=70)
    
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def perform_search():
        for item in tree.get_children():
            tree.delete(item) # Limpiar resultados anteriores

        search_term = search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un ID o código de producto para buscar.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True)
        try:
            # Intentar buscar por id_producto (numérico)
            try:
                product_id = int(search_term)
                sql = "SELECT * FROM producto WHERE id_producto = %s"
                cursor.execute(sql, (product_id,))
            except ValueError:
                # Si no es un número, intentar buscar por codigo_producto (VARCHAR)
                sql = "SELECT * FROM producto WHERE codigo_producto = %s"
                cursor.execute(sql, (search_term,))
            
            producto = cursor.fetchone()

            if producto:
                tree.insert("", tk.END, values=(
                    producto['id_producto'],
                    producto['codigo_producto'],
                    producto['nombre'],
                    producto['tipo'],
                    producto['fecha_ingreso'],
                    producto['fecha_vencimiento'],
                    producto['precio'],
                    producto['cantidad'],
                    producto['id_proveedor']
                ))
            else:
                messagebox.showinfo("No Encontrado", f"No se encontró ningún producto con ID o Código: {search_term}")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al consultar el producto: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    tk.Button(win, text="Buscar", command=perform_search).pack(pady=10)
    win.mainloop()

def eliminar_producto():
    """Abre una ventana para eliminar un producto por ID o código."""
    win = tk.Toplevel()
    win.title("Eliminar Producto")
    win.geometry("400x200")
    win.configure(bg="#f0f8ff")

    tk.Label(win, text="Ingrese ID o Código del Producto a Eliminar:", bg="#f0f8ff").pack(pady=15)
    entry_eliminar = tk.Entry(win, width=30)
    entry_eliminar.pack(pady=5)

    def confirmar_eliminar():
        search_term = entry_eliminar.get().strip()
        if not search_term:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un ID o código de producto.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar el producto con ID/Código: {search_term}?\nEsta acción es irreversible.")
        
        if confirm:
            db = conectar_db()
            if db is None:
                return

            cursor = db.cursor()
            try:
                rows_affected = 0
                # Intentar eliminar por id_producto (numérico)
                try:
                    product_id = int(search_term)
                    sql = "DELETE FROM producto WHERE id_producto = %s"
                    cursor.execute(sql, (product_id,))
                    rows_affected = cursor.rowcount
                except ValueError:
                    # Si no es un número, intentar eliminar por codigo_producto (VARCHAR)
                    sql = "DELETE FROM producto WHERE codigo_producto = %s"
                    cursor.execute(sql, (search_term,))
                    rows_affected = cursor.rowcount

                if rows_affected > 0:
                    db.commit()
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                    win.destroy()
                else:
                    messagebox.showerror("Error de Eliminación", f"No se encontró ningún producto con ID o Código: {search_term} para eliminar.")
            except mysql.connector.Error as err:
                # Capturar error de clave foránea si el producto está en movimientos
                if err.errno == 1451: # Foreign key constraint fails
                    messagebox.showerror("Error de Base de Datos", "No se puede eliminar el producto porque está asociado a movimientos existentes. Elimine los movimientos primero.")
                else:
                    messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al eliminar el producto: {err}")
            finally:
                if db and db.is_connected():
                    cursor.close()
                    db.close()

    tk.Button(win, text="Eliminar Producto", command=confirmar_eliminar,
              bg="#dc3545", fg="white", font=("Arial", 10, "bold"), width=20).pack(pady=15)
    win.mainloop()


def editar_producto():
    """Abre una ventana para buscar un producto y luego editar sus detalles."""
    win = tk.Toplevel()
    win.title("Editar Producto")
    win.geometry("500x300")
    win.configure(bg="#f0f8ff")

    tk.Label(win, text="Ingrese ID o Código del Producto a Editar:", bg="#f0f8ff").pack(pady=15)
    search_entry = tk.Entry(win, width=30)
    search_entry.pack(pady=5)

    product_data = {} # Usaremos este diccionario para guardar los datos del producto a editar

    def cargar_datos_producto():
        search_term = search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un ID o código de producto.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True)
        try:
            try:
                product_id = int(search_term)
                sql = "SELECT * FROM producto WHERE id_producto = %s"
                cursor.execute(sql, (product_id,))
            except ValueError:
                sql = "SELECT * FROM producto WHERE codigo_producto = %s"
                cursor.execute(sql, (search_term,))
            
            producto = cursor.fetchone()

            if producto:
                product_data.clear() # Limpiar datos anteriores
                product_data.update(producto) # Guardar los datos del producto encontrado

                # Cerrar la ventana de búsqueda
                win.destroy() 
                # Abrir la ventana de edición
                abrir_ventana_edicion(product_data)

            else:
                messagebox.showinfo("No Encontrado", f"No se encontró ningún producto con ID o Código: {search_term}")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al buscar el producto: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    tk.Button(win, text="Buscar Producto", command=cargar_datos_producto,
              font=("Arial", 10, "bold"), width=20).pack(pady=15)
    win.mainloop()

def abrir_ventana_edicion(producto_actual):
    """Abre la ventana para editar los detalles del producto."""
    edit_win = tk.Toplevel()
    edit_win.title(f"Editar Producto: {producto_actual['nombre']}")
    edit_win.geometry("450x650")
    edit_win.configure(bg="#f0f8ff")

    label_font = ("Arial", 10)
    entry_font = ("Arial", 10)
    button_font = ("Arial", 10, "bold")

    # Mostrar ID del producto (no editable)
    tk.Label(edit_win, text=f"ID Producto: {producto_actual['id_producto']}", font=("Arial", 12, "bold"), bg="#f0f8ff").pack(pady=5)

    tk.Label(edit_win, text="Código de Producto:", font=label_font, bg="#f0f8ff").pack(pady=5)
    entry_codigo = tk.Entry(edit_win, font=entry_font, width=30)
    entry_codigo.insert(0, producto_actual['codigo_producto'])
    entry_codigo.pack(pady=2)

    tk.Label(edit_win, text="Nombre:", font=label_font, bg="#f0f8ff").pack(pady=5)
    entry_nombre = tk.Entry(edit_win, font=entry_font, width=30)
    entry_nombre.insert(0, producto_actual['nombre'])
    entry_nombre.pack(pady=2)

    tk.Label(edit_win, text="Tipo (Cárnicos/Víveres):", font=label_font, bg="#f0f8ff").pack(pady=5)
    tipo_options = ["Carnicos", "Viveres"]
    combo_tipo = ttk.Combobox(edit_win, values=tipo_options, state="readonly", font=entry_font, width=28)
    combo_tipo.set(producto_actual['tipo'])
    combo_tipo.pack(pady=2)

    tk.Label(edit_win, text="Fecha de Ingreso (YYYY-MM-DD):", font=label_font, bg="#f0f8ff").pack(pady=5)
    entry_fecha_ingreso = tk.Entry(edit_win, font=entry_font, width=30)
    entry_fecha_ingreso.insert(0, str(producto_actual['fecha_ingreso']))
    entry_fecha_ingreso.pack(pady=2)

    tk.Label(edit_win, text="Fecha de Vencimiento (YYYY-MM-DD):", font=label_font, bg="#f0f8ff").pack(pady=5)
    entry_fecha_vencimiento = tk.Entry(edit_win, font=entry_font, width=30)
    entry_fecha_vencimiento.insert(0, str(producto_actual['fecha_vencimiento']))
    entry_fecha_vencimiento.pack(pady=2)

    tk.Label(edit_win, text="Precio:", font=label_font, bg="#f0f8ff").pack(pady=5)
    entry_precio = tk.Entry(edit_win, font=entry_font, width=30)
    entry_precio.insert(0, str(producto_actual['precio']))
    entry_precio.pack(pady=2)

    tk.Label(edit_win, text="Cantidad:", font=label_font, bg="#f0f8ff").pack(pady=5)
    entry_cantidad = tk.Entry(edit_win, font=entry_font, width=30)
    entry_cantidad.insert(0, str(producto_actual['cantidad']))
    entry_cantidad.pack(pady=2)

    tk.Label(edit_win, text="ID Proveedor:", font=label_font, bg="#f0f8ff").pack(pady=5)
    entry_id_proveedor = tk.Entry(edit_win, font=entry_font, width=30)
    entry_id_proveedor.insert(0, str(producto_actual['id_proveedor']))
    entry_id_proveedor.pack(pady=2)

    def guardar_cambios():
        nuevo_codigo = entry_codigo.get()
        nuevo_nombre = entry_nombre.get()
        nuevo_tipo = combo_tipo.get()
        nueva_fecha_ingreso_str = entry_fecha_ingreso.get()
        nueva_fecha_vencimiento_str = entry_fecha_vencimiento.get()
        nuevo_precio_str = entry_precio.get()
        nueva_cantidad_str = entry_cantidad.get()
        nuevo_id_proveedor_str = entry_id_proveedor.get()

        if not all([nuevo_codigo, nuevo_nombre, nuevo_tipo, nueva_fecha_ingreso_str, nueva_fecha_vencimiento_str, nuevo_precio_str, nueva_cantidad_str, nuevo_id_proveedor_str]):
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
            return

        if nuevo_tipo == "Seleccionar":
            messagebox.showwarning("Tipo de Producto", "Por favor, seleccione un tipo de producto válido.")
            return

        try:
            nueva_fecha_ingreso = datetime.strptime(nueva_fecha_ingreso_str, "%Y-%m-%d").date()
            nueva_fecha_vencimiento = datetime.strptime(nueva_fecha_vencimiento_str, "%Y-%m-%d").date()
            nuevo_precio = float(nuevo_precio_str)
            nueva_cantidad = int(nueva_cantidad_str)
            nuevo_id_proveedor = int(nuevo_id_proveedor_str)
        except ValueError:
            messagebox.showerror("Error de Formato", "Verifique que las fechas estén en formato YYYY-MM-DD, y que precio/cantidad/ID Proveedor sean números válidos.")
            return
        
        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            # Verificar si el nuevo proveedor existe
            cursor.execute("SELECT id_proveedor FROM proveedor WHERE id_proveedor = %s", (nuevo_id_proveedor,))
            if cursor.fetchone() is None:
                messagebox.showerror("Error de Proveedor", "El ID de Proveedor ingresado no existe.")
                return

            # Verificar si el nuevo codigo_producto ya existe para otro producto (si se cambió el código)
            if nuevo_codigo != producto_actual['codigo_producto']:
                cursor.execute("SELECT id_producto FROM producto WHERE codigo_producto = %s", (nuevo_codigo,))
                if cursor.fetchone():
                    messagebox.showerror("Código Duplicado", "El nuevo código de producto ya existe para otro producto.")
                    return

            sql = """
            UPDATE producto SET 
                codigo_producto = %s, 
                nombre = %s, 
                tipo = %s, 
                fecha_ingreso = %s, 
                fecha_vencimiento = %s, 
                precio = %s, 
                cantidad = %s, 
                id_proveedor = %s 
            WHERE id_producto = %s
            """
            cursor.execute(sql, (
                nuevo_codigo, nuevo_nombre, nuevo_tipo, 
                nueva_fecha_ingreso, nueva_fecha_vencimiento, 
                nuevo_precio, nueva_cantidad, nuevo_id_proveedor, 
                producto_actual['id_producto']
            ))
            db.commit()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            edit_win.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al actualizar el producto: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    tk.Button(edit_win, text="Guardar Cambios", command=guardar_cambios,
              font=button_font, bg="#007bff", fg="white", width=20, cursor="hand2").pack(pady=15)
    edit_win.mainloop()

# Placeholder para la función de consultar inventario general, si se desea una ventana específica
def consultar_inventario_general():
    """Abre una ventana que muestra todos los productos en el inventario."""
    win = tk.Toplevel()
    win.title("Inventario General de Productos")
    win.geometry("900x500") # Ajusta el tamaño para mostrar más columnas
    win.configure(bg="#f0f8ff")

    tk.Label(win, text="Listado Completo de Productos", font=("Arial", 14, "bold"), bg="#f0f8ff").pack(pady=10)

    # Crear el Treeview para mostrar los datos
    tree = ttk.Treeview(win, columns=("ID", "Código", "Nombre", "Tipo", "Ingreso", "Vencimiento", "Precio", "Cantidad", "Proveedor ID"), show="headings")

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

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Añadir Scrollbars
    vsb = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    hsb = ttk.Scrollbar(tree, orient="horizontal", command=tree.xview)
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
    
    cargar_productos() # Cargar los productos al abrir la ventana
    
    # Botón para refrescar la lista
    tk.Button(win, text="Refrescar Lista", command=cargar_productos).pack(pady=10)

    win.mainloop()