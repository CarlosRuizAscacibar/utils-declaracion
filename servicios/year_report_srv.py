

from dataclasses import dataclass
from decimal import Decimal
from modelos.compra_venta import CompraVenta, CompraVentaReport
from modelos.movimiento_corriente import MovimientoCorriente
from modelos.operacion import Operacion
from servicios.compraventa_to_report import compraventa_to_report
from servicios.compraventas_por_isin import agrupar_por_isin, compra_ventas_por_isin, operaciones_por_isin
import pandas as pd

from servicios.operations_from_db import dividendos_year

@dataclass
class YearReport():
    year: str
    compra_ventas_report: list[CompraVentaReport]
    beneficio: Decimal
    dividendos: list[MovimientoCorriente]
    beneficio_dividendos: Decimal


def year_report(all_ops: list[Operacion], year: str, dic_curr: dict)->YearReport:
    compra_ventas = operaciones_por_isin(all_ops)
    compra_ventas_report_in_year:list[CompraVentaReport] = [ 
        compraventa_to_report(x, dic_curr) 
        for x in compra_ventas 
        if year == f'{x.venta.fecha.year}'
    ]
    dividendos = dividendos_year(year)

    return YearReport(
        year=year,
        compra_ventas_report=compra_ventas_report_in_year,
        beneficio=sum(item.ganancia_perdida_eur for item in compra_ventas_report_in_year),
        dividendos=dividendos,
        beneficio_dividendos=sum(item.importe for item in dividendos),
    )