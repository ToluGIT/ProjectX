import unittest
from user_service_env.app import app

class UserServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_register_user(self):
        response = self.app.post('/users/register', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', response.get_data(as_text=True))

    def test_login_user(self):
        # Register user first
        self.app.post('/users/register', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        # Login
        response = self.app.post('/users/login', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
