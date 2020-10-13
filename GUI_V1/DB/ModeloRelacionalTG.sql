/* CREATE TABLE Coordenadas_trayectoria (
  mision_id INTEGER UNSIGNED NOT NULL,
  index_2 INTEGER UNSIGNED NOT NULL,
  wpt VARCHAR(255) NOT NULL,
  latitud VARCHAR(255) NOT NULL,
  longitud VARCHAR(255) NOT NULL,
  elevacion VARCHAR(255) NOT NULL,
  PRIMARY KEY(mision_id),
  INDEX Coordenadas_trayectoria_FKIndex1(mision_id)
); */

CREATE TABLE departamentos (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY(id)
)
ENGINE=InnoDB;

CREATE TABLE mision (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  municipios_id INTEGER UNSIGNED NOT NULL,
  nombre_mision VARCHAR(255) NOT NULL,
  nombre_fachada VARCHAR(255) NOT NULL,
  fecha DATE NOT NULL,
  descripcion BLOB NULL,
  nombre_usuario VARCHAR(255) NOT NULL,
  email_usuario VARCHAR(255) NOT NULL,
  camara_id FLOAT NOT NULL,
  camara_fx FLOAT NOT NULL,
  camara_fy FLOAT NOT NULL,
  camara_cx FLOAT NOT NULL,
  camara_cy FLOAT NOT NULL,
  camara_k1 FLOAT NOT NULL,
  camara_k2 FLOAT NOT NULL,
  camara_cv_v FLOAT NOT NULL,
  camara_cv_h FLOAT NOT NULL,
  coordenadas BLOB NOT NULL,
  fachada_alto FLOAT NOT NULL,
  fachada_ancho FLOAT NOT NULL,
  estado_mision INT NOT NULL,
  PRIMARY KEY(id),
  INDEX mision_FKIndex1(municipios_id)
)
ENGINE=InnoDB;

ALTER TABLE mision
ADD CONSTRAINT UC_mision UNIQUE (nombre_mision,fecha);

CREATE TABLE municipios (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  departamentos_id INTEGER UNSIGNED NOT NULL,
  nombre VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY(id),
  INDEX municipio_FKIndex1(departamentos_id)
)
ENGINE=InnoDB;

CREATE TABLE registro_fotografico (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  mision_id INTEGER UNSIGNED NOT NULL,
  imagen_entrada MEDIUMBLOB NOT NULL,
  PRIMARY KEY(id),
  INDEX registro_FKIndex1(mision_id)
);

CREATE TABLE resultados (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  mision_id INTEGER UNSIGNED NOT NULL,
  fecha DATE NOT NULL,
  imagen_salida LONGBLOB NOT NULL,
  sizeimg_entrada FLOAT NOT NULL,
  sizeimg_salida FLOAT NOT NULL,
  paremtro_rd VARCHAR(255) NOT NULL,
  PRIMARY KEY(id),
  INDEX Resultados_FKIndex1(mision_id)
);

CREATE TABLE telemetria (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  mision_id INTEGER UNSIGNED NOT NULL,
  hora_medicion TIME NOT NULL,
  sensor_1 FLOAT NOT NULL,
  sensor_2 FLOAT NOT NULL,
  sensor_3 FLOAT NOT NULL,
  sensor_4 FLOAT NOT NULL,
  sensor_5 FLOAT NOT NULL,
  PRIMARY KEY(id),
  INDEX telemetria_FKIndex1(mision_id)
);


