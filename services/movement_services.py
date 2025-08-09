# services/movement_service.py
import mysql.connector
from datetime import datetime
from utils.db_connection import conectar_db

def get_products_for_selection():
    """Obtiene una lista simple de productos para usar en un combobox."""
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_producto, nombre FROM producto ORDER BY nombre ASC")
        return cursor.fetchall()
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def get_active_lots_for_selection():
    """Obtiene los lotes que aún tienen stock para el combobox de salidas y ajustes."""
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        sql = """
            SELECT l.id_lote, l.tag_lote, l.cantidad_actual, l.unidad_medida, p.nombre AS nombre_producto
            FROM lote l
            JOIN producto p ON l.id_producto = p.id_producto
            WHERE l.cantidad_actual > 0
            ORDER BY l.fecha_ingreso DESC
        """
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def get_lots_for_product(product_id):
    """Obtiene todos los lotes (activos y agotados) para un producto específico."""
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        sql = """
            SELECT tag_lote, cantidad_inicial, cantidad_actual, unidad_medida, 
                   fecha_ingreso, fecha_vencimiento
            FROM lote
            WHERE id_producto = %s
            ORDER BY fecha_ingreso DESC
        """
        cursor.execute(sql, (product_id,))
        return cursor.fetchall()
    finally:
        if db.is_connected(): cursor.close(); db.close()

def register_entry_movement(product_id, tag_lote, cantidad, unidad, fecha_vencimiento, user_id):
    """Crea un nuevo lote y registra el movimiento de entrada en una transacción."""
    db = conectar_db()
    if not db: return (False, "Error de conexión a la base de datos.")
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id_lote FROM lote WHERE tag_lote = %s", (tag_lote,))
        if cursor.fetchone():
            return (False, "El Tag / Lote ya existe. Debe ser único.")
            
        sql_lote = """
            INSERT INTO lote (tag_lote, cantidad_inicial, cantidad_actual, unidad_medida, fecha_ingreso, fecha_vencimiento, id_producto)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        val_lote = (tag_lote, cantidad, cantidad, unidad, datetime.now().date(), fecha_vencimiento, product_id)
        cursor.execute(sql_lote, val_lote)
        new_lote_id = cursor.lastrowid

        sql_mov = "INSERT INTO movimiento (tipo, cantidad, fecha, id_producto, id_usuario, id_lote) VALUES ('Entrada', %s, %s, %s, %s, %s)"
        val_mov = (cantidad, datetime.now(), product_id, user_id, new_lote_id)
        cursor.execute(sql_mov, val_mov)
        
        db.commit()
        return (True, "Lote y movimiento de entrada registrados correctamente.")
    except mysql.connector.Error as err:
        db.rollback()
        return (False, f"Error en la transacción: {err}")
    finally:
        if db.is_connected(): cursor.close(); db.close()

def register_exit_movement(id_lote, cantidad_salida, user_id):
    """Descuenta de un lote existente y registra la salida en una transacción."""
    db = conectar_db()
    if not db: return (False, "Error de conexión a la base de datos.")
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM lote WHERE id_lote = %s FOR UPDATE", (id_lote,))
        lote = cursor.fetchone()
        if not lote: return (False, "El lote seleccionado no existe.")
        
        if lote['cantidad_actual'] < cantidad_salida:
            return (False, f"Stock insuficiente en el lote '{lote['tag_lote']}'. Disponible: {lote['cantidad_actual']}.")
            
        nueva_cantidad = lote['cantidad_actual'] - cantidad_salida
        cursor.execute("UPDATE lote SET cantidad_actual = %s WHERE id_lote = %s", (nueva_cantidad, id_lote))
        
        sql_mov = "INSERT INTO movimiento (tipo, cantidad, fecha, id_producto, id_usuario, id_lote) VALUES ('Salida', %s, %s, %s, %s, %s)"
        val_mov = (cantidad_salida, datetime.now(), lote['id_producto'], user_id, id_lote)
        cursor.execute(sql_mov, val_mov)
        
        db.commit()
        return (True, "Movimiento de salida registrado y stock del lote actualizado.")
    except mysql.connector.Error as err:
        db.rollback()
        return (False, f"Error en la transacción: {err}")
    finally:
        if db.is_connected(): cursor.close(); db.close()

def register_adjustment_movement(id_lote, cantidad_ajuste, user_id, descripcion):
    """Ajusta el stock de un lote y registra el movimiento."""
    db = conectar_db()
    if not db: return (False, "Error de conexión a la base de datos.")
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM lote WHERE id_lote = %s FOR UPDATE", (id_lote,))
        lote = cursor.fetchone()
        if not lote: return (False, "El lote seleccionado no existe.")
        
        nueva_cantidad = lote['cantidad_actual'] + cantidad_ajuste
        if nueva_cantidad < 0:
            return (False, f"El ajuste resultaría en stock negativo para el lote '{lote['tag_lote']}'.")
            
        cursor.execute("UPDATE lote SET cantidad_actual = %s WHERE id_lote = %s", (nueva_cantidad, id_lote))
        
        sql_mov = """INSERT INTO movimiento 
                   (tipo, cantidad, descripcion, fecha, id_producto, id_usuario, id_lote) 
                   VALUES ('Ajuste', %s, %s, %s, %s, %s, %s)"""
        val_mov = (cantidad_ajuste, descripcion, datetime.now(), lote['id_producto'], user_id, id_lote)
        cursor.execute(sql_mov, val_mov)
        
        db.commit()
        return (True, "Ajuste de inventario registrado y stock del lote actualizado.")
    except mysql.connector.Error as err:
        db.rollback()
        return (False, f"Error en la transacción: {err}")
    finally:
        if db.is_connected(): cursor.close(); db.close()

def get_all_movements_with_details():
    """Obtiene todos los movimientos, incluyendo el tag del lote y la descripción."""
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        sql = """
            SELECT m.id_movimiento, m.fecha, m.tipo, m.cantidad, m.descripcion,
                   p.nombre AS producto_nombre, u.nombre_completo AS usuario_nombre,
                   l.tag_lote
            FROM movimiento m
            JOIN producto p ON m.id_producto = p.id_producto
            JOIN usuario u ON m.id_usuario = u.id_usuario
            LEFT JOIN lote l ON m.id_lote = l.id_lote
            ORDER BY m.fecha DESC, m.id_movimiento DESC
        """
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        if db.is_connected(): cursor.close(); db.close()