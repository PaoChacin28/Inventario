# services/movement_service.py
import mysql.connector
from datetime import datetime
from utils.db_connection import conectar_db

def get_products_for_selection():
    """Obtiene una lista simple de productos (ID y nombre) para usar en un combobox."""
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_producto, codigo_producto, nombre FROM producto ORDER BY nombre ASC")
        return cursor.fetchall()
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def register_inventory_movement(product_id, movement_type, quantity, user_id):
    """
    Registra un movimiento y actualiza el stock del producto en una única transacción.
    """
    db = conectar_db()
    if not db: return (False, "Error de conexión a la base de datos.")
    
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT cantidad FROM producto WHERE id_producto = %s FOR UPDATE", (product_id,))
        product = cursor.fetchone()
        
        if not product:
            return (False, "El producto seleccionado ya no existe.")
            
        current_stock = product['cantidad']

        if movement_type == 'Salida':
            if current_stock < quantity:
                return (False, f"No hay stock suficiente. Stock actual: {current_stock}.")
            new_stock = current_stock - quantity
        elif movement_type == 'Entrada':
            new_stock = current_stock + quantity
        else:
            return (False, "Tipo de movimiento no válido.")

        cursor.execute("UPDATE producto SET cantidad = %s WHERE id_producto = %s", (new_stock, product_id))

        # --- CORRECCIÓN APLICADA ---
        # Usamos los nombres de columna EXACTOS de tu SQL: `tipo` y `fecha`.
        sql_insert = "INSERT INTO movimiento (tipo, cantidad, fecha, id_producto, id_usuario) VALUES (%s, %s, %s, %s, %s)"
        val_insert = (movement_type, quantity, datetime.now().date(), product_id, user_id)
        cursor.execute(sql_insert, val_insert)

        db.commit()
        return (True, "Movimiento registrado y stock actualizado correctamente.")

    except mysql.connector.Error as err:
        db.rollback()
        return (False, f"Error de base de datos durante la transacción: {err}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def get_all_movements_with_details():
    """
    Obtiene todos los movimientos con los nombres del producto y usuario asociados.
    """
    db = conectar_db()
    if not db: return []
    
    cursor = db.cursor(dictionary=True)
    try:
        # --- CORRECCIÓN APLICADA AQUÍ TAMBIÉN ---
        # Usamos `m.tipo` y `m.fecha` para que coincida con tu SQL.
        sql = """
            SELECT 
                m.id_movimiento,
                m.fecha,
                m.tipo,
                m.cantidad,
                p.nombre AS producto_nombre,
                u.nombre_completo AS usuario_nombre
            FROM movimiento m
            JOIN producto p ON m.id_producto = p.id_producto
            JOIN usuario u ON m.id_usuario = u.id_usuario
            ORDER BY m.fecha DESC, m.id_movimiento DESC
        """
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        if db.is_connected():
            cursor.close()
            db.close()