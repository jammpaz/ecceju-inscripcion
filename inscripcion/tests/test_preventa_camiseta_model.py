import unittest
import uuid
from domain.models import PreventaCamiseta
from datetime import date


class PreventaCamisetaTestCase(unittest.TestCase):

    def test_field_names(self):
        self.assertEquals(PreventaCamiseta.fields_names(),
                          ['Cédula',
                           'Nombres Completos',
                           'Localidad',
                           'Color',
                           'Talla',
                           'Cantidad',
                           'Fecha Depósito',
                           'Número Depósito',
                           'Identificador'])

    def test_field_values(self):
        id = uuid.uuid1()
        nombres_completos = 'Desconocido'
        localidad = 'Desconocido'
        color = 'blanco'
        talla = '34'
        cantidad = 1
        fecha_deposito = date.today()
        numero_deposito = 'Desconocido'
        cedula = '0000000000'
        preventa = PreventaCamiseta(id=id,
                                    nombres_completos=nombres_completos,
                                    localidad=localidad,
                                    color=color,
                                    talla=talla,
                                    cantidad=cantidad,
                                    fecha_deposito=fecha_deposito,
                                    numero_deposito=numero_deposito,
                                    cedula=cedula)

        self.assertEquals(preventa.fields_values(),
                          [cedula,
                           nombres_completos,
                           localidad,
                           color,
                           talla,
                           cantidad,
                           fecha_deposito,
                           numero_deposito,
                           id])
