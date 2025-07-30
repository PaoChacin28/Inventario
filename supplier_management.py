import tkinter as tk
from tkinter import messagebox
from tkinter import ttk # Para el Treeview en consultar_proveedor
import mysql.connector
from db_connection import conectar_db

# --- Funciones de Utilidad (para estilizar ventanas) ---
def setup_window(window, title, geometry="500x400"):
    window.title(title)
    window.geometry(geometry)
    window.configure(bg="#e0f8f7") # Fondo claro para las ventanas de gestión
    return window

def create_input_field(parent, label_text, entry_width=40, show_char=None):
    frame = tk.Frame(parent, bg="#e0f8f7")
    frame.pack(pady=3, fill="x", padx=10)
    tk.Label(frame, text=label_text, bg="#e0f8f7", font=("Arial", 10)).pack(side="left", padx=5)
    entry = tk.Entry(frame, width=entry_width, font=("Arial", 10), show=show_char)
    entry.pack(side="right", expand=True, fill="x", padx=5)
    return entry

# --- Funciones de Gestión de Proveedores ---

def registrar_proveedor():
    win = setup_window(tk.Toplevel(), "Registrar Nuevo Proveedor", "450x350")

    tk.Label(win, text="Datos del Nuevo Proveedor", font=("Arial", 14, "bold"), bg="#e0f8f7").pack(pady=15)

    e_nombre = create_input_field(win, "Nombre:")
    e_rif = create_input_field(win, "RIF:")
    e_telefono = create_input_field(win, "Teléfono:")
    e_direccion = create_input_field(win, "Dirección:")

    def guardar_proveedor():
        nombre = e_nombre.get()
        rif = e_rif.get()
        telefono = e_telefono.get()
        direccion = e_direccion.get()

        if not nombre or not rif:
            messagebox.showwarning("Campos Requeridos", "El nombre y el RIF son obligatorios.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            sql = "INSERT INTO proveedor (nombre, rif, telefono, direccion) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre, rif, telefono, direccion))
            db.commit()
            messagebox.showinfo("Éxito", "Proveedor registrado correctamente.")
            win.destroy()
        except mysql.connector.Error as err:
            if err.errno == 1062: # Duplicate entry for UNIQUE key (RIF)
                messagebox.showerror("Error de RIF", "El RIF ingresado ya existe para otro proveedor.")
            else:
                messagebox.showerror("Error de Base de Datos", f"Error al registrar proveedor: {err}")
            if db.is_connected():
                db.rollback()
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    tk.Button(win, text="Guardar Proveedor", command=guardar_proveedor,
              font=("Arial", 10, "bold"), bg="#28a745", fg="white", width=20, cursor="hand2").pack(pady=20)
    win.mainloop()

def consultar_proveedor():
    win = setup_window(tk.Toplevel(), "Consultar Proveedores", "700x500")

    tk.Label(win, text="Buscar Proveedor", font=("Arial", 14, "bold"), bg="#e0f8f7").pack(pady=15)

    e_busqueda = create_input_field(win, "Nombre o RIF:")
    
    # Configuración del Treeview para mostrar resultados
    tree_frame = tk.Frame(win, bg="#e0f8f7")
    tree_frame.pack(pady=10, fill="both", expand=True, padx=10)

    columns = ("ID", "Nombre", "RIF", "Teléfono", "Dirección")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

    for col in columns:
        tree.heading(col, text=col, anchor="w")
        tree.column(col, width=100, anchor="w")

    tree.column("ID", width=50) # Hacer la columna ID más pequeña

    # Scrollbar para el Treeview
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x')
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.pack(fill="both", expand=True)

    def buscar_proveedor_db():
        for item in tree.get_children():
            tree.delete(item) # Limpiar resultados anteriores

        busqueda = f"%{e_busqueda.get()}%" # Para búsqueda parcial

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True) # Para obtener resultados como diccionarios
        try:
            sql = "SELECT id_proveedor, nombre, rif, telefono, direccion FROM proveedor WHERE nombre LIKE %s OR rif LIKE %s"
            cursor.execute(sql, (busqueda, busqueda))
            resultados = cursor.fetchall()

            if not resultados:
                messagebox.showinfo("Sin Resultados", "No se encontraron proveedores con ese criterio de búsqueda.")
                return

            for row in resultados:
                tree.insert("", "end", values=(row['id_proveedor'], row['nombre'], row['rif'], row['telefono'], row['direccion']))

        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al buscar proveedor: {err}")
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    tk.Button(win, text="Buscar", command=buscar_proveedor_db,
              font=("Arial", 10, "bold"), bg="#007bff", fg="white", width=15, cursor="hand2").pack(pady=10)
    win.mainloop()


def editar_proveedor():
    win = setup_window(tk.Toplevel(), "Editar Proveedor", "450x450")

    tk.Label(win, text="Editar Datos del Proveedor", font=("Arial", 14, "bold"), bg="#e0f8f7").pack(pady=15)

    e_id_rif_buscar = create_input_field(win, "ID o RIF del Proveedor a Editar:")
    
    # Campos para mostrar y editar los datos
    e_nombre = create_input_field(win, "Nuevo Nombre:")
    e_rif = create_input_field(win, "Nuevo RIF:")
    e_telefono = create_input_field(win, "Nuevo Teléfono:")
    e_direccion = create_input_field(win, "Nueva Dirección:")

    current_supplier_id = None # Para guardar el ID del proveedor que se está editando

    def cargar_proveedor():
        nonlocal current_supplier_id
        busqueda = e_id_rif_buscar.get()
        if not busqueda:
            messagebox.showwarning("Entrada Vacía", "Por favor, ingresa el ID o RIF del proveedor a buscar.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True)
        try:
            if busqueda.isdigit(): # Si es un número, buscar por ID
                sql = "SELECT id_proveedor, nombre, rif, telefono, direccion FROM proveedor WHERE id_proveedor = %s"
                cursor.execute(sql, (busqueda,))
            else: # Si no es un número, buscar por RIF
                sql = "SELECT id_proveedor, nombre, rif, telefono, direccion FROM proveedor WHERE rif = %s"
                cursor.execute(sql, (busqueda,))
            
            proveedor = cursor.fetchone()

            if proveedor:
                current_supplier_id = proveedor['id_proveedor']
                e_nombre.delete(0, tk.END)
                e_nombre.insert(0, proveedor['nombre'])
                e_rif.delete(0, tk.END)
                e_rif.insert(0, proveedor['rif'])
                e_telefono.delete(0, tk.END)
                e_telefono.insert(0, proveedor['telefono'])
                e_direccion.delete(0, tk.END)
                e_direccion.insert(0, proveedor['direccion'])
                messagebox.showinfo("Proveedor Encontrado", f"Proveedor '{proveedor['nombre']}' cargado.")
            else:
                current_supplier_id = None
                messagebox.showerror("No Encontrado", "No se encontró un proveedor con ese ID o RIF.")
                # Limpiar campos si no se encuentra
                e_nombre.delete(0, tk.END)
                e_rif.delete(0, tk.END)
                e_telefono.delete(0, tk.END)
                e_direccion.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al cargar proveedor: {err}")
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    tk.Button(win, text="Cargar Proveedor", command=cargar_proveedor,
              font=("Arial", 10, "bold"), bg="#007bff", fg="white", width=20, cursor="hand2").pack(pady=10)

    def guardar_cambios():
        if current_supplier_id is None:
            messagebox.showwarning("Advertencia", "Primero carga un proveedor para editar.")
            return

        nombre = e_nombre.get()
        rif = e_rif.get()
        telefono = e_telefono.get()
        direccion = e_direccion.get()

        if not nombre or not rif:
            messagebox.showwarning("Campos Requeridos", "El nombre y el RIF no pueden estar vacíos.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            sql = "UPDATE proveedor SET nombre=%s, rif=%s, telefono=%s, direccion=%s WHERE id_proveedor=%s"
            cursor.execute(sql, (nombre, rif, telefono, direccion, current_supplier_id))
            db.commit()
            messagebox.showinfo("Éxito", "Proveedor actualizado correctamente.")
            win.destroy()
        except mysql.connector.Error as err:
            if err.errno == 1062: # Duplicate entry for UNIQUE key (RIF)
                messagebox.showerror("Error de RIF", "El nuevo RIF ingresado ya existe para otro proveedor.")
            else:
                messagebox.showerror("Error de Base de Datos", f"Error al actualizar proveedor: {err}")
            if db.is_connected():
                db.rollback()
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    tk.Button(win, text="Guardar Cambios", command=guardar_cambios,
              font=("Arial", 10, "bold"), bg="#28a745", fg="white", width=20, cursor="hand2").pack(pady=15)
    win.mainloop()


def eliminar_proveedor():
    win = setup_window(tk.Toplevel(), "Eliminar Proveedor", "400x250")

    tk.Label(win, text="Eliminar Proveedor", font=("Arial", 14, "bold"), bg="#e0f8f7").pack(pady=15)

    e_id_rif_eliminar = create_input_field(win, "ID o RIF del Proveedor a Eliminar:")

    def confirmar_eliminar():
        busqueda = e_id_rif_eliminar.get()
        if not busqueda:
            messagebox.showwarning("Entrada Vacía", "Por favor, ingresa el ID o RIF del proveedor a eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", 
                                      f"¿Estás seguro de que quieres eliminar el proveedor con ID/RIF '{busqueda}'? "
                                      "Esta acción es irreversible.")
        if not confirm:
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            # Primero, buscar el ID real para asegurar que eliminamos el correcto
            if busqueda.isdigit():
                sql_select = "SELECT id_proveedor FROM proveedor WHERE id_proveedor = %s"
            else:
                sql_select = "SELECT id_proveedor FROM proveedor WHERE rif = %s"
            cursor.execute(sql_select, (busqueda,))
            proveedor_id = cursor.fetchone()

            if proveedor_id:
                # Si el proveedor existe, intentar eliminarlo
                sql_delete = "DELETE FROM proveedor WHERE id_proveedor = %s"
                cursor.execute(sql_delete, (proveedor_id[0],))
                db.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
                    win.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el proveedor. No encontrado o error interno.")
            else:
                messagebox.showerror("No Encontrado", "No se encontró un proveedor con ese ID o RIF.")

        except mysql.connector.Error as err:
            if err.errno == 1451: # Foreign key constraint fails
                 messagebox.showerror("Error de Integridad", "No se puede eliminar el proveedor porque tiene productos asociados. Elimina los productos primero o actualiza su proveedor.")
            else:
                messagebox.showerror("Error de Base de Datos", f"Error al eliminar proveedor: {err}")
            if db.is_connected():
                db.rollback()
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    tk.Button(win, text="Eliminar Proveedor", command=confirmar_eliminar,
              font=("Arial", 10, "bold"), bg="#dc3545", fg="white", width=20, cursor="hand2").pack(pady=20)
    win.mainloop()