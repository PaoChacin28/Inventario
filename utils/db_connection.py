# db_connection.py
import mysql.connector
from tkinter import messagebox

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "pao2606",
    "database": "inventario"
}

def conectar_db():
    """Establece una conexión con la base de datos MySQL."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {err}")
        return None