import os
from servicios.lector_fichero_corriente_evo import leer_excel_corriente_evo
import unittest
from modelos.movimiento_corriente import MovimientoCorriente
from modelos.broker import BrokerEnum
from decimal import Decimal
from modelos.tipo_operacion import TipoOperacion
from datetime import date, datetime

import sys
sys.path.append("../../..")

class TestLecturaFicheroCorrienteEvo(unittest.TestCase):
    
    def test_lectura_archivo_banco(self):
        ruta_ejemplo_fichero_evo = os.path.join(os.path.dirname(__file__),'..', 'data', 'movimiento_bancario_evo.xls')
        operaciones: list[MovimientoCorriente] = leer_excel_corriente_evo(ruta_ejemplo_fichero_evo, banco="evo")
        self.assertEqual(len(operaciones), 1, "Debería leer 1 operaciones")
        self.assertEqual(operaciones[0].banco, "evo")
        self.assertEqual(operaciones[0].importe, Decimal('-11.50'))
        self.assertEqual(operaciones[0].fecha_contable, date(2024,6,7))
        self.assertEqual(operaciones[0].fecha_valor, date(2024,6,7))
        self.assertEqual(operaciones[0].concepto,"CARGO BIZUM - BIZUM")

if __name__ == '__main__':
    unittest.main()
