import unittest

from app import app


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_all_prices(self):
        response = self.app.get('/price')
        self.assertEqual(response.status_code, 200)

    def test_get_all_prices_by_date(self):
        response = self.app.get('/price/2021-01-01')
        self.assertEqual(response.status_code, 200)

    def test_get_prices_by_commodity(self):
        response = self.app.get('/price/commodity/Bawang%20Merah')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
