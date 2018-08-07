import unittest
import os
from flask import current_app
from app import create_app, db
from app.email import send_email
from config import config


class EmailIntTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app.template_folder = f"{os.getcwd()}/tests"
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_send_email(self):
        to_email = 'ecceju.rccec.org@gmail.com'
        subject = 'Testing email'
        template_path = 'template_email'
        user = 'User Test'
        reply = 'Do not reply'

        response = send_email(
            to_email,
            subject,
            template_path,
            user=user,
            reply=reply
        )

        self.assertIsNotNone(response)
