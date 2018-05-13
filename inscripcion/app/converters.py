import uuid

class UUIDUrlConverter():

    def to_python(self, value):
        return uuid.UUID(value)

    def to_url(self, values):
        return str(values)
