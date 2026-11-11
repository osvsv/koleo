-- Esquema SQL canonico de KOLEO (SQLite). Fuente: Documentacion General 10.2 + id_evento.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS tarimas (
    id_tarima            VARCHAR(32) PRIMARY KEY,
    descripcion          VARCHAR(100),
    peso_kg              DECIMAL(5,2),
    ubicacion_nodo       VARCHAR(16),
    coord_x_cm           DECIMAL(6,2),
    coord_y_cm           DECIMAL(6,2),
    estado               VARCHAR(20) NOT NULL DEFAULT 'EN_PISO'
        CHECK (estado IN ('EN_PISO','EN_TRANSITO','UBICADA_DESTINO','BLOQUEADA_SOBREPESO')),
    ultima_actualizacion TIMESTAMP
);

CREATE TABLE IF NOT EXISTS historial_movimientos (
    id_movimiento   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_evento       VARCHAR(64) NOT NULL UNIQUE,
    id_tarima       VARCHAR(32) NOT NULL REFERENCES tarimas(id_tarima),
    ruta_ejecutada  VARCHAR(32),
    origen_x_cm     DECIMAL(6,2),
    origen_y_cm     DECIMAL(6,2),
    destino_x_cm    DECIMAL(6,2),
    destino_y_cm    DECIMAL(6,2),
    peso_medido_kg  DECIMAL(5,2),
    latencia_red_ms INTEGER,
    fecha_hora      TIMESTAMP
);

CREATE TABLE IF NOT EXISTS registro_rechazos_seguridad (
    id_alerta         INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tarima         VARCHAR(32) NOT NULL REFERENCES tarimas(id_tarima),
    peso_detectado_kg DECIMAL(5,2),
    motivo            VARCHAR(100),
    coord_x_cm        DECIMAL(6,2),
    coord_y_cm        DECIMAL(6,2),
    fecha_hora        TIMESTAMP
);
