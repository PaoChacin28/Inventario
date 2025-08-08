# services/report_service.py
import mysql.connector
from datetime import datetime, timedelta
from utils.db_connection import conectar_db # Asegúrate que tu conexión a la DB está en utils/database.py

def get_low_stock_report_data(threshold=10):
    """
    Obtiene los productos cuya cantidad es menor o igual a un umbral.
    Retorna una lista de diccionarios, o None en caso de error de conexión.
    """
    db = conectar_db()
    if not db: return None
    
    cursor = db.cursor(dictionary=True)
    try:
        sql = """
            SELECT id_producto, codigo_producto, nombre, tipo, cantidad, fecha_vencimiento
            FROM producto WHERE cantidad <= %s ORDER BY cantidad ASC
        """
        cursor.execute(sql, (threshold,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error en el servicio de reporte (stock bajo): {err}")
        return [] # Retorna lista vacía en caso de error de consulta
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def get_expiring_soon_report_data(days_ahead=30):
    """
    Obtiene los productos que vencen en los próximos N días.
    Retorna una lista de diccionarios, o None en caso de error de conexión.
    """
    db = conectar_db()
    if not db: return None
    
    cursor = db.cursor(dictionary=True)
    try:
        fecha_limite = datetime.now().date() + timedelta(days=days_ahead)
        sql = """
            SELECT id_producto, codigo_producto, nombre, tipo, cantidad, fecha_vencimiento
            FROM producto WHERE fecha_vencimiento IS NOT NULL AND fecha_vencimiento <= %s 
            ORDER BY fecha_vencimiento ASC
        """
        cursor.execute(sql, (fecha_limite,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error en el servicio de reporte (por vencer): {err}")
        return [] # Retorna lista vacía en caso de error de consulta
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            
def log_report_generation(report_type, user_id):
    """
    Inserta un registro en la tabla 'reporte' para auditar la generación.
    Retorna True si fue exitoso, False en caso contrario.
    """
    db = conectar_db()
    if not db: return False

    cursor = db.cursor()
    try:
        sql = "INSERT INTO reporte (fecha_generacion, tipo_reporte, id_usuario) VALUES (%s, %s, %s)"
        val = (datetime.now(), report_type, user_id) # Usar datetime completo
        cursor.execute(sql, val)
        db.commit()
        return True
    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error al registrar la generación de reporte: {err}")
        return False
    finally:
        if db.is_connected():
            cursor.close()
            db.close()