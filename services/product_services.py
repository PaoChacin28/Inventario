# services/product_service.py
import mysql.connector
from utils.db_connection import conectar_db

def add_product(codigo_producto, nombre, tipo):
    """Inserta una definición de producto y devuelve su nuevo ID."""
    db = conectar_db()
    if not db: return (False, "Error de conexión a la base de datos.")
    cursor = db.cursor()
    try:
        sql = "INSERT INTO producto (codigo_producto, nombre, tipo) VALUES (%s, %s, %s)"
        val = (codigo_producto, nombre, tipo)
        cursor.execute(sql, val)
        db.commit()
        return (True, cursor.lastrowid)
    except mysql.connector.Error as err:
        db.rollback()
        if err.errno == 1062: return (False, f"El código de producto '{codigo_producto}' ya existe.")
        return (False, f"Error de base de datos: {err}")
    finally:
        if db.is_connected(): cursor.close(); db.close()

def update_product(product_id, nombre, tipo):
    """Actualiza la definición de un producto (nombre y tipo)."""
    db = conectar_db()
    if not db: return (False, "Error de conexión a la base de datos.")
    cursor = db.cursor()
    try:
        sql = "UPDATE producto SET nombre=%s, tipo=%s WHERE id_producto=%s"
        val = (nombre, tipo, product_id)
        cursor.execute(sql, val)
        db.commit()
        return (True, "Producto actualizado correctamente.")
    except mysql.connector.Error as err:
        db.rollback()
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
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        sql = """
            SELECT p.id_producto, p.codigo_producto, p.nombre, p.tipo,
                   IFNULL((SELECT SUM(l.cantidad_actual) FROM lote l WHERE l.id_producto = p.id_producto AND l.cantidad_actual > 0), 0) AS stock_total
            FROM producto p
            WHERE p.estado = 'Activo'
            ORDER BY p.nombre ASC
        """
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        if db.is_connected(): cursor.close(); db.close()

def deactivate_product_by_code(code):
    """Cambia el estado de un producto a 'Inactivo' (borrado lógico)."""
    db = conectar_db()
    if not db: return (False, "Error de conexión a la base de datos.")
    cursor = db.cursor()
    try:
        sql = "UPDATE producto SET estado = 'Inactivo' WHERE codigo_producto = %s"
        cursor.execute(sql, (code,))
        db.commit()
        if cursor.rowcount > 0:
            return (True, "Producto desactivado correctamente.")
        else:
            return (False, "No se encontró el producto para desactivar.")
    except mysql.connector.Error as err:
        db.rollback()
        return (False, f"Error de base de datos al desactivar: {err}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def get_providers_for_product(product_id):
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        sql = """
            SELECT p.id_proveedor, p.nombre, p.rif, p.telefono, p.direccion 
            FROM proveedor p
            JOIN producto_proveedor pp ON p.id_proveedor = pp.id_proveedor
            WHERE pp.id_producto = %s AND p.estado = 'Activo'
            ORDER BY p.nombre ASC
        """
        cursor.execute(sql, (product_id,))
        return cursor.fetchall()
    finally:
        if db.is_connected(): cursor.close(); db.close()

def associate_provider_to_product(product_id, provider_id):
    db = conectar_db()
    if not db: return (False, "Error de conexión.")
    cursor = db.cursor()
    try:
        sql = "INSERT INTO producto_proveedor (id_producto, id_proveedor) VALUES (%s, %s)"
        val = (product_id, provider_id)
        cursor.execute(sql, val)
        db.commit()
        return (True, "Proveedor asociado correctamente.")
    except mysql.connector.Error as err:
        db.rollback()
        if err.errno == 1062: return (False, "Este proveedor ya está asociado a este producto.")
        return (False, f"Error al asociar proveedor: {err}")
    finally:
        if db.is_connected(): cursor.close(); db.close()

def disassociate_provider_from_product(product_id, provider_id):
    db = conectar_db()
    if not db: return (False, "Error de conexión.")
    cursor = db.cursor()
    try:
        sql = "DELETE FROM producto_proveedor WHERE id_producto = %s AND id_proveedor = %s"
        val = (product_id, provider_id)
        cursor.execute(sql, val)
        db.commit()
        if cursor.rowcount > 0: return (True, "Proveedor desasociado correctamente.")
        else: return (False, "No se encontró la asociación para eliminar.")
    except mysql.connector.Error as err:
        db.rollback()
        return (False, f"Error al desasociar proveedor: {err}")
    finally:
        if db.is_connected(): cursor.close(); db.close()