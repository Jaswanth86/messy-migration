import unittest
from app import app, init_db

class UserApiTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        init_db()  # Reseed test DB

    def test_health_check(self):
        r = self.app.get('/')
        self.assertEqual(r.status_code, 200)

    def test_get_users(self):
        r = self.app.get('/users')
        self.assertEqual(r.status_code, 200)
        self.assertTrue(isinstance(r.get_json(), list))
# ... (add more for POST, DELETE, etc.)

if __name__ == "__main__":
    unittest.main()
