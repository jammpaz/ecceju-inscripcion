class Inscripcion:
    def __init__(self, id, localidad, servidor, fecha, comprobante_uri = '', monto = 0.0):
        self.id = id
        self.localidad = localidad
        self.servidor = servidor
        self.monto = monto
        self.fecha = fecha
        self.comprobante_uri = comprobante_uri
        self.participantes = []

    def add_participante(self, participante):
        self.participantes.append(participante)

    def total_amount(self):
        from functools import reduce
        return reduce(lambda p1, p2: p1.monto + p2.monto, self.participantes)

class Participante:
    def __init__(self, id, nombres_completos, sexo, numero_deposito, telefono_contacto = '', monto = 0.0):
        self.id = id
        self.nombres_completos = nombres_completos
        self.sexo = sexo
        self.telefono_contacto = telefono_contacto
        self.monto = monto
        self.numero_deposito = numero_deposito
