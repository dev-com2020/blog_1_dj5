from django.test import TestCase
from unittest.mock import patch
from types import SimpleNamespace
import tempfile
import os
import sqlite3 as py_sqlite3

# Import the module after patching in setUp

class GenerateQuestionsTests(TestCase):
    def setUp(self):
        # temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()

        # Patch sqlite3.connect used in services module
        real_connect = py_sqlite3.connect
        patcher_db = patch('quiz_app.services.sqlite3.connect',
                           side_effect=lambda *args, **kwargs: real_connect(self.db_path))
        self.mock_connect = patcher_db.start()
        self.addCleanup(patcher_db.stop)

        # Patch OpenAI call to avoid network
        patcher_ai = patch('quiz_app.services.client.chat.completions.create')
        self.mock_ai = patcher_ai.start()
        self.mock_ai.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content='q1'))]
        )
        self.addCleanup(patcher_ai.stop)

        # Import services after patches are in place
        from quiz_app import services
        self.services = services

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_keys_unique_per_topic(self):
        self.services.generate_questions('history')
        self.services.generate_questions('history')
        rows = self.services.print_all_questions()
        keys = [row[1] for row in rows]
        self.assertEqual(len(keys), len(set(keys)))

    def test_insert_does_not_raise(self):
        try:
            self.services.generate_questions('geography')
        except Exception as exc:
            self.fail(f'generate_questions raised {exc}')
        rows = self.services.print_all_questions()
        self.assertEqual(len(rows), 1)

