DROP DATABASE IF EXISTS veterinaria_huellitas;
CREATE DATABASE veterinaria_huellitas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE veterinaria_huellitas;

CREATE TABLE roles (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE usuarios (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(255) NOT NULL,
    telefono VARCHAR(15) NULL,
    rol_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_usuarios_roles FOREIGN KEY (rol_id) REFERENCES roles (id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE mascotas (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raza VARCHAR(100) NULL,
    sexo VARCHAR(15) NULL,
    fecha_nacimiento DATE NULL,
    usuario_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Eliminar un cliente borra a sus mascotas registradas
    CONSTRAINT fk_mascotas_usuarios FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE servicios (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(500) NULL,
    precio DECIMAL(10, 2) NOT NULL,
    duracion_minutos INT NOT NULL,
    -- Baja lógica para no romper reservas pasadas si se deja de ofrecer el servicio
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE reservas (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME NOT NULL,
    fecha_hora_fin DATETIME NOT NULL,
    mascota_id BIGINT NOT NULL,
    usuario_id BIGINT NOT NULL,
    servicio_id BIGINT NOT NULL,
    observaciones VARCHAR(500) NULL,
    estado ENUM('CONFIRMADA', 'CANCELADA', 'ATENDIDA') NOT NULL DEFAULT 'CONFIRMADA',
    creada_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- RESTRICT protege el historial: no se puede borrar una mascota o servicio con citas previas
    CONSTRAINT fk_reservas_mascotas FOREIGN KEY (mascota_id) REFERENCES mascotas (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_reservas_usuarios FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_reservas_servicios FOREIGN KEY (servicio_id) REFERENCES servicios (id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE atenciones (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    -- UNIQUE impone la relación 1 a 1: una reserva solo genera un único expediente
    reserva_id BIGINT NOT NULL UNIQUE,
    peso_kg DECIMAL(5, 2) NULL,
    diagnostico_o_detalle VARCHAR(1000) NOT NULL,
    tratamiento_o_indicaciones VARCHAR(1000) NULL,
    fecha_atencion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- SET NULL preserva el expediente médico intacto si se da de baja al usuario staff
    atendido_por_id BIGINT NULL,
    CONSTRAINT fk_atenciones_reservas FOREIGN KEY (reserva_id) REFERENCES reservas (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_atenciones_staff FOREIGN KEY (atendido_por_id) REFERENCES usuarios (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Acelera la validación de cruces de horarios en el agendamiento concurrente
CREATE INDEX idx_reservas_fechas ON reservas (fecha_hora, fecha_hora_fin);
CREATE INDEX idx_reservas_estado ON reservas (estado);
CREATE INDEX idx_mascotas_usuario ON mascotas (usuario_id);