# user_management.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk # Para Treeview y Combobox
import mysql.connector
from db_connection import conectar_db

# --- Funciones de Utilidad (para estilizar ventanas) ---
def setup_window(window, title, geometry="500x400"):
    window.title(title)
    window.geometry(geometry)
    window.configure(bg="#e0f8f7") # Fondo claro para las ventanas de gestión
    window.transient(window.master) # Hace que la ventana sea modal si es llamada desde main_menu
    window.grab_set() # Captura todos los eventos hasta que esta ventana se cierre
    return window

def create_input_field(parent, label_text, entry_width=40, show_char=None):
    frame = tk.Frame(parent, bg="#e0f8f7")
    frame.pack(pady=3, fill="x", padx=10)
    tk.Label(frame, text=label_text, bg="#e0f8f7", font=("Arial", 10)).pack(side="left", padx=5)
    entry = tk.Entry(frame, width=entry_width, font=("Arial", 10), show=show_char)
    entry.pack(side="right", expand=True, fill="x", padx=5)
    return entry

# --- Funciones de Gestión de Usuarios ---

def registrar_usuario():
    win = setup_window(tk.Toplevel(), "Registrar Nuevo Usuario", "450x380")

    tk.Label(win, text="Datos del Nuevo Usuario", font=("Arial", 14, "bold"), bg="#e0f8f7").pack(pady=15)

    e_nombre_completo = create_input_field(win, "Nombre Completo:")
    e_usuario = create_input_field(win, "Usuario:")
    e_contrasena = create_input_field(win, "Contraseña:", show_char="*")
    
    # Para el rol, usamos un Combobox para las opciones ENUM
    frame_rol = tk.Frame(win, bg="#e0f8f7")
    frame_rol.pack(pady=3, fill="x", padx=10)
    tk.Label(frame_rol, text="Rol:", bg="#e0f8f7", font=("Arial", 10)).pack(side="left", padx=5)
    cb_rol = ttk.Combobox(frame_rol, values=["Administrador", "Operador"], state="readonly", font=("Arial", 10))
    cb_rol.set("Operador") # Valor por defecto
    cb_rol.pack(side="right", expand=True, fill="x", padx=5)

    def guardar_usuario():
        nombre_completo = e_nombre_completo.get()
        usuario = e_usuario.get()
        contrasena = e_contrasena.get()
        rol = cb_rol.get()

        if not nombre_completo or not usuario or not contrasena or not rol:
            messagebox.showwarning("Campos Requeridos", "Por favor, complete todos los campos.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            sql = "INSERT INTO usuario (nombre_completo, usuario, contrasena, rol) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre_completo, usuario, contrasena, rol))
            db.commit()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            win.destroy()
        except mysql.connector.Error as err:
            if err.errno == 1062: # Duplicate entry for UNIQUE key (usuario)
                messagebox.showerror("Error de Usuario", "El nombre de usuario ya existe. Por favor, elija otro.")
            else:
                messagebox.showerror("Error de Base de Datos", f"Error al registrar usuario: {err}")
            if db.is_connected():
                db.rollback()
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    tk.Button(win, text="Guardar Usuario", command=guardar_usuario,
              font=("Arial", 10, "bold"), bg="#28a745", fg="white", width=20, cursor="hand2").pack(pady=20)
    win.mainloop()


def consultar_usuario():
    win = setup_window(tk.Toplevel(), "Consultar Usuarios", "700x500")

    tk.Label(win, text="Buscar Usuario", font=("Arial", 14, "bold"), bg="#e0f8f7").pack(pady=15)

    e_busqueda = create_input_field(win, "Nombre o Usuario:")
    
    # Configuración del Treeview para mostrar resultados
    tree_frame = tk.Frame(win, bg="#e0f8f7")
    tree_frame.pack(pady=10, fill="both", expand=True, padx=10)

    columns = ("ID", "Nombre Completo", "Usuario", "Rol") # No mostrar contraseña
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

    for col in columns:
        tree.heading(col, text=col, anchor="w")
        tree.column(col, width=100, anchor="w")

    tree.column("ID", width=50) 
    tree.column("Nombre Completo", width=200)

    # Scrollbar para el Treeview
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x')
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.pack(fill="both", expand=True)

    def buscar_usuario_db():
        for item in tree.get_children():
            tree.delete(item) # Limpiar resultados anteriores

        busqueda = f"%{e_busqueda.get()}%" # Para búsqueda parcial

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True) # Para obtener resultados como diccionarios
        try:
            sql = "SELECT id_usuario, nombre_completo, usuario, rol FROM usuario WHERE nombre_completo LIKE %s OR usuario LIKE %s"
            cursor.execute(sql, (busqueda, busqueda))
            resultados = cursor.fetchall()

            if not resultados:
                messagebox.showinfo("Sin Resultados", "No se encontraron usuarios con ese criterio de búsqueda.")
                return

            for row in resultados:
                tree.insert("", "end", values=(row['id_usuario'], row['nombre_completo'], row['usuario'], row['rol']))

        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al buscar usuario: {err}")
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    tk.Button(win, text="Buscar", command=buscar_usuario_db,
              font=("Arial", 10, "bold"), bg="#007bff", fg="white", width=15, cursor="hand2").pack(pady=10)
    win.mainloop()


def editar_usuario():
    win = setup_window(tk.Toplevel(), "Editar Usuario", "450x480")

    tk.Label(win, text="Editar Datos del Usuario", font=("Arial", 14, "bold"), bg="#e0f8f7").pack(pady=15)

    e_id_usuario_buscar = create_input_field(win, "ID o Usuario a Editar:")
    
    # Campos para mostrar y editar los datos
    e_nombre_completo = create_input_field(win, "Nuevo Nombre Completo:")
    e_usuario = create_input_field(win, "Nuevo Usuario:")
    e_contrasena = create_input_field(win, "Nueva Contraseña:", show_char="*")
    
    frame_rol_edit = tk.Frame(win, bg="#e0f8f7")
    frame_rol_edit.pack(pady=3, fill="x", padx=10)
    tk.Label(frame_rol_edit, text="Nuevo Rol:", bg="#e0f8f7", font=("Arial", 10)).pack(side="left", padx=5)
    cb_rol_edit = ttk.Combobox(frame_rol_edit, values=["Administrador", "Operador"], state="readonly", font=("Arial", 10))
    cb_rol_edit.pack(side="right", expand=True, fill="x", padx=5)

    current_user_id = None # Para guardar el ID del usuario que se está editando

    def cargar_usuario():
        nonlocal current_user_id
        busqueda = e_id_usuario_buscar.get()
        if not busqueda:
            messagebox.showwarning("Entrada Vacía", "Por favor, ingresa el ID o nombre de usuario a buscar.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor(dictionary=True)
        try:
            if busqueda.isdigit(): # Si es un número, buscar por ID
                sql = "SELECT id_usuario, nombre_completo, usuario, contrasena, rol FROM usuario WHERE id_usuario = %s"
                cursor.execute(sql, (busqueda,))
            else: # Si no es un número, buscar por nombre de usuario
                sql = "SELECT id_usuario, nombre_completo, usuario, contrasena, rol FROM usuario WHERE usuario = %s"
                cursor.execute(sql, (busqueda,))
            
            usuario_data = cursor.fetchone()

            if usuario_data:
                current_user_id = usuario_data['id_usuario']
                e_nombre_completo.delete(0, tk.END)
                e_nombre_completo.insert(0, usuario_data['nombre_completo'])
                e_usuario.delete(0, tk.END)
                e_usuario.insert(0, usuario_data['usuario'])
                e_contrasena.delete(0, tk.END)
                e_contrasena.insert(0, usuario_data['contrasena']) # En un sistema real, no cargarías la contraseña plana
                cb_rol_edit.set(usuario_data['rol'])
                messagebox.showinfo("Usuario Encontrado", f"Usuario '{usuario_data['usuario']}' cargado.")
            else:
                current_user_id = None
                messagebox.showerror("No Encontrado", "No se encontró un usuario con ese ID o nombre de usuario.")
                # Limpiar campos si no se encuentra
                e_nombre_completo.delete(0, tk.END)
                e_usuario.delete(0, tk.END)
                e_contrasena.delete(0, tk.END)
                cb_rol_edit.set("")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Base de Datos", f"Error al cargar usuario: {err}")
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    tk.Button(win, text="Cargar Usuario", command=cargar_usuario,
              font=("Arial", 10, "bold"), bg="#007bff", fg="white", width=20, cursor="hand2").pack(pady=10)

    def guardar_cambios():
        if current_user_id is None:
            messagebox.showwarning("Advertencia", "Primero carga un usuario para editar.")
            return

        nombre_completo = e_nombre_completo.get()
        usuario = e_usuario.get()
        contrasena = e_contrasena.get()
        rol = cb_rol_edit.get()

        if not nombre_completo or not usuario or not contrasena or not rol:
            messagebox.showwarning("Campos Requeridos", "Todos los campos son obligatorios.")
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            sql = "UPDATE usuario SET nombre_completo=%s, usuario=%s, contrasena=%s, rol=%s WHERE id_usuario=%s"
            cursor.execute(sql, (nombre_completo, usuario, contrasena, rol, current_user_id))
            db.commit()
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
            win.destroy()
        except mysql.connector.Error as err:
            if err.errno == 1062: # Duplicate entry for UNIQUE key (usuario)
                messagebox.showerror("Error de Usuario", "El nuevo nombre de usuario ya existe. Por favor, elija otro.")
            else:
                messagebox.showerror("Error de Base de Datos", f"Error al actualizar usuario: {err}")
            if db.is_connected():
                db.rollback()
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    tk.Button(win, text="Guardar Cambios", command=guardar_cambios,
              font=("Arial", 10, "bold"), bg="#28a745", fg="white", width=20, cursor="hand2").pack(pady=15)
    win.mainloop()


def eliminar_usuario():
    win = setup_window(tk.Toplevel(), "Eliminar Usuario", "400x250")

    tk.Label(win, text="Eliminar Usuario", font=("Arial", 14, "bold"), bg="#e0f8f7").pack(pady=15)

    e_id_usuario_eliminar = create_input_field(win, "ID o Usuario a Eliminar:")

    def confirmar_eliminar():
        busqueda = e_id_usuario_eliminar.get()
        if not busqueda:
            messagebox.showwarning("Entrada Vacía", "Por favor, ingresa el ID o nombre de usuario a eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", 
                                      f"¿Estás seguro de que quieres eliminar el usuario con ID/Usuario '{busqueda}'? "
                                      "Esta acción es irreversible y podría afectar reportes o movimientos asociados.")
        if not confirm:
            return

        db = conectar_db()
        if db is None:
            return

        cursor = db.cursor()
        try:
            # Primero, buscar el ID real para asegurar que eliminamos el correcto
            if busqueda.isdigit():
                sql_select = "SELECT id_usuario FROM usuario WHERE id_usuario = %s"
            else:
                sql_select = "SELECT id_usuario FROM usuario WHERE usuario = %s"
            cursor.execute(sql_select, (busqueda,))
            usuario_id = cursor.fetchone()

            if usuario_id:
                # Si el usuario existe, intentar eliminarlo
                sql_delete = "DELETE FROM usuario WHERE id_usuario = %s"
                cursor.execute(sql_delete, (usuario_id[0],))
                db.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
                    win.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el usuario. No encontrado o error interno.")
            else:
                messagebox.showerror("No Encontrado", "No se encontró un usuario con ese ID o nombre de usuario.")

        except mysql.connector.Error as err:
            if err.errno == 1451: # Foreign key constraint fails (si el usuario tiene reportes o movimientos asociados)
                 messagebox.showerror("Error de Integridad", "No se puede eliminar el usuario porque tiene reportes o movimientos asociados. Elimina estos registros primero.")
            else:
                messagebox.showerror("Error de Base de Datos", f"Error al eliminar usuario: {err}")
            if db.is_connected():
                db.rollback()
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

    tk.Button(win, text="Eliminar Usuario", command=confirmar_eliminar,
              font=("Arial", 10, "bold"), bg="#dc3545", fg="white", width=20, cursor="hand2").pack(pady=20)
    win.mainloop()