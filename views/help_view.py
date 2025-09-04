# views/help_view.py

import tkinter as tk
from tkinter import ttk
import controllers.help_controller as help_controller

# --- TEXTO PARA LA VENTANA EMERGENTE DE 'AYUDA' ---
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



# --- TEXTO PARA LA SECCIÓN 'MANUAL DE USUARIO' ---
FULL_MANUAL_TEXT = """
Sistema de Control de Inventario para Frigorífico JPG, F.P.


-----------------------------------------------------------------------------------------------------------------
1. INTRODUCCIÓN
-----------------------------------------------------------------------------------------------------------------
Bienvenido al Manual de Usuario del Sistema de Control de Inventario del Frigorífico JPG, F.P. Este documento ha sido diseñado para guiarlo a través de todas las funcionalidades de la aplicación, desde la instalación y el primer acceso hasta la ejecución de las operaciones diarias de gestión de inventario.
El objetivo de este sistema es proporcionar una herramienta robusta, intuitiva y segura para la trazabilidad completa de los productos, optimizando el control del stock y facilitando la toma de decisiones.

-----------------------------------------------------------------------------------------------------------------
2. REQUERIMIENTOS DEL SISTEMA
-----------------------------------------------------------------------------------------------------------------
Para garantizar un funcionamiento estable, seguro y con soporte completo, el equipo debe cumplir con las siguientes especificaciones.

2.1. Requerimientos Mínimos Soportados
- Sistema Operativo: Windows 10.
- Procesador: Intel Core i3 o AMD Ryzen 3.
- Memoria RAM: 4 GB.
- Espacio en Disco: 1 GB de espacio libre.
- Software Adicional: Servidor de base de datos MySQL (v8.0+) instalado y en ejecución.

2.2. Requerimientos Recomendados
- Sistema Operativo: Windows 11.
- Procesador: Intel Core i5 o AMD Ryzen 5.
- Memoria RAM: 8 GB o más.
- Espacio en Disco: Disco de Estado Sólido (SSD).

---
NOTA IMPORTANTE SOBRE SISTEMAS OPERATIVOS ANTIGUOS
----------------------------------------------------
El uso de la aplicación en sistemas operativos como Windows 7, Windows 8 o versiones antiguas de Windows 10, no es recomendable.

Técnicamente, la aplicación podría iniciarse en algunos de estos sistemas, pero se hace bajo el propio riesgo del usuario. El desarrollador no puede garantizar su estabilidad, la correcta apariencia visual, y, lo más importante, la seguridad de los datos en un sistema operativo que ya no recibe actualizaciones de seguridad. Se recomienda encarecidamente utilizar un sistema operativo moderno y actualizado.
---
-----------------------------------------------------------------------------------------------------------------
3. INSTALACIÓN Y ACCESO
-----------------------------------------------------------------------------------------------------------------
La puesta en marcha del sistema consta de dos pasos sencillos: la configuración de la base de datos y el acceso a la aplicación.

3.1. Configuración de la Base de Datos (Paso único)
-Asegúrese de tener un servidor MySQL instalado y funcionando.
-Utilizando un cliente de base de datos, ejecute el archivo `inventario.sql` proporcionado. Este script creará la base de datos, las tablas y los datos iniciales necesarios.

3.2. Acceso a la Aplicación
El sistema se distribuye como una carpeta que contiene un archivo ejecutable.

-Copie la carpeta completa del sistema a una ubicación permanente en su computador (ej. C:\\Aplicaciones\\Sistema de Inventario).
-Para iniciar, simplemente haga doble clic en el archivo ejecutable (.exe) que se encuentra dentro de la carpeta(\Sistema de Inventario\dist).
-(Recomendado) Puede crear un acceso directo a este archivo .exe en su escritorio para un acceso más rápido y cómodo.

NO es necesario ejecutar comandos en la terminal ni tener Python instalado en el equipo del usuario final.

-----------------------------------------------------------------------------------------------------------------
4. PRIMEROS PASOS: INICIO DE SESIÓN
-----------------------------------------------------------------------------------------------------------------
Al abrir la aplicación, verá el formulario de Inicio de Sesión.
- Usuario: Ingrese su nombre de usuario (ej. `admin`).
- Contraseña: Ingrese su contraseña.
Haga clic en el botón "Iniciar Sesión" o presione la tecla Enter para acceder.

-----------------------------------------------------------------------------------------------------------------
5. DESCRIPCIÓN DE LOS MÓDULOS DEL SISTEMA
-----------------------------------------------------------------------------------------------------------------
El menú lateral contiene todos los módulos de la aplicación.

5.1. Módulo de Productos
Es el catálogo central. Muestra una lista de todos los productos activos con su stock total.
•	Añadir Producto: Abre un formulario para definir un nuevo producto (código, nombre, tipo) y asociarle uno o más proveedores.
•	Editar Seleccionado: Abre un formulario de gestión completo para modificar el nombre, el tipo y la lista de proveedores asociados a un producto existente.
•	Desincorporar Seleccionado: Oculta un producto de las listas activas, pero mantiene su historial.
•	Ver Lotes: Muestra una tabla con todas las entregas (lotes) del producto seleccionado, incluyendo su stock individual.
•	Ver Proveedores: Muestra una lista de los proveedores asociados a un producto.

5.2. Módulo de Movimientos
Es el centro de las operaciones de inventario. La vista principal es el historial de todos los movimientos.
•	Registrar Nuevo Movimiento: Abre el formulario dinámico para:
•	Entrada: Define un nuevo LOTE (tag, cantidad, etc.) para un producto.
•	Salida: Descuenta stock de un LOTE existente.
•	Ajuste: Establece un nuevo valor de stock para un LOTE (usado para corregir conteos o registrar mermas).

5.3. Módulos de Administración (Solo para rol "Administrador")
•	Usuarios: Permite gestionar las cuentas de usuario (Añadir, Editar, Desincorporar). Requiere que las contraseñas cumplan un formato de seguridad.
•	Proveedores: Permite gestionar el catálogo de proveedores (Añadir, Editar, Desincorporar).
•	Reportes: Genera informes dinámicos y exportables a PDF. El usuario genera el reporte en pantalla y luego puede exportar, lo que abre una vista previa en su lector de PDF predeterminado.
•	Manual de Usuario: Muestra este documento completo dentro de la aplicación, con una opción para exportarlo a PDF.

5.4. Módulo de Ayuda
Muestra una ventana emergente con una guía rápida sobre el funcionamiento de los módulos principales. 

5.5. Cerrar Sesión
Finaliza la sesión actual y devuelve a la pantalla de Inicio de Sesión, listo para que otro usuario ingrese.

-----------------------------------------------------------------------------------------------------------------
6. MENSAJES DE ERROR COMUNES Y SU SIGNIFICADO
-----------------------------------------------------------------------------------------------------------------
- "Campos Incompletos": Intentó guardar un formulario sin rellenar todos los campos obligatorios.
- "Formato Incorrecto": Un campo (RIF, Código de Producto) no cumple con el formato esperado.
- "Contraseña Inválida": La contraseña no cumple los requisitos de seguridad.
- "Stock Insuficiente": Intentó registrar una salida por una cantidad mayor a la disponible en el lote.
- "El Tag / Lote ya existe": El identificador de un nuevo lote ya está en uso. Debe ser único.
- "La consulta no arrojo resultados": El reporte que se esta intentando generar esta vacio por lo tanto no hay resultados en la tabla 


-----------------------------------------------------------------------------------------------------------------
7. GLOSARIO DE TÉRMINOS
-----------------------------------------------------------------------------------------------------------------
- Lote: Una entrega específica de un producto. Es la unidad básica del inventario para la trazabilidad.
- Tag de Lote: El código único y obligatorio que se asigna a un lote para su identificación.
- Movimiento de Ajuste: Operación que establece un nuevo valor de stock para un lote.

-----------------------------------------------------------------------------------------------------------------
8. SOPORTE Y CONTACTO
-----------------------------------------------------------------------------------------------------------------
Para cualquier duda, contacte al administrador del sistema.
- Nombre: Paola Chacin
- Correo: pao28chacin@gmail.com
- Teléfono: 0424-8321324 / 0412-0867938
"""

def show_full_manual_in_frame(parent_frame):
    """(NUEVA) Dibuja el manual largo en el frame principal."""
    from views.main_view import _clear_frame
    _clear_frame(parent_frame)

    top_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    top_frame.pack(side='top', fill='x', padx=10, pady=10)

    bottom_frame = ttk.Frame(parent_frame, style='MainContent.TFrame')
    bottom_frame.pack(side='bottom', fill='x', padx=10, pady=10)
    
    container = ttk.Frame(parent_frame, style='MainContent.TFrame')
    container.pack(fill="both", expand=True, padx=10)

    ttk.Label(top_frame, text="Manual de Usuario del Sistema", style='ContentTitle.TLabel').pack(pady=10)

    text_widget = tk.Text(container, wrap="word", font=("Arial", 11), relief="flat", padx=10, pady=10, bg="white")
    vsb = ttk.Scrollbar(container, orient="vertical", command=text_widget.yview)
    text_widget.config(yscrollcommand=vsb.set)
    
    vsb.pack(side="right", fill="y")
    text_widget.pack(side="left", fill="both", expand=True)
    
    text_widget.insert("1.0", FULL_MANUAL_TEXT)
    text_widget.config(state="disabled")
    
    def export_action():
        help_controller.handle_export_manual_as_pdf(FULL_MANUAL_TEXT)
    
    ttk.Button(bottom_frame, text="Exportar en PDF", command=export_action, style='Action.TButton').pack(side='right')

    #def preview_action():
     #   help_controller.handle_preview_manual(FULL_MANUAL_TEXT)
    
    ##  help_controller.handle_save_manual(FULL_MANUAL_TEXT)
    
    #save_button = ttk.Button(bottom_frame, text="Guardar PDF", command=save_action, style='Search.TButton')
    #save_button.pack(side='right')
    #preview_button = ttk.Button(bottom_frame, text="Visualizar PDF", command=preview_action, style='Action.TButton')
    #preview_button.pack(side='right', padx=(0, 10))

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