# main.py
import sys
import os
from views import login_view

# Añadir el directorio raíz del proyecto al path de Python
# Esto asegura que las importaciones (ej. from views import...) funcionen correctamente
# sin importar desde dónde se ejecute el script.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    # Inicia la aplicación creando y mostrando la ventana de login
    login_view.create_login_window()