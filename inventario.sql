-- ====================================================================
-- SCRIPT DE REINICIO TOTAL Y POBLACIÓN DE DATOS (VERSIÓN FINAL)
-- ====================================================================

DROP DATABASE IF EXISTS inventario;
CREATE DATABASE inventario;
USE inventario;

CREATE TABLE usuario (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre_completo VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    rol ENUM('Administrador', 'Operador') NOT NULL,
    estado ENUM('Activo', 'Inactivo') NOT NULL DEFAULT 'Activo'
);

CREATE TABLE proveedor (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    rif VARCHAR(15) NOT NULL UNIQUE,
    telefono VARCHAR(20), 
    direccion VARCHAR(200),
    estado ENUM('Activo', 'Inactivo') NOT NULL DEFAULT 'Activo'
);

CREATE TABLE producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    codigo_producto VARCHAR(30) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    tipo ENUM('Carnicos', 'Viveres') NOT NULL,
    estado ENUM('Activo', 'Inactivo') NOT NULL DEFAULT 'Activo'
);

CREATE TABLE producto_proveedor (
    id_producto_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    id_proveedor INT NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto) ON DELETE CASCADE,
    FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor) ON DELETE CASCADE,
    UNIQUE KEY uq_producto_proveedor (id_producto, id_proveedor)
);

CREATE TABLE lote (
    id_lote INT AUTO_INCREMENT PRIMARY KEY,
    tag_lote VARCHAR(50) NOT NULL UNIQUE,
    cantidad_inicial DECIMAL(10, 3) NOT NULL,
    cantidad_actual DECIMAL(10, 3) NOT NULL,
    unidad_medida ENUM('Unidades', 'Kilos') NOT NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_vencimiento DATE,
    id_producto INT,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto) ON DELETE CASCADE
);

CREATE TABLE movimiento (
    id_movimiento INT PRIMARY KEY AUTO_INCREMENT,
    tipo ENUM('Entrada', 'Salida', 'Ajuste') NOT NULL,
    cantidad DECIMAL(10, 3) NOT NULL,
    descripcion VARCHAR(255) NULL DEFAULT NULL,
    fecha DATETIME NOT NULL,
    id_producto INT,
    id_usuario INT,
    id_lote INT,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto), 
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_lote) REFERENCES lote(id_lote)
);


CREATE TABLE reporte (
    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
    fecha_generacion DATETIME NOT NULL,
    tipo_reporte VARCHAR(100) NOT NULL,
    id_usuario INT, 
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) 
);

