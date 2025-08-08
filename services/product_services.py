# services/product_service.py
import mysql.connector
from utils.db_connection import conectar_db

def add_product(codigo_producto, nombre, tipo, unidad_medida, fecha_ingreso, fecha_vencimiento, cantidad, id_proveedor):
    db = conectar_db()
    if not db: return (False, "Error de conexión a la base de datos.")
    cursor = db.cursor()
    try:
        # CORRECCIÓN: La columna y el valor de 'precio' han sido eliminados.
        sql = """
            INSERT INTO producto 
            (codigo_producto, nombre, tipo, unidad_medida, fecha_ingreso, fecha_vencimiento, cantidad, id_proveedor) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (codigo_producto, nombre, tipo, unidad_medida, fecha_ingreso, fecha_vencimiento, cantidad, id_proveedor)
        cursor.execute(sql, val)
        db.commit()
        return (True, "Producto registrado correctamente.")
    except mysql.connector.Error as err:
        db.rollback()
        if err.errno == 1062: return (False, f"El código de producto '{codigo_producto}' ya existe.")
        if err.errno == 1452: return (False, f"El proveedor con ID '{id_proveedor}' no existe.")
        return (False, f"Error de base de datos: {err}")
    finally:
        if db.is_connected(): cursor.close(); db.close()

def update_product(product_id, nombre, tipo, unidad_medida, fecha_ingreso, fecha_vencimiento, cantidad, id_proveedor):
    db = conectar_db()
    if not db: return (False, "Error de conexión a la base de datos.")
    cursor = db.cursor()
    try:
        # CORRECCIÓN: La columna y el valor de 'precio' han sido eliminados.
        sql = """
            UPDATE producto SET nombre=%s, tipo=%s, unidad_medida=%s, fecha_ingreso=%s, 
            fecha_vencimiento=%s, cantidad=%s, id_proveedor=%s 
            WHERE id_producto=%s
        """
        val = (nombre, tipo, unidad_medida, fecha_ingreso, fecha_vencimiento, cantidad, id_proveedor, product_id)
        cursor.execute(sql, val)
        db.commit()
        return (True, "Producto actualizado correctamente.")
    except mysql.connector.Error as err:
        db.rollback()
        if err.errno == 1452: return (False, f"El proveedor con ID '{id_proveedor}' no existe.")
        return (False, f"Error de base de datos al actualizar: {err}")
    finally:
        if db.is_connected(): cursor.close(); db.close()

# Las funciones GET y DELETE no necesitan cambios en su lógica.
def get_product_by_code(code):
    db = conectar_db()
    if not db: return None
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM producto WHERE codigo_producto = %s", (code,))
        return cursor.fetchone()
    finally:
        if db.is_connected(): cursor.close(); db.close()

def get_all_products():
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM producto ORDER BY nombre ASC")
        return cursor.fetchall()
    finally:
        if db.is_connected(): cursor.close(); db.close()

def delete_product_by_code(code):
    db = conectar_db()
    if not db: return (False, "Error de conexión a la base de datos.")
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM producto WHERE codigo_producto = %s", (code,))
        db.commit()
        if cursor.rowcount > 0: return (True, f"Producto con código '{code}' eliminado correctamente.")
        else: return (False, f"No se encontró un producto con el código '{code}'.")
    finally:
        if db.is_connected(): cursor.close(); db.close()