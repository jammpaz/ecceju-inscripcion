class Inscripcion:
    def __init__(self, id, localidad, servidor, monto, fecha, comprobante_uri):
        self.id = id
        self.localidad = localidad
        self.servidor = servidor
        self.monto = monto
        self.fecha = fecha
        self.comprobante_uri = comprobante_uri
        self.participantes = []

    def addParticipante(self, participante):
        self.participantes.append(participante)

class Participante:
    def __init__(self, nombres_completos, sexo, telefono_contacto):
        self.nombres_completos = nombres_completos
        self.sexo = sexo
        self.telefono_contacto = telefono_contacto
