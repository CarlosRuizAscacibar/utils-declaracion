CREATE TABLE "bank_movements" (
  "id" TEXT NOT NULL PRIMARY KEY,
  "concepto" TEXT,
  "importe" TEXT,
  "fecha_contable" TEXT,
  "fecha_valor" TEXT,
  "banco" TEXT,
  "saldo" TEXT
);

CREATE TABLE "operacion" (
  "id" TEXT NOT NULL PRIMARY KEY,
  "fecha" DATE,
  "isin" TEXT,
  "tipo" TEXT,
  "cantidad" INTEGER,
  "precio_unitario" TEXT,
  "divisa" TEXT,
  "nombre" TEXT,
  "importe_neto" TEXT,
  "broker" TEXT,
  "restantes" INTEGER
);

-- eur_usd definition

CREATE TABLE "eur_usd" (
  "str_time" TEXT NOT NULL PRIMARY KEY,
  "source" TEXT,
  "target" TEXT,
  "value" REAL,
  "time" INTEGER

);



select a.s + b.s from 
(select SUM(importe) s from bank_movements WHERE concepto like 'VENTA VALORES') a
,(select SUM(importe) s from bank_movements WHERE concepto like 'COMPRA VALORES')  b;
SELECT sum(importe_neto) FROM operacion
WHERE (tipo IN ('TipoOperacion.DIVIDENDO')) AND (nombre IN ('ZIM INTEGRATED SHIPPING SERV'));
SELECT * FROM bank_movements bm WHERE bm.fecha_contable = '2021-11-30';
SELECT * FROM bank_movements bm WHERE concepto LIKE '%dividendo%'
AND bm.fecha_contable LIKE '2023%';
SELECT * FROM eur_usd ;
DROP TABLE eur_usd;
SELECT * FROM bank_movements bm  ;

DROP VIEW operacion_forex_vinculada_movimiento;
CREATE VIEW operacion_forex_vinculada_movimiento as
SELECT o.fecha,o.nombre,o.importe_neto, o.id AS id_operacion, bm.id AS id_movimiento,
bm.importe importe_banco, o.importe_neto / eu.value AS importe_estimado_euro,
ABS( ABS(o.importe_neto / eu.value) - ABS(bm.importe)) AS diferencia_est_eur 
FROM operacion o 
JOIN bank_movements bm ON bm.fecha_contable = o.fecha 
AND (
	(bm.concepto LIKE '%COMPRA%' AND o.tipo LIKE '%COMPRA')
	OR
	(bm.concepto LIKE '%VENTA%' AND o.tipo LIKE '%VENTA')
)
JOIN eur_usd eu ON eu.str_time = bm.fecha_contable AND o.divisa = 'USD'
WHERE ABS( ABS(o.importe_neto / eu.value) - ABS(bm.importe)) < 3
AND o.divisa != 'EUR';

SELECT o.fecha,o.nombre,o.importe_neto, o.id AS id_operacion, bm.id AS id_movimiento,
bm.importe importe_banco, o.importe_neto / eu.value AS importe_estimado_euro,
ABS( ABS(o.importe_neto / eu.value) - ABS(bm.importe)) AS diferencia_est_eur 
FROM operacion o 
JOIN bank_movements bm ON bm.fecha_contable = o.fecha 
	AND bm.concepto LIKE '%VENTA%' AND o.tipo LIKE '%VENTA'
JOIN eur_usd eu ON eu.str_time = bm.fecha_contable AND o.divisa = 'USD'
WHERE ABS( (o.importe_neto / eu.value) - bm.importe) < 3
AND o.divisa != 'EUR';

SELECT * FROM operacion_forex_vinculada_movimiento 
WHERE id_operacion LIKE '%VENTA%' AND fecha LIKE '%2023%';

SELECT * FROM operacion o WHERE o.tipo LIKE '%COMPRA';

SELECT * FROM bank_movements bm ;



