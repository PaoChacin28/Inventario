# utils/styles.py
from tkinter import ttk

def configure_styles(window):
    """
    Configura todos los estilos de la aplicación, incluyendo los estilos personalizados para formularios.
    """
    style = ttk.Style(window)
    style.theme_use('clam')

    # --- Estilos de Frames y Layout ---
    style.configure('MainContent.TFrame', background='#ffffff')
    style.configure('Sidebar.TFrame', background="#924904", borderwidth=0)
    
    # --- Estilos de Texto y Etiquetas ---
    style.configure('ContentTitle.TLabel', font=("Arial", 24, "bold"), padding=10, 
                    background='#ffffff', foreground='black')
    style.configure('ContentLabel.TLabel', font=("Arial", 10), 
                    background='#ffffff', foreground='black')

    # --- Estilos de Botones (Tus colores originales) ---
    style.configure('Sidebar.TButton', font=("Arial", 12, "bold"), padding=10, 
                    background="#913B02", foreground='white', relief='flat', borderwidth=0) 
    style.map('Sidebar.TButton', background=[('active', "#411902")])

    style.configure('Search.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#411902", foreground='white', relief='flat', borderwidth=0)
    style.map('Search.TButton', background=[('active', "#200D01")])

    style.configure('Action.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#411902", foreground='white', relief='flat', borderwidth=0)
    style.map('Action.TButton', background=[('active', "#200D01")])
    
    style.configure('Accent.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#411902", foreground='white', relief='flat', borderwidth=0)
    style.map('Accent.TButton', background=[('active', "#200D01")])

    style.configure('Delete.TButton', font=("Arial", 10, "bold"), padding=8, 
                    background="#411902", foreground='white', relief='flat', borderwidth=0)
    style.map('Delete.TButton', background=[('active', "#200D01")])

    # --- Estilos de otros Widgets ---
    style.configure('Treeview', rowheight=25, font=('Arial', 10))
    style.configure('Treeview.Heading', font=('Arial', 11, 'bold'))
    
    # --- ESTILOS NUEVOS Y CORREGIDOS ---
    
    # Estilo para LabelFrame con título en negrita (el que causaba el error)
    # Define el estilo para el marco del LabelFrame
    style.configure('Bold.TLabelFrame', background='#ffffff', borderwidth=1, relief="groove")
    # Define el estilo para la ETIQUETA (el texto) del LabelFrame
    style.configure('Bold.TLabelFrame.Label', 
                    font=("Arial", 11, "bold"),
                    background='#ffffff',
                    foreground='black')

    # Estilo para un botón de acción más pequeño
    style.configure('Small.Action.TButton',
                    font=("Arial", 9),
                    padding=4,
                    background="#411902", foreground='white', relief='flat')
    style.map('Small.Action.TButton', background=[('active', "#200D01")])

    # Estilo para el botón de eliminación "X" (muy pequeño)
    style.configure('Small.Delete.TButton',
                    font=("Arial", 8, "bold"),
                    padding=(4, 2),
                    background="#913B02", foreground='white', relief='flat')
    style.map('Small.Delete.TButton', background=[('active', "#411902")])