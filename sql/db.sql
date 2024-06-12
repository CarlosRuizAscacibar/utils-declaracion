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
