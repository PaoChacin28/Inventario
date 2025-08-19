# services/provider_service.py
import mysql.connector
from utils.db_connection import conectar_db # Asegúrate que tu conexión a la DB está en utils/database.py

def add_provider(nombre, rif, telefono, direccion):
    """
    Agrega un nuevo proveedor a la base de datos.
    Retorna (True, "Mensaje de éxito") o (False, "Mensaje de error").
    """
    db = conectar_db()
    if not db:
        return (False, "No se pudo conectar a la base de datos.")
    
    cursor = db.cursor()
    try:
        sql = "INSERT INTO proveedor (nombre, rif, telefono, direccion) VALUES (%s, %s, %s, %s)"
        # Guarda None en la base de datos si las cadenas de texto opcionales están vacías
        val = (nombre, rif, telefono or None, direccion or None)
        cursor.execute(sql, val)
        db.commit()
        return (True, "Proveedor registrado correctamente.")
    except mysql.connector.Error as err:
        db.rollback()
        if err.errno == 1062: # Error de RIF duplicado
            return (False, f"El RIF '{rif}' ya está registrado. Verifique los datos.")
        return (False, f"Error al registrar proveedor: {err}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def get_provider_by_rif(rif):
    """
    Busca un proveedor por su RIF.
    Retorna un diccionario con los datos o None si no se encuentra.
    """
    db = conectar_db()
    if not db: return None
    
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM proveedor WHERE rif = %s", (rif,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Error al buscar proveedor por RIF: {err}")
        return None
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def get_all_providers():
    """Devuelve una lista de todos los proveedores."""
    db = conectar_db()
    if not db: return []
        
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM proveedor ORDER BY nombre ASC")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error al obtener todos los proveedores: {err}")
        return []
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def update_provider(provider_id, nombre, rif, telefono, direccion):
    """
    Actualiza los datos de un proveedor existente por su ID.
    Retorna (True, "Mensaje de éxito") o (False, "Mensaje de error").
    """
    db = conectar_db()
    if not db:
        return (False, "No se pudo conectar a la base de datos.")
        
    cursor = db.cursor()
    try:
        sql = "UPDATE proveedor SET nombre=%s, rif=%s, telefono=%s, direccion=%s WHERE id_proveedor=%s"
        val = (nombre, rif, telefono or None, direccion or None, provider_id)
        cursor.execute(sql, val)
        db.commit()
        return (True, "Proveedor actualizado correctamente.")
    except mysql.connector.Error as err:
        db.rollback()
        if err.errno == 1062:
            return (False, f"El RIF '{rif}' ya pertenece a otro proveedor.")
        return (False, f"Error al actualizar el proveedor: {err}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def get_providers_for_selection():
    """Obtiene una lista simple de proveedores (ID y nombre) para usar en un combobox."""
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_proveedor, nombre FROM proveedor ORDER BY nombre ASC")
        return cursor.fetchall()
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def deactivate_provider_by_rif(rif):
    """Cambia el estado de un proveedor a 'Inactivo'."""
    db = conectar_db()
    if not db: return (False, "Error de conexión a la base de datos.")
    cursor = db.cursor()
    try:
        sql = "UPDATE proveedor SET estado = 'Inactivo' WHERE rif = %s"
        cursor.execute(sql, (rif,))
        db.commit()
        if cursor.rowcount > 0:
            return (True, "Proveedor desactivado correctamente.")
        else:
            return (False, "No se encontró el proveedor para desactivar.")
    except mysql.connector.Error as err:
        db.rollback()
        return (False, f"Error de base de datos al desactivar: {err}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()