import unittest
import uuid
from app.converters import UUIDUrlConverter


class UUIDUrlConverterTestCase(unittest.TestCase):

    def test_to_python_from_string_to_uuid(self):
        converter = UUIDUrlConverter()
        expected_value = uuid.uuid1()

        actual_value = converter.to_python(str(expected_value))

        self.assertEqual(expected_value, actual_value)

    def test_to_url_from_uuid_to_string(self):
        converter = UUIDUrlConverter()
        uuid_value = uuid.uuid1()
        expected_value = str(uuid_value)

        actual_value = converter.to_url(uuid_value)

        self.assertEqual(expected_value, actual_value)
