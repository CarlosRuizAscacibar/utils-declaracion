from modelos.cartera_isin import CarteraIsin
from modelos.operacion import Operacion
from modelos.split import Split
from modelos.tipo_operacion import TipoOperacion
from modelos.compra_venta import CompraVenta
from servicios.compraventa_to_report import compraventa_to_report
from servicios.operations_from_db import all_dividendos
from servicios.quote_srv import quote_for_isin_eur

def cartere_isin(operaciones: list[Operacion | Split], isin: str, dic_curr) -> CarteraIsin:
    op_isin_dic: dict[str, list[Operacion]] = agrupar_por_isin(operaciones=operaciones)
    compra_ventas = compra_ventas_por_isin(op_isin_dic[isin])
    compra_ventas_report = [compraventa_to_report(x, dic_curr) for x in compra_ventas]
    acciones_actual = sum( getattr(op, "restantes", 0) for op in op_isin_dic[isin])
    quote_actual = quote_for_isin_eur(isin)
    valor_actual = 0
    if quote_actual:
        valor_actual = quote_actual * acciones_actual

    dividendos = [x for x in all_dividendos() if op_isin_dic[isin][0].nombre in x.concepto]
    return CarteraIsin(isin= isin,
        operaciones = op_isin_dic[isin],
        compra_ventas = compra_ventas,
        acciones_actual=acciones_actual,
        compra_ventas_report = compra_ventas_report,
        dividendos=dividendos,
        beneficio_dividendos=sum(item.importe for item in dividendos),
        valor_actual=valor_actual
    )


def operaciones_por_isin(operaciones: list[Operacion | Split]) -> list[CompraVenta]:
    op_isin_dic: dict[str, list[Operacion]] = agrupar_por_isin(operaciones=operaciones)
    compra_ventas : list[CompraVenta] = []
    for isin in op_isin_dic:
        compra_ventas = compra_ventas + compra_ventas_por_isin(op_isin_dic[isin])
    
    compra_ventas = sorted(compra_ventas, key=lambda x: x.venta.fecha.isoformat())
    return compra_ventas
    
def agrupar_por_isin(operaciones: list[Operacion | Split]) -> dict[str, list[Operacion]]:
    dic_isin = dict()
    for op in operaciones:
        if op.isin not in dic_isin:
            dic_isin[op.isin] = []
        dic_isin[op.isin].append(op)
    
    for clave in dic_isin:
        dic_isin[clave] = sorted(dic_isin[clave], key= sort_key)
        fill_ultima_venta(dic_isin[clave])

    return dic_isin

def dias_ultima_venta(op: Operacion) -> int | None:
        if isinstance(op.fecha_ultima_venta, float):
            op.fecha_ultima_venta = None
            return
    
        if op.fecha_ultima_venta is None:
            op.dias_ultima_venta = None
            return

        op.dias_ultima_venta = (op.fecha - op.fecha_ultima_venta).days

def fill_ultima_venta(operaciones: list[Operacion | Split]) -> None:
    ultima_fecha_venta = None
    for op in operaciones:
        if isinstance(op, Split):
            continue
        if op.tipo == TipoOperacion.VENTA:
            ultima_fecha_venta = op.fecha
        elif op.tipo == TipoOperacion.COMPRA:
            op.fecha_ultima_venta = ultima_fecha_venta
            dias_ultima_venta(op)


def sort_key(x: Split | Operacion):
    key = x.fecha.isoformat()
    if hasattr(x, "tipo"):
        key = key + x.tipo.name
    return key

def compra_ventas_por_isin(operaciones: list[Operacion | Split]) -> list[CompraVenta]:
    compra_ventas: list[CompraVenta] = []
    compras_con_acciones: list[Operacion] = []
    for x in operaciones:
        if isinstance(x, Split):
            for y in compras_con_acciones:
                y.restantes = y.restantes / x.numOriginal
                y.restantes = y.restantes * x.numDestino
        else:
            if x.tipo == TipoOperacion.COMPRA:
                compras_con_acciones.append(x)
            if x.tipo == TipoOperacion.VENTA:
                while len(compras_con_acciones) > 0 and x.restantes > 0:
                    cantidad = x.restantes
                    if cantidad > compras_con_acciones[0].restantes:
                        cantidad = compras_con_acciones[0].restantes
                    compra_ventas.append(CompraVenta(compra=compras_con_acciones[0], venta=x, cantidad=cantidad))
                    compras_con_acciones[0].restantes = compras_con_acciones[0].restantes - cantidad
                    if compras_con_acciones[0].restantes == 0:
                        compras_con_acciones.pop(0)
                    x.restantes = x.restantes - cantidad
                if len(compras_con_acciones) == 0 and x.restantes > 0:
                    raise Exception(f"Accion sin compras {x.isin} {x.fecha} {x.tipo.name} {x.cantidad} {x.restantes}")
    return compra_ventas