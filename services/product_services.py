# services/product_service.py
import mysql.connector
from utils.db_connection import conectar_db

def add_product(codigo_producto, nombre, tipo, id_proveedor):
    """Inserta una definición de producto, sin stock."""
    db = conectar_db()
    if not db: return (False, "Error de conexión a la base de datos.")
    cursor = db.cursor()
    try:
        sql = "INSERT INTO producto (codigo_producto, nombre, tipo, id_proveedor) VALUES (%s, %s, %s, %s)"
        val = (codigo_producto, nombre, tipo, id_proveedor)
        cursor.execute(sql, val)
        db.commit()
        return (True, "Producto definido correctamente.")
    except mysql.connector.Error as err:
        db.rollback()
        if err.errno == 1062: return (False, f"El código de producto '{codigo_producto}' ya existe.")
        if err.errno == 1452: return (False, f"El proveedor con ID '{id_proveedor}' no existe.")
        return (False, f"Error de base de datos: {err}")
    finally:
        if db.is_connected(): cursor.close(); db.close()

def update_product(product_id, nombre, tipo, id_proveedor):
    """Actualiza la definición de un producto."""
    db = conectar_db()
    if not db: return (False, "Error de conexión a la base de datos.")
    cursor = db.cursor()
    try:
        sql = "UPDATE producto SET nombre=%s, tipo=%s, id_proveedor=%s WHERE id_producto=%s"
        val = (nombre, tipo, id_proveedor, product_id)
        cursor.execute(sql, val)
        db.commit()
        return (True, "Producto actualizado correctamente.")
    except mysql.connector.Error as err:
        db.rollback()
        if err.errno == 1452: return (False, f"El proveedor con ID '{id_proveedor}' no existe.")
        return (False, f"Error de base de datos al actualizar: {err}")
    finally:
        if db.is_connected(): cursor.close(); db.close()

def get_product_by_code(code):
    db = conectar_db()
    if not db: return None
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM producto WHERE codigo_producto = %s", (code,))
        return cursor.fetchone()
    finally:
        if db.is_connected(): cursor.close(); db.close()

def get_all_products_with_stock():
    """
    Devuelve todos los productos y calcula su stock total sumando las cantidades de sus lotes activos.
    CORREGIDO: Usa IFNULL para manejar productos sin stock.
    """
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        # --- CORRECCIÓN CLAVE ---
        # Usamos IFNULL(SUM(...), 0) para que si un producto no tiene lotes (SUM da NULL),
        # se muestre un stock de 0 en lugar de nada.
        sql = """
            SELECT 
                p.id_producto, p.codigo_producto, p.nombre, p.tipo,
                prov.nombre AS nombre_proveedor,
                IFNULL((SELECT SUM(l.cantidad_actual) FROM lote l WHERE l.id_producto = p.id_producto), 0) AS stock_total
            FROM producto p
            LEFT JOIN proveedor prov ON p.id_proveedor = prov.id_proveedor
            ORDER BY p.nombre ASC
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error en servicio al obtener productos con stock: {err}")
        return []
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def delete_product_by_code(code):
    db = conectar_db()
    if not db: return (False, "Error de conexión a la base de datos.")
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM producto WHERE codigo_producto = %s", (code,))
        db.commit()
        if cursor.rowcount > 0: return (True, f"Producto con código '{code}' eliminado.")
        else: return (False, f"No se encontró producto con código '{code}'.")
    finally:
        if db.is_connected(): cursor.close(); db.close()