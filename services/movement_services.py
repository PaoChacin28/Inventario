# services/movement_service.py
import mysql.connector
from datetime import datetime
from utils.db_connection import conectar_db
from decimal import Decimal

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
    """Descuenta de un lote existente, con conversión de tipos corregida."""
    db = conectar_db()
    if not db: return (False, "Error de conexión.")
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM lote WHERE id_lote = %s FOR UPDATE", (id_lote,))
        lote = cursor.fetchone()
        if not lote: return (False, "El lote seleccionado no existe.")
        
        # --- CORRECCIÓN DE TIPO ---
        cantidad_actual_decimal = lote['cantidad_actual']
        cantidad_salida_decimal = Decimal(str(cantidad_salida))

        if cantidad_actual_decimal < cantidad_salida_decimal:
            return (False, f"Stock insuficiente. Disponible: {cantidad_actual_decimal}.")
            
        nueva_cantidad = cantidad_actual_decimal - cantidad_salida_decimal
        cursor.execute("UPDATE lote SET cantidad_actual = %s WHERE id_lote = %s", (nueva_cantidad, id_lote))
        
        sql_mov = "INSERT INTO movimiento (tipo, cantidad, fecha, id_producto, id_usuario, id_lote) VALUES ('Salida', %s, %s, %s, %s, %s)"
        val_mov = (cantidad_salida_decimal, datetime.now(), lote['id_producto'], user_id, id_lote)
        cursor.execute(sql_mov, val_mov)
        
        db.commit()
        return (True, "Movimiento de salida registrado.")
        
    except mysql.connector.Error as err:
        db.rollback()
        return (False, f"Error en la transacción: {err}")
    finally:
        if db.is_connected(): cursor.close(); db.close()

def register_adjustment_movement(id_lote, nueva_cantidad_ajuste, user_id, descripcion):
    """
    Ajusta el stock de un lote a un valor específico (asignación directa).
    El stock final no puede ser negativo.
    """
    db = conectar_db()
    if not db: return (False, "Error de conexión.")
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM lote WHERE id_lote = %s FOR UPDATE", (id_lote,))
        lote = cursor.fetchone()
        if not lote: return (False, "El lote seleccionado no existe.")
        
        # --- CAMBIO FUNDAMENTAL EN LA LÓGICA DE AJUSTE ---
        
        # 1. Convertimos a Decimal para precisión
        cantidad_actual_decimal = lote['cantidad_actual']
        nueva_cantidad_decimal = Decimal(str(nueva_cantidad_ajuste))

        # 2. Validamos que el nuevo stock no sea negativo
        if nueva_cantidad_decimal < 0:
            # Esta es una doble validación, por si acaso la del controlador falla.
            return (False, "El valor de ajuste no puede ser negativo.")
            
        # 3. Calculamos la DIFERENCIA para guardarla en la tabla de movimientos (para auditoría)
        #    Ejemplo: Si stock era 3 y el ajuste es 10, el movimiento fue de +7.
        #    Ejemplo: Si stock era 15 y el ajuste es 5, el movimiento fue de -10.
        cantidad_para_movimiento = nueva_cantidad_decimal - cantidad_actual_decimal
        
        # 4. Actualizamos el lote con el nuevo valor absoluto
        cursor.execute("UPDATE lote SET cantidad_actual = %s WHERE id_lote = %s", (nueva_cantidad_decimal, id_lote))
        
        # 5. Insertamos el movimiento con la DIFERENCIA calculada
        sql_mov = """INSERT INTO movimiento (tipo, cantidad, descripcion, fecha, id_producto, id_usuario, id_lote) 
                   VALUES ('Ajuste', %s, %s, %s, %s, %s, %s)"""
        val_mov = (cantidad_para_movimiento, descripcion, datetime.now(), lote['id_producto'], user_id, id_lote)
        cursor.execute(sql_mov, val_mov)
        
        db.commit()
        return (True, "Ajuste de inventario registrado correctamente.")
        
    except mysql.connector.Error as err:
        db.rollback()
        return (False, f"Error en la transacción: {err}")
    finally:
        if db.is_connected(): cursor.close(); db.close()
        
def get_all_movements_with_details():
    """
    Obtiene todos los movimientos, incluyendo el tag del lote y la descripción.
    CORREGIDO: Usa LEFT JOIN en todas las tablas para garantizar que no se omitan movimientos.
    """
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        # --- CORRECCIÓN CLAVE EN LA CONSULTA SQL ---
        sql = """
            SELECT 
                m.id_movimiento, m.fecha, m.tipo, m.cantidad, m.descripcion,
                p.nombre AS producto_nombre, 
                u.nombre_completo AS usuario_nombre,
                l.tag_lote
            FROM movimiento m
            LEFT JOIN producto p ON m.id_producto = p.id_producto
            LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
            LEFT JOIN lote l ON m.id_lote = l.id_lote
            ORDER BY m.fecha DESC, m.id_movimiento DESC
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error en servicio al obtener el historial de movimientos: {err}")
        return []
    finally:
        if db.is_connected():
            cursor.close()
            db.close()