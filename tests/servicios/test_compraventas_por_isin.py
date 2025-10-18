from modelos.split import Split
from servicios.compraventas_por_isin import operaciones_por_isin, agrupar_por_isin
from modelos.tipo_operacion import TipoOperacion
from datetime import datetime
from modelos.operacion import Operacion
import unittest
import json

class TestCompraVentasPorIsin(unittest.TestCase):
    def test_operaciones_por_isin(self):
        op1 = Operacion(fecha=datetime.strptime('01-01-2020', '%d-%m-%Y'),isin='ISIN1',cantidad=1,precio_unitario=1,tipo=TipoOperacion.COMPRA, restantes=1)
        op2 = Operacion(fecha=datetime.strptime('04-01-2020', '%d-%m-%Y'),isin='ISIN2',cantidad=1,precio_unitario=1,tipo=TipoOperacion.VENTA, restantes=1)
        op3 = Operacion(fecha=datetime.strptime('03-01-2020', '%d-%m-%Y'),isin='ISIN2',cantidad=1,precio_unitario=1,tipo=TipoOperacion.COMPRA, restantes=1)
        operaciones = [op1,op2,op3]

        dic_isin = agrupar_por_isin(operaciones)
        self.assertTrue('ISIN1' in dic_isin)
        self.assertEqual(len(dic_isin['ISIN1']),1)
        self.assertEqual(len(dic_isin['ISIN2']),2)
    
    def test_operaciones_por_isin_1_compra_varias_ventas(self):
        op1 = Operacion(fecha=datetime.strptime('01-01-2020', '%d-%m-%Y'),isin='ISIN1',cantidad=2,precio_unitario=1,tipo=TipoOperacion.COMPRA, restantes=2)
        op2 = Operacion(fecha=datetime.strptime('04-01-2020', '%d-%m-%Y'),isin='ISIN1',cantidad=1,precio_unitario=2,tipo=TipoOperacion.VENTA, restantes=1)
        op3 = Operacion(fecha=datetime.strptime('03-01-2020', '%d-%m-%Y'),isin='ISIN1',cantidad=1,precio_unitario=3,tipo=TipoOperacion.VENTA, restantes=1)
        operaciones = [op1,op2,op3]

        dic_isin = operaciones_por_isin(operaciones)
        self.assertEqual(dic_isin[0].cantidad,1)
        self.assertEqual(dic_isin[0].compra,op1)
        self.assertEqual(dic_isin[0].venta,op3)
        self.assertEqual(dic_isin[1].compra,op1)
        self.assertEqual(dic_isin[1].venta,op2)
    
    def test_operaciones_por_isin_varias_compras_una_ventas(self):
        op1 = Operacion(fecha=datetime.strptime('01-01-2020', '%d-%m-%Y'),isin='ISIN1',cantidad=2,precio_unitario=1,tipo=TipoOperacion.COMPRA, restantes=2)
        op2 = Operacion(fecha=datetime.strptime('03-01-2020', '%d-%m-%Y'),isin='ISIN1',cantidad=3,precio_unitario=3,tipo=TipoOperacion.COMPRA, restantes=3)
        op3 = Operacion(fecha=datetime.strptime('04-01-2020', '%d-%m-%Y'),isin='ISIN1',cantidad=5,precio_unitario=2,tipo=TipoOperacion.VENTA, restantes=5)
        operaciones = [op1,op2,op3]

        dic_isin = operaciones_por_isin(operaciones)
        self.assertEqual(dic_isin[0].cantidad,2)
        self.assertEqual(dic_isin[0].compra,op1)
        self.assertEqual(dic_isin[0].venta,op3)
        self.assertEqual(dic_isin[1].cantidad,3)
        self.assertEqual(dic_isin[1].compra,op2)
        self.assertEqual(dic_isin[1].venta,op3)
    
    def test_operaciones_por_isin_varias_compras_una_ventas_y_sobran(self):
        op1 = Operacion(fecha=datetime.strptime('01-01-2020', '%d-%m-%Y'),isin='ISIN1',cantidad=2,precio_unitario=1,tipo=TipoOperacion.COMPRA, restantes=2)
        op2 = Operacion(fecha=datetime.strptime('03-01-2020', '%d-%m-%Y'),isin='ISIN1',cantidad=4,precio_unitario=3,tipo=TipoOperacion.COMPRA, restantes=4)
        op3 = Operacion(fecha=datetime.strptime('04-01-2020', '%d-%m-%Y'),isin='ISIN1',cantidad=5,precio_unitario=2,tipo=TipoOperacion.VENTA, restantes=5)
        operaciones = [op1,op2,op3]

        dic_isin = operaciones_por_isin(operaciones)
        self.assertEqual(dic_isin[0].cantidad,2)
        self.assertEqual(dic_isin[0].compra,op1)
        self.assertEqual(dic_isin[0].venta,op3)
        self.assertEqual(dic_isin[1].cantidad,3)
        self.assertEqual(dic_isin[1].compra,op2)
        self.assertEqual(dic_isin[1].venta,op3)
        self.assertEqual(op1.restantes, 0)
        self.assertEqual(op2.restantes, 1)

    def test_operaciones_por_isin_varias_compras_una_ventas_y_split(self):
        op1 = Operacion(fecha=datetime.strptime('01-01-2020', '%d-%m-%Y'),isin='ISIN1',cantidad=2,precio_unitario=1,tipo=TipoOperacion.COMPRA, restantes=2)
        op2 = Operacion(fecha=datetime.strptime('03-01-2020', '%d-%m-%Y'),isin='ISIN1',cantidad=4,precio_unitario=3,tipo=TipoOperacion.COMPRA, restantes=4)
        op3 = Operacion(fecha=datetime.strptime('04-01-2020', '%d-%m-%Y'),isin='ISIN1',cantidad=5,precio_unitario=2,tipo=TipoOperacion.VENTA, restantes=5)
        op4 = Split(id='split_isin1', isin='ISIN1', fecha=datetime.strptime('05-01-2020', '%d-%m-%Y'), numOriginal=1, numDestino=10)
        operaciones = [op1,op2,op3, op4]

        dic_isin = operaciones_por_isin(operaciones)
        self.assertEqual(dic_isin[0].cantidad,2)
        self.assertEqual(dic_isin[0].compra,op1)
        self.assertEqual(dic_isin[0].venta,op3)
        self.assertEqual(dic_isin[1].cantidad,3)
        self.assertEqual(dic_isin[1].compra,op2)
        self.assertEqual(dic_isin[1].venta,op3)
        self.assertEqual(op1.restantes, 0)
        self.assertEqual(op2.restantes, 10)
