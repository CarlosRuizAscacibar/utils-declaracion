#OLD SCRIPT FOR DEGIRO

#%%
import csv
import json
import math
import re
import pandas as pd
import datetime
import copy


# %%
input_file = csv.DictReader(open('Account.csv', newline='\n', encoding='utf8'))
rows = []
for row in input_file:
    rows.append(row)

#%%

# %%
class degiro_cols():
        fecha = "fecha"
        hora = "hora"
        fecha_valor = "fecha_valor"
        producto = "producto"
        isin = "isin"
        descripcion = "descripcion"
        tipo = "tipo"
        moneda_var = "moneda_var"
        variacion = "variacion"
        moneda_saldo = "moneda_saldo"
        saldo = "saldo"
        id_orden = "id_orden"
# %%
dic_degiro_operations={}
for x in rows:
    if x[degiro_cols.id_orden]:
        id_op = x[degiro_cols.id_orden]
        if not (id_op in dic_degiro_operations):
            dic_degiro_operations[id_op] = []
        dic_degiro_operations[id_op].append(x)


# %%

# %%
def comision_op(op):
    comision_ = 0
    for x in op:
        if 'Comisión' in x[degiro_cols.descripcion]:
            comision_ = comision_ + float(x[degiro_cols.variacion].replace(',','.'))
    return (-1.0 * comision_)

def is_compra(op):
    compra = False
    for x in op:
        if 'Compra ' in x[degiro_cols.descripcion]:
            compra = True
    return compra

def is_venta(op):
    venta = False
    for x in op:
        if 'Venta ' in x[degiro_cols.descripcion]:
            venta = True
    return venta

def value_compra(op):
    val = 0
    compra_val = 0
    retirada = 0
    for x in op:
        if 'Compra ' in x[degiro_cols.descripcion]:
            try:
                compra_val = compra_val + float(x[degiro_cols.variacion].replace(',','.'))
            except:
                print(f"ERROR IN {x[degiro_cols.id_orden]}")
        if 'Retirada Cambio de Divisa' in x[degiro_cols.descripcion]:
            retirada = abs(retirada + float(x[degiro_cols.variacion].replace(',','.')))
    if retirada > 0:
        val = retirada
    else:
        val = compra_val
     
    return val

def value_venta(op):
    val = 0
    compra_val = 0
    retirada = 0
    for x in op:
        if 'Venta ' in x[degiro_cols.descripcion]:
            compra_val = compra_val + float(x[degiro_cols.variacion].replace(',','.'))
        if 'Ingreso Cambio de Divisa' in x[degiro_cols.descripcion]:
            retirada = abs(retirada + float(x[degiro_cols.variacion].replace(',','.')))
    if retirada:
        val = retirada
    else:
        val = compra_val
    return val
def value(op):
    if is_compra(op):
        return abs(value_compra(op))
    if is_venta(op):
        return abs(value_venta(op))
    Exception("value() of operation which is not buy neither sell")

def numero_compra(op):
    res = 0
    for x in op:
        if 'Compra ' in x[degiro_cols.descripcion] :
            res = res+ int(re.match(r'Compra (\d+)', x[degiro_cols.descripcion]).groups()[0])
    return res
def numero_venta(op):
    res = 0
    for x in op:
        if 'Venta ' in x[degiro_cols.descripcion] :
            res = res + int(re.match(r'Venta (\d+)', x[degiro_cols.descripcion]).groups()[0])
    return res
    

def numero_op(op):
    if is_compra(op):
        return numero_compra(op)
    if is_venta(op):
        return numero_venta(op)
    Exception("value() of operation which is not buy neither sell")




def tipo_op(op):
    if is_compra(op):
        return 'compra'
    if is_venta(op):
        return 'venta'
    Exception("value() of operation which is not buy neither sell")

# %%
# %%
def info_op(op):
    print('info op')
    num = numero_op(op)
    val = value(op)
    comision = comision_op(op)
    tipo = tipo_op(op)
    try:
        val_comision = value_comision(val, comision, tipo)
    except Exception as e:
        print(op)
        raise e
    try :
        abs( round(val / float(num), 2))
    except :
        print(op)
    info={
        'comision': comision,
        'isin': op[0][degiro_cols.isin],
        'value': val,
        'value_comision': val_comision,
        'fecha': op[0][degiro_cols.fecha],
        'tipo': tipo,
        'producto': op[0][degiro_cols.producto],
        'numero': num,
        'precio': abs( round(val / float(num), 2)),
        'precio_comision': abs( round(val_comision / float(num), 2))
    }
    return info

def value_comision(value, comision, tipo_operacion):
    if tipo_operacion == 'compra':
        return round(value + comision, 2)
    if tipo_operacion == 'venta':
        return round(value - comision, 2)
    #raise Exception(f"Tipo de operacion desconocida {tipo_operacion}")
    return 0
    


def get_two_months(d, months_less):
    date_1 = pd.to_datetime(datetime.datetime.strftime(d,"%Y-%m-%d"), format="%Y-%m-%d") - pd.DateOffset(months=months_less)
    return date_1.to_pydatetime()

def has_venta_two_month_rule(op, ops):
    two_months_less = get_two_months(op['fecha'],2)
    if op['isin'][:2] != 'ES':
        two_months_less = get_two_months(op['fecha'],12)
    if ops != None:
        for x in ops:
            if x['tipo'] == 'venta' and x['fecha'] >= two_months_less and x['fecha'] < op['fecha']:
                print(f"{two_months_less} fecha venta: {x['fecha']}         fecha compra: {op['fecha']} ")
                return True
    return False
# %%


info_op(dic_degiro_operations['c3bf1b7f-27bc-4d5f-9d32-382b214dbc10'])
info_op(dic_degiro_operations['5857f585-264c-405a-a1b1-bfad86548c57'])

# %%
info_op(dic_degiro_operations['c3bf1b7f-27bc-4d5f-9d32-382b214dbc10'])
# %%
info_op(dic_degiro_operations['fb6cf6b8-9765-4ad7-b8d5-cc236b2f86c0'])
# %%
operations_info = []
for k,v in dic_degiro_operations.items():
    info = info_op(v)
    info['id'] = k
    operations_info.append(info)

pd.DataFrame(operations_info).to_csv('compras_y_ventas.csv')
# %%
dic_degiro_operations

# %%
ops = [x for x in operations_info if x['isin'] == 'ES0148396007']
# %%

# %%
# %%
def venta_cartera(op, cartera):
    venta_copy = copy.deepcopy(op)
    res = []
    cartera_for_op = []
    i = 0
    while venta_copy['numero'] > 0 and i<len(cartera):
        cartera_op = cartera[i]
        if cartera_op['numero'] > 0:
            numero = -1
            valor_de_compra = -1
            valor_venta = -1
            beneficio = -1
            if venta_copy['numero'] > cartera_op['numero']:
                numero = cartera_op['numero']
                cartera_for_op.append([cartera_op['numero'], cartera_op['precio_comision']])
                venta_copy['numero'] = venta_copy['numero'] - cartera_op['numero']
                valor_de_compra = round(cartera_op['precio_comision'] * numero, 2)
                valor_venta = round(venta_copy['precio_comision'] * cartera_op['numero'], 2)
                beneficio = round(valor_venta - valor_de_compra, 2)
                cartera_op['numero'] = 0
            if venta_copy['numero'] <= cartera_op['numero']:
                numero = venta_copy['numero']
                cartera_op['numero']= cartera_op['numero'] - numero
                valor_de_compra = round(numero * cartera_op['precio_comision'],2)
                valor_venta =  round(numero * venta_copy['precio_comision'] , 2)
                beneficio = round(valor_venta - valor_de_compra, 2)
                venta_copy['numero'] = 0


            res.append({
                    'isin': venta_copy['isin'] + ' | ' + venta_copy['producto'],
                    'valor_venta': valor_venta,
                    'valor_de_compra': valor_de_compra,
                    'recompra_impuestos': cartera_op['recompra'] and beneficio < 0,
                    'recompra': cartera_op['recompra'],
                    'fecha':venta_copy['fecha'],
                    'fecha_compra':cartera_op['fecha'],
                    'numero': numero,
                    'precio_compra': cartera_op['precio_comision'],
                    'precio_venta': venta_copy['precio_comision'],
                    'beneficio': beneficio
                })
        i = i + 1
    return res

def operaciones_por_isin(sorted_ops):
    cartera = []
    res = []
    i = 0
    for x in sorted_ops:
        if x['tipo'] == 'compra':
            x['recompra'] = has_venta_two_month_rule(x, sorted_ops[:i])
        i = i + 1
    
    for x in sorted_ops:
        if x['tipo'] == 'compra':
            cartera.append(x)
        else:
            res.extend(venta_cartera(x, cartera))
    return res

dic_ops_isin={}
for x in operations_info:
    if x['isin']:
        id_op = x['isin']
        if not (id_op in dic_ops_isin):
            dic_ops_isin[id_op] = []
        dic_ops_isin[id_op].append(x)
res = []
for isin, ops_isin in dic_ops_isin.items():
    for x in ops_isin:
        x['fecha'] = datetime.datetime.strptime(x['fecha'],'%d-%m-%Y')
    sorted_ops_isin = sorted(ops_isin, key=lambda x: x['fecha'])
    res.extend(operaciones_por_isin(sorted_ops_isin))

pd.DataFrame(res).to_csv('declaracion_compra_venta.csv')

# %%

# %%
