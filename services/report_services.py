# services/report_service.py

import mysql.connector
from datetime import datetime, timedelta
from utils.db_connection import conectar_db

def get_low_stock_report_data(threshold=10):
    """
    Obtiene los productos ACTIVOS cuyo stock total consolidado está por debajo de un umbral.
    """
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        sql = """
            SELECT p.codigo_producto, p.nombre, p.tipo,
                   IFNULL(SUM(l.cantidad_actual), 0) AS stock_total
            FROM producto p
            LEFT JOIN lote l ON p.id_producto = l.id_producto AND l.cantidad_actual > 0
            WHERE p.estado = 'Activo'
            GROUP BY p.id_producto
            HAVING stock_total <= %s
            ORDER BY stock_total ASC;
        """
        cursor.execute(sql, (threshold,))
        return cursor.fetchall()
    finally:
        if db.is_connected(): cursor.close(); db.close()

def get_expiring_soon_report_data(days_ahead=30):
    """
    Obtiene los lotes ACTIVOS que vencen en los próximos N días.
    """
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        fecha_limite = datetime.now().date() + timedelta(days=days_ahead)
        sql = """
            SELECT 
                p.codigo_producto, p.nombre,
                l.tag_lote, l.cantidad_actual, l.unidad_medida, l.fecha_vencimiento
            FROM lote l
            JOIN producto p ON l.id_producto = p.id_producto
            WHERE l.fecha_vencimiento IS NOT NULL 
              AND l.fecha_vencimiento <= %s
              AND l.cantidad_actual > 0
              AND p.estado = 'Activo'
            ORDER BY l.fecha_vencimiento ASC;
        """
        cursor.execute(sql, (fecha_limite,))
        return cursor.fetchall()
    finally:
        if db.is_connected(): cursor.close(); db.close()

def get_movements_by_date_range(start_date, end_date):
    """Obtiene todos los movimientos dentro de un rango de fechas."""
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        sql = """
            SELECT m.fecha, p.nombre as producto_nombre, m.tipo, l.tag_lote, m.cantidad, m.descripcion, u.nombre_completo as usuario_nombre
            FROM movimiento m
            JOIN producto p ON m.id_producto = p.id_producto
            JOIN usuario u ON m.id_usuario = u.id_usuario
            LEFT JOIN lote l ON m.id_lote = l.id_lote
            WHERE DATE(m.fecha) BETWEEN %s AND %s
            ORDER BY m.fecha DESC
        """
        cursor.execute(sql, (start_date, end_date))
        return cursor.fetchall()
    finally:
        if db.is_connected(): cursor.close(); db.close()

def get_lot_traceability_report(lote_id):
    """Obtiene el historial completo de movimientos de un lote específico."""
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        sql = """
            SELECT m.fecha, m.tipo, m.cantidad, m.descripcion, u.nombre_completo as usuario_nombre
            FROM movimiento m
            JOIN usuario u ON m.id_usuario = u.id_usuario
            WHERE m.id_lote = %s
            ORDER BY m.fecha ASC
        """
        cursor.execute(sql, (lote_id,))
        return cursor.fetchall()
    finally:
        if db.is_connected(): cursor.close(); db.close()

def get_movements_by_product(product_id, start_date, end_date):
    """Obtiene todos los movimientos de un producto específico en un rango de fechas."""
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        sql = """
            SELECT m.fecha, l.tag_lote, m.tipo, m.cantidad, m.descripcion, u.nombre_completo as usuario_nombre
            FROM movimiento m
            JOIN usuario u ON m.id_usuario = u.id_usuario
            LEFT JOIN lote l ON m.id_lote = l.id_lote
            WHERE m.id_producto = %s AND DATE(m.fecha) BETWEEN %s AND %s
            ORDER BY m.fecha DESC
        """
        cursor.execute(sql, (product_id, start_date, end_date))
        return cursor.fetchall()
    finally:
        if db.is_connected(): cursor.close(); db.close()

def get_entries_by_provider(provider_id, start_date, end_date):
    """Obtiene todas las entradas (lotes) asociadas a productos de un proveedor específico en un rango de fechas."""
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        sql = """
            SELECT l.fecha_ingreso, p.nombre as producto_nombre, l.tag_lote, l.cantidad_inicial, l.unidad_medida, l.fecha_vencimiento
            FROM lote l
            JOIN producto p ON l.id_producto = p.id_producto
            JOIN producto_proveedor pp ON p.id_producto = pp.id_producto
            WHERE pp.id_proveedor = %s AND l.fecha_ingreso BETWEEN %s AND %s
            ORDER BY l.fecha_ingreso DESC
        """
        cursor.execute(sql, (provider_id, start_date, end_date))
        return cursor.fetchall()
    finally:
        if db.is_connected(): cursor.close(); db.close()
        
def get_full_stock_report_data():
    """
    Obtiene el stock actual de TODOS los productos activos.
    """
    db = conectar_db()
    if not db: return []
    cursor = db.cursor(dictionary=True)
    try:
        # Esta consulta es similar a la de stock mínimo, pero sin el filtro HAVING.
        sql = """
            SELECT p.codigo_producto, p.nombre, p.tipo,
                   IFNULL(SUM(l.cantidad_actual), 0) AS stock_total,
                   GROUP_CONCAT(DISTINCT l.unidad_medida SEPARATOR ', ') as unidades
            FROM producto p
            LEFT JOIN lote l ON p.id_producto = l.id_producto AND l.cantidad_actual > 0
            WHERE p.estado = 'Activo'
            GROUP BY p.id_producto
            ORDER BY p.nombre ASC;
        """
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        if db.is_connected(): cursor.close(); db.close()