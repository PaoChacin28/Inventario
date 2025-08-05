# user_management.py
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Asume que db_connection.py está en la misma carpeta
from db_connection import conectar_db 

# Función auxiliar para limpiar el frame 
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# --- Funciones de Gestión de Usuarios ---

def registrar_usuario_internal(parent_frame):
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
    ttk.Label(parent_frame, text="Registrar Nuevo Usuario", style='ContentTitle.TLabel').pack(pady=20)

    # Frame para los campos de entrada para mejor organización
    input_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    input_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Usar grid para los campos del formulario para un mejor control del layout
    input_frame.columnconfigure(0, weight=1)
    input_frame.columnconfigure(1, weight=3) # Dar más espacio a las entradas

    # Campo: Nombre Completo
    ttk.Label(input_frame, text="Nombre Completo:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    nombre_completo_entry = ttk.Entry(input_frame, font=("Arial", 10), width=30)
    nombre_completo_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

    # Campo: Nombre de Usuario (para login)
    ttk.Label(input_frame, text="Nombre de Usuario:", style='ContentLabel.TLabel').grid(row=1, column=0, sticky="w", pady=5, padx=5)
    usuario_entry = ttk.Entry(input_frame, font=("Arial", 10), width=30)
    usuario_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

    # Campo: Contraseña
    ttk.Label(input_frame, text="Contraseña:", style='ContentLabel.TLabel').grid(row=2, column=0, sticky="w", pady=5, padx=5)
    contrasena_entry = ttk.Entry(input_frame, show="*", font=("Arial", 10), width=30) # show="*" para ocultar la contraseña
    contrasena_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

    # Campo: Rol (Administrador/Operador)
    ttk.Label(input_frame, text="Rol:", style='ContentLabel.TLabel').grid(row=3, column=0, sticky="w", pady=5, padx=5)
    rol_combobox = ttk.Combobox(input_frame, values=["Administrador", "Operador"], state="readonly", font=("Arial", 10), width=28)
    rol_combobox.grid(row=3, column=1, sticky="ew", pady=5, padx=5)
    rol_combobox.set("Operador") # Valor por defecto

    def guardar_usuario():
        nombre_completo = nombre_completo_entry.get().strip()
        usuario = usuario_entry.get().strip()
        contrasena = contrasena_entry.get().strip()
        rol = rol_combobox.get().strip()

        missing_fields = []
        if not nombre_completo:
            missing_fields.append("Nombre Completo")
        if not usuario:
            missing_fields.append("Nombre de Usuario")
        if not contrasena:
            missing_fields.append("Contraseña")
        if not rol:
            missing_fields.append("Rol")

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
            sql = "INSERT INTO usuario (nombre_completo, usuario, contrasena, rol) VALUES (%s, %s, %s, %s)"
            val = (nombre_completo, usuario, contrasena, rol)
            cursor.execute(sql, val)
            db.commit()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            
            # Opcional: limpiar los campos después de registrar
            nombre_completo_entry.delete(0, tk.END)
            usuario_entry.delete(0, tk.END)
            contrasena_entry.delete(0, tk.END)
            rol_combobox.set("Operador") # Resetear a valor por defecto

        except mysql.connector.Error as err:
            if err.errno == 1062: # Código de error para entrada duplicada (UNIQUE constraint en 'usuario')
                messagebox.showerror("Error de Registro", "El nombre de usuario ya existe. Por favor, elija otro.")
            else:
                messagebox.showerror("Error de Base de Datos", f"Error al registrar usuario: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    # Botón de Guardar
    ttk.Button(parent_frame, text="Guardar Usuario", command=guardar_usuario, style='Action.TButton').pack(pady=20)


def consultar_usuario_internal(parent_frame):
    clear_frame(parent_frame)
    style = ttk.Style(parent_frame)
    style.configure('Search.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#2196F3", foreground='white', borderwidth=0, relief="flat") 
    style.map('Search.TButton', background=[('active', "#0B7CDA")])

    ttk.Label(parent_frame, text="Consultar Usuario Específico", style='ContentTitle.TLabel').pack(pady=20)

    search_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    search_frame.pack(padx=20, pady=10, fill="x")
    search_frame.columnconfigure(0, weight=1)
    search_frame.columnconfigure(1, weight=3)
    search_frame.columnconfigure(2, weight=1)

    ttk.Label(search_frame, text="Nombre de Usuario:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    usuario_search_entry = ttk.Entry(search_frame, font=("Arial", 10), width=30)
    usuario_search_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

    details_frame = ttk.LabelFrame(parent_frame, text="Detalles del Usuario", style='MainContent.TFrame')
    details_frame.pack(padx=20, pady=10, fill="both", expand=True)
    details_frame.columnconfigure(0, weight=1)
    details_frame.columnconfigure(1, weight=3)

    # Variables para mostrar los detalles del usuario
    id_usuario_var = tk.StringVar()
    nombre_completo_var = tk.StringVar()
    usuario_var = tk.StringVar()
    rol_var = tk.StringVar()

    ttk.Label(details_frame, text="ID:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=id_usuario_var, style='ContentLabel.TLabel').grid(row=0, column=1, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, text="Nombre Completo:", style='ContentLabel.TLabel').grid(row=1, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=nombre_completo_var, style='ContentLabel.TLabel').grid(row=1, column=1, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, text="Nombre de Usuario:", style='ContentLabel.TLabel').grid(row=2, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=usuario_var, style='ContentLabel.TLabel').grid(row=2, column=1, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, text="Rol:", style='ContentLabel.TLabel').grid(row=3, column=0, sticky="w", pady=2, padx=5)
    ttk.Label(details_frame, textvariable=rol_var, style='ContentLabel.TLabel').grid(row=3, column=1, sticky="w", pady=2, padx=5)

    def buscar_usuario():
        usuario_nombre = usuario_search_entry.get().strip()
        if not usuario_nombre:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese el nombre de usuario a buscar.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True)
        try:
            sql = "SELECT id_usuario, nombre_completo, usuario, rol FROM usuario WHERE usuario = %s"
            cursor.execute(sql, (usuario_nombre,))
            usuario = cursor.fetchone()

            if usuario:
                id_usuario_var.set(usuario['id_usuario'])
                nombre_completo_var.set(usuario['nombre_completo'])
                usuario_var.set(usuario['usuario'])
                rol_var.set(usuario['rol'])
                messagebox.showinfo("Usuario Encontrado", f"Usuario '{usuario['nombre_completo']}' encontrado.")
            else:
                id_usuario_var.set("")
                nombre_completo_var.set("")
                usuario_var.set("")
                rol_var.set("")
                messagebox.showwarning("No Encontrado", f"No se encontró ningún usuario con el nombre '{usuario_nombre}'.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al buscar usuario: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    ttk.Button(search_frame, text="Buscar", command=buscar_usuario, style='Search.TButton').grid(row=0, column=2, sticky="ew", pady=5, padx=5)


def editar_usuario_internal(parent_frame):
    clear_frame(parent_frame)
    style = ttk.Style(parent_frame)
    style.configure('Action.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#4CAF50", foreground='white', borderwidth=0, relief="flat") 
    style.map('Action.TButton', background=[('active', "#45A049")])
    style.configure('Search.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#2196F3", foreground='white', borderwidth=0, relief="flat") 
    style.map('Search.TButton', background=[('active', "#0B7CDA")])

    ttk.Label(parent_frame, text="Editar Usuario", style='ContentTitle.TLabel').pack(pady=20)

    search_edit_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    search_edit_frame.pack(padx=20, pady=10, fill="x")
    search_edit_frame.columnconfigure(0, weight=1)
    search_edit_frame.columnconfigure(1, weight=3)
    search_edit_frame.columnconfigure(2, weight=1)

    ttk.Label(search_edit_frame, text="Nombre de Usuario a Editar:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    usuario_edit_search_entry = ttk.Entry(search_edit_frame, font=("Arial", 10), width=30)
    usuario_edit_search_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

    # Frame para los campos de edición, inicialmente oculto o vacío
    edit_form_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    edit_form_frame.pack(padx=20, pady=10, fill="both", expand=True)
    edit_form_frame.columnconfigure(0, weight=1)
    edit_form_frame.columnconfigure(1, weight=3)

    # Campos de entrada para la edición (variables asociadas)
    nombre_completo_edit_entry = ttk.Entry(edit_form_frame, font=("Arial", 10), width=30)
    # No se permite editar el nombre de usuario directamente si es la clave de búsqueda, para evitar problemas
    # con UNIQUE constraints. Se puede hacer si se añade un campo para el "nuevo nombre de usuario".
    # Por ahora, si se quiere cambiar el nombre de usuario, se debería eliminar y registrar uno nuevo.
    # Si se decide que el nombre de usuario es editable, se debe manejar la validación UNIQUE.
    contrasena_edit_entry = ttk.Entry(edit_form_frame, show="*", font=("Arial", 10), width=30)
    rol_edit_combobox = ttk.Combobox(edit_form_frame, values=["Administrador", "Operador"], state="readonly", font=("Arial", 10), width=28)
    
    # Label para el ID de usuario que no se edita, pero se muestra
    ttk.Label(edit_form_frame, text="ID de Usuario:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    id_usuario_display_label = ttk.Label(edit_form_frame, text="", style='ContentLabel.TLabel')
    id_usuario_display_label.grid(row=0, column=1, sticky="w", pady=5, padx=5)

    ttk.Label(edit_form_frame, text="Nombre Completo:", style='ContentLabel.TLabel').grid(row=1, column=0, sticky="w", pady=5, padx=5)
    nombre_completo_edit_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
    # Campo para mostrar el nombre de usuario actual, no editable directamente
    ttk.Label(edit_form_frame, text="Nombre de Usuario Actual:", style='ContentLabel.TLabel').grid(row=2, column=0, sticky="w", pady=5, padx=5)
    usuario_actual_label = ttk.Label(edit_form_frame, text="", style='ContentLabel.TLabel')
    usuario_actual_label.grid(row=2, column=1, sticky="w", pady=5, padx=5)

    ttk.Label(edit_form_frame, text="Nueva Contraseña (dejar en blanco para no cambiar):", style='ContentLabel.TLabel').grid(row=3, column=0, sticky="w", pady=5, padx=5)
    contrasena_edit_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=5)
    ttk.Label(edit_form_frame, text="Rol:", style='ContentLabel.TLabel').grid(row=4, column=0, sticky="w", pady=5, padx=5)
    rol_edit_combobox.grid(row=4, column=1, sticky="ew", pady=5, padx=5)
    
    btn_actualizar = ttk.Button(edit_form_frame, text="Actualizar Usuario", style='Action.TButton')
    btn_actualizar.grid(row=5, column=0, columnspan=2, pady=15)
    btn_actualizar.grid_remove() # Ocultar inicialmente

    current_user_id = None # Para almacenar el ID del usuario que se está editando

    def cargar_datos_usuario():
        nonlocal current_user_id
        usuario_nombre = usuario_edit_search_entry.get().strip()
        if not usuario_nombre:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese el nombre de usuario a editar.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True)
        try:
            sql = "SELECT id_usuario, nombre_completo, usuario, rol FROM usuario WHERE usuario = %s"
            cursor.execute(sql, (usuario_nombre,))
            usuario = cursor.fetchone()

            if usuario:
                current_user_id = usuario['id_usuario']
                id_usuario_display_label.config(text=usuario['id_usuario'])
                nombre_completo_edit_entry.delete(0, tk.END)
                nombre_completo_edit_entry.insert(0, usuario['nombre_completo'])
                usuario_actual_label.config(text=usuario['usuario']) # Mostrar el nombre de usuario, no permitir edición directa
                contrasena_edit_entry.delete(0, tk.END) # Dejar en blanco para una nueva contraseña
                rol_edit_combobox.set(usuario['rol'])
                
                btn_actualizar.grid() # Mostrar el botón de actualizar
                edit_form_frame.pack(padx=20, pady=10, fill="both", expand=True) # Asegurarse de que el frame de edición esté visible
                messagebox.showinfo("Usuario Encontrado", f"Datos del usuario '{usuario['nombre_completo']}' cargados para edición.")
            else:
                messagebox.showwarning("No Encontrado", f"No se encontró ningún usuario con el nombre '{usuario_nombre}'.")
                # Limpiar y ocultar campos si no se encuentra
                id_usuario_display_label.config(text="")
                nombre_completo_edit_entry.delete(0, tk.END)
                usuario_actual_label.config(text="")
                contrasena_edit_entry.delete(0, tk.END)
                rol_edit_combobox.set("Operador")
                btn_actualizar.grid_remove() # Ocultar el botón de actualizar
                current_user_id = None
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al cargar usuario para edición: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    def actualizar_usuario():
        if current_user_id is None:
            messagebox.showwarning("Advertencia", "No hay usuario cargado para actualizar.")
            return

        nombre_completo = nombre_completo_edit_entry.get().strip()
        nueva_contrasena = contrasena_edit_entry.get().strip()
        rol = rol_edit_combobox.get().strip()
        
        # El nombre de usuario no se edita directamente desde este formulario para simplificar
        # y evitar conflictos de UNIQUE KEY. Se asume que solo se edita nombre, contraseña y rol.

        missing_fields = []
        if not nombre_completo:
            missing_fields.append("Nombre Completo")
        if not rol:
            missing_fields.append("Rol")

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
            if nueva_contrasena: # Si se ingresó una nueva contraseña, actualizarla
                sql = """
                    UPDATE usuario 
                    SET nombre_completo = %s, contrasena = %s, rol = %s
                    WHERE id_usuario = %s
                """
                val = (nombre_completo, nueva_contrasena, rol, current_user_id)
            else: # Si la contraseña está vacía, no se actualiza
                sql = """
                    UPDATE usuario 
                    SET nombre_completo = %s, rol = %s
                    WHERE id_usuario = %s
                """
                val = (nombre_completo, rol, current_user_id)

            cursor.execute(sql, val)
            db.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
            else:
                messagebox.showwarning("Advertencia", "No se realizó ninguna actualización (los datos eran los mismos o el usuario no existe).")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al actualizar usuario: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()
        
        # Después de actualizar, limpiar el formulario y resetear
        usuario_edit_search_entry.delete(0, tk.END)
        id_usuario_display_label.config(text="")
        nombre_completo_edit_entry.delete(0, tk.END)
        usuario_actual_label.config(text="")
        contrasena_edit_entry.delete(0, tk.END)
        rol_edit_combobox.set("Operador")
        btn_actualizar.grid_remove()
        current_user_id = None


    ttk.Button(search_edit_frame, text="Cargar Usuario", command=cargar_datos_usuario, style='Search.TButton').grid(row=0, column=2, sticky="ew", pady=5, padx=5)
    btn_actualizar.config(command=actualizar_usuario) # Asignar la función al botón


def eliminar_usuario_internal(parent_frame):
    clear_frame(parent_frame)
    style = ttk.Style(parent_frame)
    style.configure('Delete.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#f44336", foreground='white', borderwidth=0, relief="flat") 
    style.map('Delete.TButton', background=[('active', "#DA190B")])
    style.configure('Search.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#2196F3", foreground='white', borderwidth=0, relief="flat") 
    style.map('Search.TButton', background=[('active', "#0B7CDA")])

    ttk.Label(parent_frame, text="Eliminar Usuario", style='ContentTitle.TLabel').pack(pady=20)

    delete_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    delete_frame.pack(padx=20, pady=10, fill="x")
    delete_frame.columnconfigure(0, weight=1)
    delete_frame.columnconfigure(1, weight=3)
    delete_frame.columnconfigure(2, weight=1)

    ttk.Label(delete_frame, text="Nombre de Usuario a Eliminar:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5, padx=5)
    usuario_delete_entry = ttk.Entry(delete_frame, font=("Arial", 10), width=30)
    usuario_delete_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

    def eliminar_usuario():
        usuario_nombre = usuario_delete_entry.get().strip()
        if not usuario_nombre:
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese el nombre de usuario a eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", 
                                      f"¿Está seguro de que desea eliminar el usuario con nombre '{usuario_nombre}'?\nEsta acción es irreversible.")
        if not confirm:
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            sql = "DELETE FROM usuario WHERE usuario = %s"
            cursor.execute(sql, (usuario_nombre,))
            db.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Usuario '{usuario_nombre}' eliminado correctamente.")
                usuario_delete_entry.delete(0, tk.END) # Limpiar el campo
            else:
                messagebox.showwarning("No Encontrado", f"No se encontró ningún usuario con el nombre '{usuario_nombre}'.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al eliminar usuario: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()

    ttk.Button(delete_frame, text="Eliminar Usuario", command=eliminar_usuario, style='Delete.TButton').grid(row=0, column=2, sticky="ew", pady=5, padx=5)


def consultar_usuarios_general_internal(parent_frame):
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Consultar Listado General de Usuarios", style='ContentTitle.TLabel').pack(pady=20)
    
    # Crear un Frame para contener el Treeview y el botón de refrescar
    user_container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    user_container.pack(fill="both", expand=True, padx=10, pady=10)

    # Crear el Treeview para mostrar los datos
    tree = ttk.Treeview(user_container, columns=("ID", "Nombre Completo", "Usuario", "Rol"), show="headings")

    # Definir los encabezados de las columnas
    tree.heading("ID", text="ID", anchor=tk.W)
    tree.heading("Nombre Completo", text="Nombre Completo", anchor=tk.W)
    tree.heading("Usuario", text="Usuario", anchor=tk.W)
    tree.heading("Rol", text="Rol", anchor=tk.W)

    # Definir el ancho de las columnas (ajusta según necesidad)
    tree.column("ID", width=50, stretch=tk.NO)
    tree.column("Nombre Completo", width=200, stretch=tk.NO)
    tree.column("Usuario", width=150, stretch=tk.NO)
    tree.column("Rol", width=100, stretch=tk.NO)

    tree.pack(side="left", fill="both", expand=True)

    # Añadir Scrollbars
    vsb = ttk.Scrollbar(user_container, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    hsb = ttk.Scrollbar(parent_frame, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x', padx=10) 
    tree.configure(xscrollcommand=hsb.set)

    def cargar_usuarios():
        # Limpiar Treeview antes de cargar nuevos datos
        for item in tree.get_children():
            tree.delete(item)

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True) # Para acceder a los campos por nombre
        try:
            sql = "SELECT id_usuario, nombre_completo, usuario, rol FROM usuario ORDER BY nombre_completo ASC"
            cursor.execute(sql)
            usuarios = cursor.fetchall()

            if usuarios:
                for user in usuarios:
                    tree.insert("", tk.END, values=(
                        user['id_usuario'],
                        user['nombre_completo'],
                        user['usuario'],
                        user['rol']
                    ))
            else:
                pass # El Treeview simplemente aparecerá vacío si no hay datos.

        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al consultar los usuarios: {err}")
        finally:
            if db and db.is_connected():
                cursor.close()
                db.close()
    
    cargar_usuarios() # Cargar los usuarios al construir la UI

    # Botón para refrescar la lista
    ttk.Button(parent_frame, text="Refrescar Lista", command=cargar_usuarios, style='Action.TButton').pack(pady=10)