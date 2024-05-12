import os
from servicios.lector_fichero_evo import leer_excel_evo_y_mapear_objetos, parse_evo_date
import unittest
from modelos.operacion import Operacion
from modelos.broker import BrokerEnum
from decimal import Decimal
from modelos.tipo_operacion import TipoOperacion
from datetime import date, datetime

import sys
sys.path.append("../../..")

class TestLecturaArchivoEvo(unittest.TestCase):
    def test_evento_compra_venta(self):
        ruta_ejemplo_fichero_evo = os.path.join(os.path.dirname(__file__),'..', 'data', 'ejemplo_fichero_evo.xlsx')
        operaciones: list[Operacion] = leer_excel_evo_y_mapear_objetos(ruta_ejemplo_fichero_evo, broker=BrokerEnum.EVO)
        self.assertEqual(len(operaciones), 2, "Debería leer 2 operaciones")
        self.assertEqual(operaciones[0].broker, BrokerEnum.EVO)
        self.assertEqual(operaciones[0].cantidad, 18)
        self.assertEqual(operaciones[0].precio_unitario, Decimal('0.1040473'))
        self.assertEqual(operaciones[0].isin, 'US71979Z7869')
        self.assertEqual(operaciones[0].tipo, TipoOperacion.COMPRA)
        self.assertEqual(operaciones[0].fecha, date(2024,3,27))
        self.assertEqual(operaciones[1].isin, 'US72554V4086')
        self.assertEqual(operaciones[1].cantidad, 10)
        self.assertEqual(operaciones[1].precio_unitario, Decimal('17.62'))
        self.assertEqual(operaciones[1].importe_neto, Decimal('176.2'))
        self.assertEqual(operaciones[1].tipo, TipoOperacion.VENTA)
        self.assertEqual(operaciones[1].fecha, date(2024,3,27))

    def test_play(self):
        self.assertEqual(date(2024,3,27), parse_evo_date("2024-03-27"))


if __name__ == '__main__':
    unittest.main()
