# views/help_view.py
import tkinter as tk
from tkinter import ttk

MANUAL_TEXT = """
MANUAL DE USUARIO - SISTEMA DE INVENTARIO JPG

Bienvenido al sistema de gestión de inventario. A continuación se describen las funcionalidades principales de cada módulo.

----------------------------------------------------
1. MÓDULO DE PRODUCTOS
----------------------------------------------------
Esta sección es el catálogo central de todos los artículos.

- Listado General: Muestra todos los productos activos. La columna "Stock Total" es un cálculo en tiempo real de la suma de todos los lotes de ese producto.
- Añadir Producto: Abre un formulario para definir un nuevo producto (código, nombre, tipo) y asociarle uno o varios proveedores iniciales.
- Editar Seleccionado: Permite cambiar el nombre o el tipo de un producto seleccionado.
- Desactivar Seleccionado: Oculta un producto de las listas activas, pero mantiene su historial. NO lo borra permanentemente.
- Ver Lotes: Muestra una tabla con todos los lotes (entregas) de un producto seleccionado, detallando el stock individual de cada uno y sus fechas.
- Ver Proveedores: Muestra una tabla con todos los proveedores asociados a un producto y permite gestionar dichas asociaciones.

----------------------------------------------------
2. MÓDULO DE MOVIMIENTOS
----------------------------------------------------
Este es el módulo para registrar todas las operaciones del almacén.

- Historial de Movimientos: Es la vista principal. Muestra un registro de auditoría de todas las entradas, salidas y ajustes realizados en el sistema.
- Registrar Nuevo Movimiento: Abre el formulario para registrar una nueva operación. El formulario es dinámico:
    - Si elige "Entrada": Se le pedirá definir un nuevo LOTE para un producto (con su tag, cantidad, unidad y fecha de vencimiento).
    - Si elige "Salida": Deberá seleccionar un LOTE existente de la lista, y la cantidad se descontará de ese lote específico.
    - Si elige "Ajuste": Deberá seleccionar un LOTE existente, ingresar una cantidad (positiva o negativa) y una descripción obligatoria (ej. "Merma por producto dañado").

----------------------------------------------------
3. MÓDULOS DE ADMINISTRADOR
----------------------------------------------------
Estas secciones solo son visibles para usuarios con el rol "Administrador".

- Usuarios: Permite crear, editar y desactivar las cuentas de usuario que pueden acceder al sistema.
- Proveedores: Permite gestionar el catálogo de proveedores.
- Reportes: Herramienta para generar informes dinámicos y exportables a excel, como "Stock Mínimo", "Próximos a Vencer" o historiales por rango de fecha.

----------------------------------------------------
"""

def show_help_manual(main_window):
    """Crea y muestra una ventana Toplevel con el manual de usuario."""
    help_window = tk.Toplevel(main_window)
    help_window.title("Manual de Usuario del Sistema")
    help_window.geometry("700x600")
    help_window.resizable(False, False)
    
    # Frame principal con padding
    main_frame = ttk.Frame(help_window, padding=10)
    main_frame.pack(fill="both", expand=True)

    # Crear un Text widget para mostrar el manual
    text_widget = tk.Text(main_frame, wrap="word", font=("Arial", 10), relief="flat")
    text_widget.pack(side="left", fill="both", expand=True)
    
    # Crear una Scrollbar y asociarla al Text widget
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=text_widget.yview)
    scrollbar.pack(side="right", fill="y")
    text_widget.config(yscrollcommand=scrollbar.set)
    
    # Insertar el texto del manual
    text_widget.insert("1.0", MANUAL_TEXT)
    
    # Hacer que el texto sea de solo lectura
    text_widget.config(state="disabled")
    
    # Botón para cerrar la ventana
    close_button = ttk.Button(help_window, text="Cerrar", command=help_window.destroy, style='Delete.TButton')
    close_button.pack(pady=10)
    
    # Hacer la ventana modal (opcional, pero recomendado)
    help_window.transient(main_window)
    help_window.grab_set()
    main_window.wait_window(help_window)