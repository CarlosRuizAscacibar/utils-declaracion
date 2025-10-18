from modelos.operacion import Operacion
from modelos.split import Split
from modelos.tipo_operacion import TipoOperacion
from modelos.compra_venta import CompraVenta

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

    return dic_isin

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