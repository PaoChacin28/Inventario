from tkinter import ttk

def configure_styles(window):
    """
    Configura todos los estilos de la aplicación usando ttk.Style.
    Esta función debe ser llamada UNA VEZ al crear la ventana principal.
    """
    style = ttk.Style(window)
    style.theme_use('clam')

    # --- Estilos de Frames y Layout ---
    style.configure('MainContent.TFrame', background='#ffffff')
    style.configure('Sidebar.TFrame', background="#924904", borderwidth=0)
    style.configure('TLabelFrame', background='#ffffff', borderwidth=1, relief="groove")


    # --- Estilos de Texto y Etiquetas ---
    style.configure('ContentTitle.TLabel', font=("Arial", 24, "bold"), padding=10, 
                    background='#ffffff', foreground='black')
    style.configure('ContentLabel.TLabel', font=("Arial", 12), 
                    background='#ffffff', foreground='black')
    style.configure('ContentBackground.TLabel', background='#ffffff')


    # --- Estilos de Botones ---
    # Botones de la barra lateral
    style.configure('Sidebar.TButton', font=("Arial", 12, "bold"), padding=10, 
                    background="#913B02", foreground='white', relief='flat', borderwidth=0) 
    style.map('Sidebar.TButton', background=[('active', "#411902")])

    # Botones de los submenús
    style.configure('Submenu.TButton', font=("Arial", 10), padding=8, 
                    background="#411902", foreground='white', relief='flat', borderwidth=0)
    style.map('Submenu.TButton', background=[('active', "#180901")])
    
    # Botón de Búsqueda (Azul)
    style.configure('Search.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#411902", foreground='white', relief='flat', borderwidth=0)
    style.map('Search.TButton', background=[('active', "#411902")])

    # Botón de Acción / Guardar (Verde)
    style.configure('Action.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#411902", foreground='white', relief='flat', borderwidth=0)
    style.map('Action.TButton', background=[('active', "#411902")])
    
    # Botón de Énfasis / Acento (para acciones importantes como registrar movimiento)
    style.configure('Accent.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#411902", foreground='white', relief='flat', borderwidth=0)
    style.map('Accent.TButton', background=[('active', "#411902")])

    # Botón de Eliminar (Rojo)
    style.configure('Delete.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#411902", foreground='white', relief='flat', borderwidth=0)
    style.map('Delete.TButton', background=[('active', "#411902")])


    # --- Estilos de otros Widgets ---
    style.configure('Treeview', rowheight=25, font=('Arial', 10))
    style.configure('Treeview.Heading', font=('Arial', 11, 'bold'))