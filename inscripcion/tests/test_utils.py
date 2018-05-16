import unittest
from utils.security import PasswordManager

class PasswordManagerTestCase(unittest.TestCase):

    def test_hashed_password_should_not_be_none(self):
        plain_password = 'super secret pass'
        hashed_password = PasswordManager(plain_password).hash()
        self.assertTrue(hashed_password is not None)

    def test_password_verification(self):
        plain_password = 'super secret pass'
        hashed_password = PasswordManager(plain_password).hash()
        is_valid = PasswordManager(plain_password).check_with(hashed_password)
        self.assertTrue(is_valid)
        is_valid = PasswordManager('wrong pass').check_with(hashed_password)
        self.assertFalse(is_valid)

    def test_password_salts_are_random(self):
        plain_password = 'super secret pass'
        hashed_password_1 = PasswordManager(plain_password).hash()
        hashed_password_2 = PasswordManager(plain_password).hash()
        self.assertTrue(hashed_password_1 != hashed_password_2)
