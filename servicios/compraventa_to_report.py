from modelos.compra_venta import CompraVenta, CompraVentaReport

def compraventa_to_report(compra_venta: CompraVenta) -> CompraVentaReport:
    precio_total_compra = compra_venta.compra.precio_unitario * compra_venta.cantidad
    precio_total_venta = compra_venta.venta.precio_unitario * compra_venta.cantidad
    dias_entre_compra_y_ultima_venta = 0
    if compra_venta.compra.fecha_ultima_venta:
        dias_entre_compra_y_ultima_venta = (compra_venta.compra.fecha - compra_venta.compra.fecha_ultima_venta).days
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
        dias_entre_compra_y_ultima_venta = dias_entre_compra_y_ultima_venta
    )