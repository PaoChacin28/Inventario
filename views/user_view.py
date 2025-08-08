# views/user_view.py
import tkinter as tk
from tkinter import ttk
import controllers.user_controller as user_controller

def clear_frame(frame):
    for widget in frame.winfo_children(): widget.destroy()

def show_register_user_form(parent_frame):
    """Dibuja el formulario para registrar un nuevo usuario."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Registrar Nuevo Usuario", style='ContentTitle.TLabel').pack(pady=20)

    frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    frame.pack(padx=20, pady=10, fill="x")
    frame.columnconfigure(1, weight=1)

    # Widgets
    ttk.Label(frame, text="Nombre Completo:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5)
    nombre_entry = ttk.Entry(frame, width=40)
    nombre_entry.grid(row=0, column=1, sticky="ew", pady=5)
    
    ttk.Label(frame, text="Nombre de Usuario:", style='ContentLabel.TLabel').grid(row=1, column=0, sticky="w", pady=5)
    usuario_entry = ttk.Entry(frame, width=40)
    usuario_entry.grid(row=1, column=1, sticky="ew", pady=5)

    ttk.Label(frame, text="Contraseña:", style='ContentLabel.TLabel').grid(row=2, column=0, sticky="w", pady=5)
    contrasena_entry = ttk.Entry(frame, show="*", width=40)
    contrasena_entry.grid(row=2, column=1, sticky="ew", pady=5)
    
    ttk.Label(frame, text="Rol:", style='ContentLabel.TLabel').grid(row=3, column=0, sticky="w", pady=5)
    rol_combo = ttk.Combobox(frame, values=["Administrador", "Operador"], state="readonly")
    rol_combo.set("Operador")
    rol_combo.grid(row=3, column=1, sticky="ew", pady=5)

    def guardar_action():
        success = user_controller.handle_register_user(
            nombre_entry.get().strip(),
            usuario_entry.get().strip(),
            contrasena_entry.get().strip(),
            rol_combo.get()
        )
        if success:
            nombre_entry.delete(0, tk.END)
            usuario_entry.delete(0, tk.END)
            contrasena_entry.delete(0, tk.END)
            rol_combo.set("Operador")

    ttk.Button(parent_frame, text="Guardar Usuario", command=guardar_action, style='Action.TButton').pack(pady=20)

def show_edit_user_form(parent_frame):
    """Dibuja el formulario para buscar y editar un usuario."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Editar Usuario", style='ContentTitle.TLabel').pack(pady=20)

    # Frame de Búsqueda
    search_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    search_frame.pack(padx=20, pady=10, fill="x")
    search_frame.columnconfigure(1, weight=1)
    ttk.Label(search_frame, text="Usuario a Editar:", style='ContentLabel.TLabel').grid(row=0, column=0, padx=5, sticky="w")
    search_entry = ttk.Entry(search_frame, width=30)
    search_entry.grid(row=0, column=1, padx=5, sticky="ew")
    
    edit_form_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    current_user_id = None

    def buscar_y_cargar_action():
        nonlocal current_user_id
        for widget in edit_form_frame.winfo_children(): widget.destroy()
        
        user_data = user_controller.handle_find_user(search_entry.get().strip())
        
        if user_data:
            current_user_id = user_data['id_usuario']
            
            # Crear widgets de edición dinámicamente
            ttk.Label(edit_form_frame, text="Nombre Completo:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5)
            nombre_edit = ttk.Entry(edit_form_frame, width=40)
            nombre_edit.insert(0, user_data['nombre_completo'])
            nombre_edit.grid(row=0, column=1, sticky="ew", pady=5)

            ttk.Label(edit_form_frame, text="Nueva Contraseña:", style='ContentLabel.TLabel').grid(row=1, column=0, sticky="w", pady=5)
            pass_edit = ttk.Entry(edit_form_frame, show="*", width=40)
            pass_edit.grid(row=1, column=1, sticky="ew", pady=5)

            ttk.Label(edit_form_frame, text="Rol:", style='ContentLabel.TLabel').grid(row=2, column=0, sticky="w", pady=5)
            rol_edit = ttk.Combobox(edit_form_frame, values=["Administrador", "Operador"], state="readonly")
            rol_edit.set(user_data['rol'])
            rol_edit.grid(row=2, column=1, sticky="ew", pady=5)
            
            def actualizar_action():
                success = user_controller.handle_update_user(
                    current_user_id,
                    nombre_edit.get().strip(),
                    rol_edit.get(),
                    pass_edit.get().strip()
                )
                if success:
                    search_entry.delete(0, tk.END)
                    for widget in edit_form_frame.winfo_children(): widget.destroy()

            ttk.Button(edit_form_frame, text="Actualizar", command=actualizar_action, style='Action.TButton').grid(row=3, columnspan=2, pady=10)
            edit_form_frame.pack(padx=20, pady=10, fill="x")
            edit_form_frame.columnconfigure(1, weight=1)

    ttk.Button(search_frame, text="Buscar", command=buscar_y_cargar_action, style='Search.TButton').grid(row=0, column=2, padx=5)

def show_delete_user_form(parent_frame):
    """Dibuja el formulario para eliminar un usuario."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Eliminar Usuario", style='ContentTitle.TLabel').pack(pady=20)
    
    delete_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    delete_frame.pack(padx=20, pady=10, fill="x")
    delete_frame.columnconfigure(1, weight=1)

    ttk.Label(delete_frame, text="Usuario a Eliminar:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", padx=5)
    user_entry = ttk.Entry(delete_frame, width=30)
    user_entry.grid(row=0, column=1, sticky="ew", padx=5)

    def eliminar_action():
        if user_controller.handle_delete_user(user_entry.get().strip()):
            user_entry.delete(0, tk.END)

    ttk.Button(delete_frame, text="Eliminar", command=eliminar_action, style='Delete.TButton').grid(row=0, column=2, padx=5)

def show_all_users_list(parent_frame):
    """Dibuja una tabla con todos los usuarios."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Listado General de Usuarios", style='ContentTitle.TLabel').pack(pady=20)
    
    container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    container.pack(fill="both", expand=True, padx=10, pady=10)
    
    cols = ("ID", "Nombre Completo", "Usuario", "Rol")
    tree = ttk.Treeview(container, columns=cols, show="headings")
    for col in cols: tree.heading(col, text=col)
    
    tree.column("ID", width=60, anchor='center')
    tree.column("Nombre Completo", width=250)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)
    
    def cargar_datos():
        for i in tree.get_children(): tree.delete(i)
        users = user_controller.handle_get_all_users()
        for user in users:
            tree.insert("", "end", values=(user['id_usuario'], user['nombre_completo'], user['usuario'], user['rol']))

    ttk.Button(parent_frame, text="Refrescar Lista", command=cargar_datos, style='Action.TButton').pack(pady=10)
    cargar_datos()