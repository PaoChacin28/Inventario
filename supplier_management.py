# provider_management.py
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Asume que db_connection.py está en la misma carpeta
from db_connection import conectar_db 

# Función auxiliar para limpiar el frame (replicada aquí para auto-contención)
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# --- Funciones de Gestión de Proveedores ---

def registrar_proveedor_internal(parent_frame):
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
    ttk.Label(parent_frame, text="Registrar Nuevo Proveedor", style='ContentTitle.TLabel').pack(pady=20)

    # Frame para los campos de entrada para mejor organización
    input_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    input_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Usar grid para los campos del formulario para un mejor control del layout
    input_frame.columnconfigure(0, weight=1)
    input_frame.columnconfigure(1, weight=3) # Dar más espacio a las entradas

    # Campo: Nombre
    ttk.Label(input_frame, text="Nombre:",
              style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    nombre_entry = ttk.Entry(input_frame, font=("Arial", 10), width=30)
    nombre_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

    # Campo: RIF (Registro de Información Fiscal)
    ttk.Label(input_frame, text="RIF:", 
              style='ContentLabel.TLabel').grid(row=1, column=0, sticky="w", pady=5, padx=5)
    rif_entry = ttk.Entry(input_frame, font=("Arial", 10), width=30)
    rif_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

    # Campo: Teléfono (Opcional)
    ttk.Label(input_frame, text="Teléfono:", 
              style='ContentLabel.TLabel').grid(row=2, column=0, sticky="w", pady=5, padx=5)
    telefono_entry = ttk.Entry(input_frame, font=("Arial", 10), width=30)
    telefono_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

    # Campo: Dirección (Opcional)
    ttk.Label(input_frame, text="Dirección:", 
              style='ContentLabel.TLabel').grid(row=3, column=0, sticky="w", pady=5, padx=5)
    direccion_entry = ttk.Entry(input_frame, font=("Arial", 10), width=30)
    direccion_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=5)

    def guardar_proveedor():
        nombre = nombre_entry.get().strip()
        rif = rif_entry.get().strip()
        telefono = telefono_entry.get().strip() # Es opcional
        direccion = direccion_entry.get().strip() # Es opcional

        missing_fields = []
        if not nombre:
            missing_fields.append("Nombre")
        if not rif:
            missing_fields.append("RIF")

        if missing_fields:
            messagebox.showwarning("Campos Incompletos", 
                                   "Los siguientes campos son obligatorios y no pueden estar vacíos:\n\n- " + 
                                   "\n- ".join(missing_fields))
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            sql = "INSERT INTO proveedor (nombre, rif, telefono, direccion) VALUES (%s, %s, %s, %s)"
            val = (nombre, rif, telefono if telefono else None, direccion if direccion else None) # Inserta None si están vacíos
            cursor.execute(sql, val)
            db.commit()
            messagebox.showinfo("Éxito", "Proveedor registrado correctamente.")
            
            # Opcional: limpiar los campos después de registrar
            nombre_entry.delete(0, tk.END)
            rif_entry.delete(0, tk.END)
            telefono_entry.delete(0, tk.END)
            direccion_entry.delete(0, tk.END)

        except mysql.connector.Error as err:
            if err.errno == 1062: # Código de error para entrada duplicada (UNIQUE constraint en 'rif')
                messagebox.showerror("Error de Registro", 
                                     "El RIF de proveedor ya existe. Por favor, verifique el dato o consulte si ya está registrado.")
            else:
                messagebox.showerror("Error de Base de Datos", f"Error al registrar proveedor: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    # Botón de Guardar
    ttk.Button(parent_frame, text="Guardar Proveedor", command=guardar_proveedor, 
               style='Action.TButton').pack(pady=20)


def consultar_proveedor_internal(parent_frame):
    clear_frame(parent_frame)
    style = ttk.Style(parent_frame)
    style.configure('Search.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#2196F3", foreground='white', borderwidth=0, relief="flat") 
    style.map('Search.TButton', background=[('active', "#0B7CDA")])

    ttk.Label(parent_frame, text="Consultar Proveedor", style='ContentTitle.TLabel').pack(pady=20)

    search_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    search_frame.pack(padx=20, pady=10, fill="x")
    search_frame.columnconfigure(0, weight=1)
    search_frame.columnconfigure(1, weight=3)
    search_frame.columnconfigure(2, weight=1)

    ttk.Label(search_frame, text="RIF del Proveedor:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    rif_search_entry = ttk.Entry(search_frame, font=("Arial", 10), width=30)
    rif_search_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

    details_frame = ttk.LabelFrame(parent_frame, text="Detalles del Proveedor", style='MainContent.TFrame')
    details_frame.pack(padx=20, pady=10, fill="both", expand=True)
    details_frame.columnconfigure(0, weight=1)
    details_frame.columnconfigure(1, weight=3)

    # Variables para mostrar los detalles del proveedor
    id_proveedor_var = tk.StringVar()
    nombre_var = tk.StringVar()
    rif_var = tk.StringVar()
    telefono_var = tk.StringVar()
    direccion_var = tk.StringVar()

    ttk.Label(details_frame, text="ID:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=id_proveedor_var, style='ContentLabel.TLabel').grid(row=0, column=1, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, text="Nombre:", style='ContentLabel.TLabel').grid(row=1, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=nombre_var, style='ContentLabel.TLabel').grid(row=1, column=1, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, text="RIF:", style='ContentLabel.TLabel').grid(row=2, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=rif_var, style='ContentLabel.TLabel').grid(row=2, column=1, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, text="Teléfono:", style='ContentLabel.TLabel').grid(row=3, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=telefono_var, style='ContentLabel.TLabel').grid(row=3, column=1, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, text="Dirección:", style='ContentLabel.TLabel').grid(row=4, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=direccion_var, style='ContentLabel.TLabel').grid(row=4, column=1, sticky="w", pady=2, padx=5)

    def buscar_proveedor():
        rif = rif_search_entry.get().strip()
        if not rif:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese el RIF del proveedor a buscar.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM proveedor WHERE rif = %s"
            cursor.execute(sql, (rif,))
            proveedor = cursor.fetchone()

            if proveedor:
                id_proveedor_var.set(proveedor['id_proveedor'])
                nombre_var.set(proveedor['nombre'])
                rif_var.set(proveedor['rif'])
                telefono_var.set(proveedor['telefono'] if proveedor['telefono'] else "N/A")
                direccion_var.set(proveedor['direccion'] if proveedor['direccion'] else "N/A")
                messagebox.showinfo("Proveedor Encontrado", f"Proveedor '{proveedor['nombre']}' encontrado.")
            else:
                id_proveedor_var.set("")
                nombre_var.set("")
                rif_var.set("")
                telefono_var.set("")
                direccion_var.set("")
                messagebox.showwarning("No Encontrado", f"No se encontró ningún proveedor con el RIF '{rif}'.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al buscar proveedor: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    ttk.Button(search_frame, text="Buscar", command=buscar_proveedor, style='Search.TButton').grid(row=0, column=2, sticky="ew", pady=5, padx=5)


def editar_proveedor_internal(parent_frame):
    clear_frame(parent_frame)
    style = ttk.Style(parent_frame)
    style.configure('Action.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#4CAF50", foreground='white', borderwidth=0, relief="flat") 
    style.map('Action.TButton', background=[('active', "#45A049")])
    style.configure('Search.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#2196F3", foreground='white', borderwidth=0, relief="flat") 
    style.map('Search.TButton', background=[('active', "#0B7CDA")])


    ttk.Label(parent_frame, text="Editar Proveedor", style='ContentTitle.TLabel').pack(pady=20)

    search_edit_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    search_edit_frame.pack(padx=20, pady=10, fill="x")
    search_edit_frame.columnconfigure(0, weight=1)
    search_edit_frame.columnconfigure(1, weight=3)
    search_edit_frame.columnconfigure(2, weight=1)

    ttk.Label(search_edit_frame, text="RIF del Proveedor a Editar:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    rif_edit_search_entry = ttk.Entry(search_edit_frame, font=("Arial", 10), width=30)
    rif_edit_search_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

    # Frame para los campos de edición, inicialmente oculto o vacío
    edit_form_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    edit_form_frame.pack(padx=20, pady=10, fill="both", expand=True)
    edit_form_frame.columnconfigure(0, weight=1)
    edit_form_frame.columnconfigure(1, weight=3)

    # Campos de entrada para la edición (variables asociadas)
    nombre_edit_entry = ttk.Entry(edit_form_frame, font=("Arial", 10), width=30)
    rif_edit_entry = ttk.Entry(edit_form_frame, font=("Arial", 10), width=30) # RIF también puede ser editable
    telefono_edit_entry = ttk.Entry(edit_form_frame, font=("Arial", 10), width=30)
    direccion_edit_entry = ttk.Entry(edit_form_frame, font=("Arial", 10), width=30)
    
    # Label para el ID de proveedor que no se edita, pero se muestra
    ttk.Label(edit_form_frame, text="ID de Proveedor:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    id_proveedor_display_label = ttk.Label(edit_form_frame, text="", style='ContentLabel.TLabel')
    id_proveedor_display_label.grid(row=0, column=1, sticky="w", pady=5, padx=5)

    ttk.Label(edit_form_frame, text="Nombre:", style='ContentLabel.TLabel').grid(row=1, column=0, sticky="w", pady=5, padx=5)
    nombre_edit_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(edit_form_frame, text="RIF:", style='ContentLabel.TLabel').grid(row=2, column=0, sticky="w", pady=5, padx=5)
    rif_edit_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(edit_form_frame, text="Teléfono:", style='ContentLabel.TLabel').grid(row=3, column=0, sticky="w", pady=5, padx=5)
    telefono_edit_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(edit_form_frame, text="Dirección:", style='ContentLabel.TLabel').grid(row=4, column=0, sticky="w", pady=5, padx=5)
    direccion_edit_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=5)
    
    btn_actualizar = ttk.Button(edit_form_frame, text="Actualizar Proveedor", style='Action.TButton')
    btn_actualizar.grid(row=5, column=0, columnspan=2, pady=15)
    btn_actualizar.grid_remove() # Ocultar inicialmente

    current_proveedor_id = None # Para almacenar el ID del proveedor que se está editando

    def cargar_datos_proveedor():
        nonlocal current_proveedor_id
        rif_proveedor = rif_edit_search_entry.get().strip()
        if not rif_proveedor:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese el RIF del proveedor a editar.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM proveedor WHERE rif = %s"
            cursor.execute(sql, (rif_proveedor,))
            proveedor = cursor.fetchone()

            if proveedor:
                current_proveedor_id = proveedor['id_proveedor']
                id_proveedor_display_label.config(text=proveedor['id_proveedor'])
                nombre_edit_entry.delete(0, tk.END)
                nombre_edit_entry.insert(0, proveedor['nombre'])
                rif_edit_entry.delete(0, tk.END)
                rif_edit_entry.insert(0, proveedor['rif'])
                telefono_edit_entry.delete(0, tk.END)
                telefono_edit_entry.insert(0, proveedor['telefono'] if proveedor['telefono'] else "")
                direccion_edit_entry.delete(0, tk.END)
                direccion_edit_entry.insert(0, proveedor['direccion'] if proveedor['direccion'] else "")
                
                btn_actualizar.grid() # Mostrar el botón de actualizar
                edit_form_frame.pack(padx=20, pady=10, fill="both", expand=True) # Asegurarse de que el frame de edición esté visible
                messagebox.showinfo("Proveedor Encontrado", f"Datos del proveedor '{proveedor['nombre']}' cargados para edición.")
            else:
                messagebox.showwarning("No Encontrado", f"No se encontró ningún proveedor con el RIF '{rif_proveedor}'.")
                # Limpiar y ocultar campos si no se encuentra
                id_proveedor_display_label.config(text="")
                nombre_edit_entry.delete(0, tk.END)
                rif_edit_entry.delete(0, tk.END)
                telefono_edit_entry.delete(0, tk.END)
                direccion_edit_entry.delete(0, tk.END)
                btn_actualizar.grid_remove() # Ocultar el botón de actualizar
                current_proveedor_id = None
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al cargar proveedor para edición: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    def actualizar_proveedor():
        if current_proveedor_id is None:
            messagebox.showwarning("Advertencia", "No hay proveedor cargado para actualizar.")
            return

        nombre = nombre_edit_entry.get().strip()
        rif = rif_edit_entry.get().strip()
        telefono = telefono_edit_entry.get().strip()
        direccion = direccion_edit_entry.get().strip()

        missing_fields = []
        if not nombre:
            missing_fields.append("Nombre")
        if not rif:
            missing_fields.append("RIF")

        if missing_fields:
            messagebox.showwarning("Campos Incompletos", 
                                   "Los siguientes campos son obligatorios y no pueden estar vacíos:\n\n- " + 
                                   "\n- ".join(missing_fields))
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            sql = """
                UPDATE proveedor 
                SET nombre = %s, rif = %s, telefono = %s, direccion = %s
                WHERE id_proveedor = %s
            """
            val = (nombre, rif, telefono if telefono else None, direccion if direccion else None, current_proveedor_id)
            cursor.execute(sql, val)
            db.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Proveedor actualizado correctamente.")
            else:
                messagebox.showwarning("Advertencia", "No se realizó ninguna actualización (los datos eran los mismos o el proveedor no existe).")
        except mysql.connector.Error as err:
            if err.errno == 1062: # Código de error para RIF duplicado
                messagebox.showerror("Error de Actualización", "El RIF ingresado ya pertenece a otro proveedor.")
            else:
                messagebox.showerror("Error de Base de Datos", f"Error al actualizar proveedor: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()
        
        # Después de actualizar, puedes recargar los datos o limpiar el formulario
        rif_edit_search_entry.delete(0, tk.END)
        id_proveedor_display_label.config(text="")
        nombre_edit_entry.delete(0, tk.END)
        rif_edit_entry.delete(0, tk.END)
        telefono_edit_entry.delete(0, tk.END)
        direccion_edit_entry.delete(0, tk.END)
        btn_actualizar.grid_remove()
        current_proveedor_id = None


    ttk.Button(search_edit_frame, text="Cargar Proveedor", command=cargar_datos_proveedor, style='Search.TButton').grid(row=0, column=2, sticky="ew", pady=5, padx=5)
    btn_actualizar.config(command=actualizar_proveedor) # Asignar la función al botón


def eliminar_proveedor_internal(parent_frame):
    clear_frame(parent_frame)
    style = ttk.Style(parent_frame)
    style.configure('Delete.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#f44336", foreground='white', borderwidth=0, relief="flat") 
    style.map('Delete.TButton', background=[('active', "#DA190B")])
    style.configure('Search.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#2196F3", foreground='white', borderwidth=0, relief="flat") 
    style.map('Search.TButton', background=[('active', "#0B7CDA")])


    ttk.Label(parent_frame, text="Eliminar Proveedor", style='ContentTitle.TLabel').pack(pady=20)

    delete_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    delete_frame.pack(padx=20, pady=10, fill="x")
    delete_frame.columnconfigure(0, weight=1)
    delete_frame.columnconfigure(1, weight=3)
    delete_frame.columnconfigure(2, weight=1)

    ttk.Label(delete_frame, text="RIF del Proveedor a Eliminar:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    rif_delete_entry = ttk.Entry(delete_frame, font=("Arial", 10), width=30)
    rif_delete_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

    def eliminar_proveedor():
        rif_proveedor = rif_delete_entry.get().strip()
        if not rif_proveedor:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese el RIF del proveedor a eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", 
                                      f"¿Está seguro de que desea eliminar el proveedor con RIF '{rif_proveedor}'?\nEsta acción es irreversible y podría afectar productos asociados.")
        if not confirm:
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            sql = "DELETE FROM proveedor WHERE rif = %s"
            cursor.execute(sql, (rif_proveedor,))
            db.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Proveedor con RIF '{rif_proveedor}' eliminado correctamente.")
                rif_delete_entry.delete(0, tk.END) # Limpiar el campo
            else:
                messagebox.showwarning("No Encontrado", f"No se encontró ningún proveedor con el RIF '{rif_proveedor}'.")
        except mysql.connector.Error as err:
            # Error 1451: Cannot delete or update a parent row: a foreign key constraint fails
            if err.errno == 1451:
                messagebox.showerror("Error de Eliminación", 
                                     "No se puede eliminar este proveedor porque tiene productos asociados. "
                                     "Por favor, elimine o reasigne los productos de este proveedor primero.")
            else:
                messagebox.showerror("Error de Base de Datos", f"Error al eliminar proveedor: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    ttk.Button(delete_frame, text="Eliminar Proveedor", command=eliminar_proveedor, style='Delete.TButton').grid(row=0, column=2, sticky="ew", pady=5, padx=5)


def consultar_proveedores_general_internal(parent_frame):
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Consultar Listado General de Proveedores", style='ContentTitle.TLabel').pack(pady=20)
    
    # Crear un Frame para contener el Treeview y el botón de refrescar
    supplier_container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    supplier_container.pack(fill="both", expand=True, padx=10, pady=10)

    # Crear el Treeview para mostrar los datos
    tree = ttk.Treeview(supplier_container, columns=("ID", "Nombre", "RIF", "Teléfono", "Dirección"), show="headings")

    # Definir los encabezados de las columnas
    tree.heading("ID", text="ID", anchor=tk.W)
    tree.heading("Nombre", text="Nombre", anchor=tk.W)
    tree.heading("RIF", text="RIF", anchor=tk.W)
    tree.heading("Teléfono", text="Teléfono", anchor=tk.W)
    tree.heading("Dirección", text="Dirección", anchor=tk.W)

    # Definir el ancho de las columnas (ajusta según necesidad)
    tree.column("ID", width=50, stretch=tk.NO)
    tree.column("Nombre", width=180, stretch=tk.NO)
    tree.column("RIF", width=120, stretch=tk.NO)
    tree.column("Teléfono", width=100, stretch=tk.NO)
    tree.column("Dirección", width=250, stretch=tk.NO)

    tree.pack(side="left", fill="both", expand=True)

    # Añadir Scrollbars
    vsb = ttk.Scrollbar(supplier_container, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    hsb = ttk.Scrollbar(parent_frame, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x', padx=10) 
    tree.configure(xscrollcommand=hsb.set)

    def cargar_proveedores():
        # Limpiar Treeview antes de cargar nuevos datos
        for item in tree.get_children():
            tree.delete(item)

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True) # Para acceder a los campos por nombre
        try:
            sql = "SELECT * FROM proveedor ORDER BY nombre ASC"
            cursor.execute(sql)
            proveedores = cursor.fetchall()

            if proveedores:
                for prov in proveedores:
                    tree.insert("", tk.END, values=(
                        prov['id_proveedor'],
                        prov['nombre'],
                        prov['rif'],
                        prov['telefono'] if prov['telefono'] else "N/A", # Mostrar "N/A" si es None
                        prov['direccion'] if prov['direccion'] else "N/A" # Mostrar "N/A" si es None
                    ))
            else:
                pass # El Treeview simplemente aparecerá vacío si no hay datos.

        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al consultar los proveedores: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()
    
    cargar_proveedores() # Cargar los proveedores al construir la UI

    # Botón para refrescar la lista
    ttk.Button(parent_frame, text="Refrescar Lista", command=cargar_proveedores, style='Action.TButton').pack(pady=10)