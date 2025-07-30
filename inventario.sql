CREATE DATABASE IF NOT EXISTS inventario;
USE inventario;

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre_completo VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    rol ENUM('Administrador', 'Operador') NOT NULL 
);

CREATE TABLE IF NOT EXISTS proveedor (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    rif VARCHAR(15) NOT NULL UNIQUE,
    telefono VARCHAR(20), 
    direccion VARCHAR(200) 
);


CREATE TABLE IF NOT EXISTS producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    codigo_producto VARCHAR(30) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    tipo ENUM('Carnicos', 'Viveres') NOT NULL, 
    fecha_ingreso DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    cantidad INT NOT NULL,
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor) 
);

CREATE TABLE IF NOT EXISTS reporte (
    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
    fecha_generacion DATE NOT NULL,
    tipo_reporte ENUM('Stock mínimo', 'Productos Por Vencer') NOT NULL, 
    id_usuario INT, 
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) 
);

CREATE TABLE IF NOT EXISTS movimiento (
    id_movimiento INT PRIMARY KEY AUTO_INCREMENT,
    tipo ENUM('Entrada', 'Salida') NOT NULL,
    cantidad INT NOT NULL,
    fecha DATE NOT NULL,
    id_producto INT,
    id_usuario INT,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto), 
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) 
);
  
  