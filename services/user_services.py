# services/user_service.py
import mysql.connector
from utils.db_connection import conectar_db # Asegúrate que tu conexión a la DB está en utils/database.py

def add_user(nombre_completo, usuario, contrasena, rol):
    """
    Registra un nuevo usuario en la base de datos.
    Retorna una tupla (éxito, mensaje).
    """
    db = conectar_db()
    if not db:
        return (False, "No se pudo conectar a la base de datos.")
    
    cursor = db.cursor()
    try:
        sql = "INSERT INTO usuario (nombre_completo, usuario, contrasena, rol) VALUES (%s, %s, %s, %s)"
        val = (nombre_completo, usuario, contrasena, rol)
        cursor.execute(sql, val)
        db.commit()
        return (True, f"Usuario '{usuario}' registrado correctamente.")
    except mysql.connector.Error as err:
        db.rollback()
        if err.errno == 1062: # Error de entrada duplicada
            return (False, f"El nombre de usuario '{usuario}' ya existe.")
        return (False, f"Error al registrar usuario: {err}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def get_user_by_username(username):
    """
    Busca un usuario por su nombre de usuario.
    Retorna un diccionario con los datos del usuario o None si no se encuentra.
    """
    db = conectar_db()
    if not db: return None
    
    cursor = db.cursor(dictionary=True)
    try:
        sql = "SELECT id_usuario, nombre_completo, usuario, rol FROM usuario WHERE usuario = %s"
        cursor.execute(sql, (username,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Error al buscar usuario: {err}")
        return None
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def get_all_users():
    """Devuelve una lista de todos los usuarios."""
    db = conectar_db()
    if not db: return []
    
    cursor = db.cursor(dictionary=True)
    try:
        sql = "SELECT id_usuario, nombre_completo, usuario, rol FROM usuario ORDER BY nombre_completo ASC"
        cursor.execute(sql)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error al consultar todos los usuarios: {err}")
        return []
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def update_user(user_id, nombre_completo, rol, nueva_contrasena=None):
    """
    Actualiza los datos de un usuario por su ID.
    Si se provee nueva_contrasena, también la actualiza.
    Retorna una tupla (éxito, mensaje).
    """
    db = conectar_db()
    if not db:
        return (False, "No se pudo conectar a la base de datos.")

    cursor = db.cursor()
    try:
        if nueva_contrasena:
            sql = "UPDATE usuario SET nombre_completo = %s, contrasena = %s, rol = %s WHERE id_usuario = %s"
            val = (nombre_completo, nueva_contrasena, rol, user_id)
        else:
            sql = "UPDATE usuario SET nombre_completo = %s, rol = %s WHERE id_usuario = %s"
            val = (nombre_completo, rol, user_id)
        
        cursor.execute(sql, val)
        db.commit()
        return (True, "Usuario actualizado correctamente.")
    except mysql.connector.Error as err:
        db.rollback()
        return (False, f"Error al actualizar usuario: {err}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def deactivate_user_by_username(username):
    """Cambia el estado de un usuario a 'Inactivo'."""
    db = conectar_db()
    if not db: return (False, "Error de conexión a la base de datos.")
    cursor = db.cursor()
    try:
        sql = "UPDATE usuario SET estado = 'Inactivo' WHERE usuario = %s"
        cursor.execute(sql, (username,))
        db.commit()
        if cursor.rowcount > 0:
            return (True, "Usuario desactivado correctamente.")
        else:
            return (False, "No se encontró el usuario para desactivar.")
    except mysql.connector.Error as err:
        db.rollback()
        return (False, f"Error de base de datos al desactivar: {err}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()