# views/provider_view.py
import tkinter as tk
from tkinter import ttk
import controllers.provider_controller as provider_controller

def clear_frame(frame):
    for widget in frame.winfo_children(): widget.destroy()

def show_register_provider_form(parent_frame):
    """Dibuja el formulario para registrar un nuevo proveedor."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Registrar Nuevo Proveedor", style='ContentTitle.TLabel').pack(pady=20)
    
    frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    frame.pack(padx=20, pady=10, fill="x")
    frame.columnconfigure(1, weight=1)

    # Widgets
    ttk.Label(frame, text="Nombre:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5)
    nombre_entry = ttk.Entry(frame, width=40)
    nombre_entry.grid(row=0, column=1, sticky="ew", pady=5)
    
    ttk.Label(frame, text="RIF:", style='ContentLabel.TLabel').grid(row=1, column=0, sticky="w", pady=5)
    rif_entry = ttk.Entry(frame, width=40)
    rif_entry.grid(row=1, column=1, sticky="ew", pady=5)

    ttk.Label(frame, text="Teléfono:", style='ContentLabel.TLabel').grid(row=2, column=0, sticky="w", pady=5)
    telefono_entry = ttk.Entry(frame, width=40)
    telefono_entry.grid(row=2, column=1, sticky="ew", pady=5)

    ttk.Label(frame, text="Dirección:", style='ContentLabel.TLabel').grid(row=3, column=0, sticky="w", pady=5)
    direccion_entry = ttk.Entry(frame, width=40)
    direccion_entry.grid(row=3, column=1, sticky="ew", pady=5)

    def guardar_action():
        success = provider_controller.handle_add_provider(
            nombre_entry.get().strip(),
            rif_entry.get().strip(),
            telefono_entry.get().strip(),
            direccion_entry.get().strip()
        )
        if success:
            nombre_entry.delete(0, tk.END)
            rif_entry.delete(0, tk.END)
            telefono_entry.delete(0, tk.END)
            direccion_entry.delete(0, tk.END)

    ttk.Button(parent_frame, text="Guardar Proveedor", command=guardar_action, style='Action.TButton').pack(pady=20)

def show_edit_provider_form(parent_frame):
    """Dibuja el formulario para buscar y editar un proveedor."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Editar Proveedor", style='ContentTitle.TLabel').pack(pady=20)

    # Frame de Búsqueda
    search_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    search_frame.pack(padx=20, pady=10, fill="x")
    search_frame.columnconfigure(1, weight=1)
    ttk.Label(search_frame, text="RIF del Proveedor:", style='ContentLabel.TLabel').grid(row=0, column=0, padx=5, sticky="w")
    search_entry = ttk.Entry(search_frame, width=30)
    search_entry.grid(row=0, column=1, padx=5, sticky="ew")
    
    edit_form_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    current_provider_id = None

    def buscar_y_cargar_action():
        nonlocal current_provider_id
        for widget in edit_form_frame.winfo_children(): widget.destroy()
        
        provider_data = provider_controller.handle_find_provider(search_entry.get().strip())
        
        if provider_data:
            current_provider_id = provider_data['id_proveedor']
            
            # Crear widgets de edición
            ttk.Label(edit_form_frame, text="Nombre:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", pady=5)
            nombre_edit = ttk.Entry(edit_form_frame, width=40); nombre_edit.insert(0, provider_data['nombre']); nombre_edit.grid(row=0, column=1, sticky="ew", pady=5)
            
            ttk.Label(edit_form_frame, text="RIF:", style='ContentLabel.TLabel').grid(row=1, column=0, sticky="w", pady=5)
            rif_edit = ttk.Entry(edit_form_frame, width=40); rif_edit.insert(0, provider_data['rif']); rif_edit.grid(row=1, column=1, sticky="ew", pady=5)

            ttk.Label(edit_form_frame, text="Teléfono:", style='ContentLabel.TLabel').grid(row=2, column=0, sticky="w", pady=5)
            tel_edit = ttk.Entry(edit_form_frame, width=40); tel_edit.insert(0, provider_data['telefono'] or ""); tel_edit.grid(row=2, column=1, sticky="ew", pady=5)
            
            ttk.Label(edit_form_frame, text="Dirección:", style='ContentLabel.TLabel').grid(row=3, column=0, sticky="w", pady=5)
            dir_edit = ttk.Entry(edit_form_frame, width=40); dir_edit.insert(0, provider_data['direccion'] or ""); dir_edit.grid(row=3, column=1, sticky="ew", pady=5)
            
            def actualizar_action():
                success = provider_controller.handle_update_provider(current_provider_id, nombre_edit.get(), rif_edit.get(), tel_edit.get(), dir_edit.get())
                if success:
                    search_entry.delete(0, tk.END); [widget.destroy() for widget in edit_form_frame.winfo_children()]

            ttk.Button(edit_form_frame, text="Actualizar", command=actualizar_action, style='Action.TButton').grid(row=4, columnspan=2, pady=10)
            edit_form_frame.pack(padx=20, pady=10, fill="x"); edit_form_frame.columnconfigure(1, weight=1)

    ttk.Button(search_frame, text="Buscar", command=buscar_y_cargar_action, style='Search.TButton').grid(row=0, column=2, padx=5)

def show_delete_provider_form(parent_frame):
    """Dibuja el formulario para eliminar un proveedor."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Eliminar Proveedor", style='ContentTitle.TLabel').pack(pady=20)
    
    delete_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    delete_frame.pack(padx=20, pady=10, fill="x")
    delete_frame.columnconfigure(1, weight=1)

    ttk.Label(delete_frame, text="RIF del Proveedor:", style='ContentLabel.TLabel').grid(row=0, column=0, sticky="w", padx=5)
    rif_entry = ttk.Entry(delete_frame, width=30)
    rif_entry.grid(row=0, column=1, sticky="ew", padx=5)

    def eliminar_action():
        if provider_controller.handle_delete_provider(rif_entry.get().strip()):
            rif_entry.delete(0, tk.END)

    ttk.Button(delete_frame, text="Eliminar", command=eliminar_action, style='Delete.TButton').grid(row=0, column=2, padx=5)

def show_all_providers_list(parent_frame):
    """Dibuja una tabla con todos los proveedores."""
    clear_frame(parent_frame)
    ttk.Label(parent_frame, text="Listado General de Proveedores", style='ContentTitle.TLabel').pack(pady=20)
    
    container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    container.pack(fill="both", expand=True, padx=10, pady=10)
    
    cols = ("ID", "Nombre", "RIF", "Teléfono", "Dirección")
    tree = ttk.Treeview(container, columns=cols, show="headings")
    for col in cols: tree.heading(col, text=col)
    
    tree.column("ID", width=60, anchor='center')
    tree.column("Nombre", width=200)
    tree.column("Dirección", width=300)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)
    
    def cargar_datos():
        for i in tree.get_children(): tree.delete(i)
        providers = provider_controller.handle_get_all_providers()
        for p in providers:
            tree.insert("", "end", values=(p['id_proveedor'], p['nombre'], p['rif'], p['telefono'] or "N/A", p['direccion'] or "N/A"))

    ttk.Button(parent_frame, text="Refrescar Lista", command=cargar_datos, style='Action.TButton').pack(pady=10)
    cargar_datos()