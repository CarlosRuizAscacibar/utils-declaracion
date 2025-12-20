from decimal import Decimal
import math
from modelos.compra_venta import CompraVenta, CompraVentaReport

def compraventa_to_report(compra_venta: CompraVenta, dic_all_curr) -> CompraVentaReport:
    precio_total_compra = compra_venta.compra.precio_unitario * compra_venta.cantidad
    precio_total_venta = compra_venta.venta.precio_unitario * compra_venta.cantidad
    dias_entre_compra_y_ultima_venta = 0
    if compra_venta.compra.fecha_ultima_venta and not math.isnan(compra_venta.compra.fecha_ultima_venta):
        dias_entre_compra_y_ultima_venta = (compra_venta.compra.fecha - compra_venta.compra.fecha_ultima_venta).days
    
    dec_precio_total_compra = convert_to_eur(precio_total_compra, 
                                             compra_venta.compra.divisa, 
                                             compra_venta.compra.fecha.strftime('%Y-%m-%d'), 
                                             dic_all_curr=dic_all_curr)
    
    dec_precio_total_venta = convert_to_eur(precio_total_venta, 
                                             compra_venta.venta.divisa, 
                                             compra_venta.venta.fecha.strftime('%Y-%m-%d'), 
                                             dic_all_curr=dic_all_curr)
    

    ganancia_perdida_eur = dec_precio_total_venta - dec_precio_total_compra
    return CompraVentaReport(
        nombre = compra_venta.compra.nombre,
        isin = compra_venta.compra.isin,
        fecha_compra= compra_venta.compra.fecha,
        broker_compra= compra_venta.compra.broker.name,
        precio_unitario_compra= compra_venta.compra.precio_unitario,
        fecha_venta= compra_venta.venta.fecha,
        broker_venta= compra_venta.venta.broker.name,
        precio_unitario_venta= compra_venta.venta.precio_unitario,
        cantidad=compra_venta.cantidad,
        precio_total_compra = precio_total_compra,
        precio_total_venta = precio_total_venta,
        ganancia_perdida = precio_total_venta - precio_total_compra,
        dias_entre_compra_y_ultima_venta = dias_entre_compra_y_ultima_venta,
        precio_total_compra_eur = dec_precio_total_compra,
        precio_total_venta_eur = dec_precio_total_venta,
        ganancia_perdida_eur =  ganancia_perdida_eur,
    )

def convert_to_eur(amount_to_convert: Decimal, divisa: str, str_fecha: str, dic_all_curr):
    if divisa == 'USD':
        return (amount_to_convert / dic_all_curr[divisa][str_fecha]).quantize(Decimal('0.00'))
    if divisa == 'GBP':
        return (amount_to_convert / dic_all_curr[divisa][str_fecha]).quantize(Decimal('0.00'))
    if divisa == 'EUR':
        return amount_to_convert
    else:
        return amount_to_convert

