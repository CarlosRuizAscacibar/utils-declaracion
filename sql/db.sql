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
CREATE VIEW operacion_forex_vinculada_movimiento AS
SELECT o.fecha,o.nombre,o.importe_neto, o.id AS id_operacion,bm.banco, bm.id AS id_movimiento,
bm.importe importe_banco,bm.concepto, o.importe_neto / eu.value AS importe_estimado_euro,
ABS( ABS(o.importe_neto / eu.value) - ABS(bm.importe)) AS diferencia_est_eur 
FROM operacion o 
JOIN bank_movements bm ON bm.fecha_contable = o.fecha 
AND
	(
		(
			o.tipo LIKE '%VENTA'
			AND
			(
				(bm.concepto LIKE '%VENTA%') OR --evo
				(bm.concepto LIKE '%@%')  --MYINV 
			)
			
		)
		OR
		(
			o.tipo LIKE '%COMPRA'
			AND
			(
				(bm.concepto LIKE '%COMPRA%') OR --evo
				(bm.concepto LIKE '%@%')  --MYINV 
			)
		)
	)
JOIN eur_usd eu ON eu.str_time = bm.fecha_contable AND o.divisa = 'USD'
WHERE ABS( ABS(o.importe_neto / eu.value) - ABS(bm.importe)) < 3
AND o.divisa != 'EUR';


DROP VIEW operacion_euro_vinculada_movimiento;
CREATE VIEW operacion_euro_vinculada_movimiento as
SELECT o.fecha,o.nombre,o.importe_neto, o.id AS id_operacion,bm.banco, bm.id AS id_movimiento,
bm.importe importe_banco,bm.concepto, o.importe_neto / 1 AS importe_estimado_euro,
ABS( ABS(o.importe_neto / 1) - ABS(bm.importe)) AS diferencia_est_eur  
FROM operacion o 
JOIN bank_movements bm ON bm.fecha_contable = o.fecha
	AND
	(
		(
			o.tipo LIKE '%VENTA'
			AND
			(
				(bm.concepto LIKE '%VENTA%') OR --evo
				(bm.concepto LIKE '%@%')  --MYINV 
			)
			
		)
		OR
		(
			o.tipo LIKE '%COMPRA'
			AND
			(
				(bm.concepto LIKE '%COMPRA%') OR --evo
				(bm.concepto LIKE '%@%')  --MYINV 
			)
		)
	)
	AND abs(bm.importe) = abs(o.importe_neto)
WHERE divisa='EUR' ;

DROP VIEW all_operacion_vinculada_movimiento;
CREATE VIEW all_operacion_vinculada_movimiento 
(fecha,nombre,importe_neto,id_operacion,banco,id_movimiento,importe_banco,concepto,importe_estimado_euro,diferencia_est_eur)
AS 
SELECT * FROM operacion_forex_vinculada_movimiento
UNION
SELECT * FROM operacion_euro_vinculada_movimiento;

-- compra_venta definition

CREATE TABLE "compra_venta" (
"index" INTEGER,
  "nombre" TEXT,
  "isin" TEXT,
  "fecha_compra" TEXT,
  "broker_compra" TEXT,
  "precio_unitario_compra" TEXT,
  "fecha_venta" TEXT,
  "broker_venta" TEXT,
  "precio_unitario_venta" TEXT,
  "cantidad" INTEGER,
  "precio_total_compra" TEXT,
  "precio_total_venta" TEXT,
  "ganancia_perdida" TEXT
);

CREATE INDEX "ix_compra_venta_index"ON "compra_venta" ("index");

DROP TABLE compra_venta;

CREATE VIEW op_dividendo_movimiento_espana AS 
SELECT * FROM operacion o 
JOIN bank_movements bm ON bm.fecha_contable = o.fecha
	AND
	(
		o.tipo LIKE '%DIVIDENDO'
		AND
		(
			(bm.concepto LIKE '%DIVIDENDO%') OR --evo
			(bm.concepto LIKE '%@%')  --MYINV 
		)
		
	)
	AND abs(bm.importe) = abs(o.importe_neto)
;
SELECT * FROM op_dividendo_movimiento_espana;

DROP VIEW op_dividendo_movimiento_forex;
CREATE VIEW op_dividendo_movimiento_forex AS 
SELECT o.id, o.importe_neto / eu.value as importe_eur FROM operacion o 
JOIN eur_usd eu ON eu.str_time = o.fecha AND o.divisa = 'USD'
WHERE o.tipo = 'TipoOperacion.DIVIDENDO'
;
SELECT isin, sum(importe_eur) 
FROM operacion o JOIN op_dividendo_movimiento_forex op_forex ON o.id = OP_FOREX.id 
WHERE o.fecha LIKE '2023%'
GROUP BY isin;

SELECT o.isin, o.nombre, OP_FOREX.importe_eur, OP_FOREX.importe_eur / 0.81 AS bruto, (OP_FOREX.importe_eur / 0.81) - OP_FOREX.importe_eur AS retencion
FROM operacion o JOIN op_dividendo_movimiento_forex op_forex ON o.id = OP_FOREX.id 
WHERE o.fecha LIKE '2023%'
;
SELECT * FROM operacion o WHERE fecha ='2023-11-30';
SELECT * FROM bank_movements bm WHERE fecha_valor = '2023-11-30';




SELECT sum(precio_total_venta)- sum(precio_total_compra) FROM compra_venta cv 
WHERE fecha_venta like '%2024%' 
-- AND cv.isin = 'IL0065100930'
;



SELECT "index",nombre,isin,fecha_venta,cantidad,precio_total_compra,precio_total_venta,ganancia_perdida 
FROM compra_venta cv 
WHERE fecha_venta LIKE '%2024%';


SELECT * FROM operacion;


SELECT * FROM operacion_forex_vinculada_movimiento 
WHERE id_operacion LIKE '%VENTA%' AND fecha LIKE '%2023%';

SELECT * FROM operacion o WHERE o.tipo LIKE '%COMPRA';

SELECT * FROM bank_movements bm  ORDER BY fecha_contable ;
SELECT * FROM operacion o WHERE broker != 'evo';
SELECT * FROM operacion_forex_vinculada_movimiento;

SELECT * FROM all_operacion_vinculada_movimiento;
SELECT * FROM bank_movements bm WHERE fecha_contable ='2024-01-23'

SELECT o.id,o.fecha,o.isin,o.tipo,o.cantidad,abs(vin_mov.importe_banco) / o.cantidad AS precio_unitario,'EUR' AS divisa,o.nombre,vin_mov.importe_banco AS importe_neto,o.broker,o.restantes 
FROM operacion o 
JOIN all_operacion_vinculada_movimiento vin_mov ON o.id = vin_mov.id_operacion;







