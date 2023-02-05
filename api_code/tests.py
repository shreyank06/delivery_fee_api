import unittest
import json
from delivery_fee_api import app

class TestDeliveryFee(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def post_and_verify(self, data, delivery_fee):
        response = self.app.post('/delivery_fee', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['delivery_fee'], delivery_fee)

    def test_delivery_fee_for_large_delivery_distance(self):
        data = {
            'cart_value': 50,
            'delivery_distance': 20000,
            'number_of_items': 5,
            'time': '2023-01-31T15:00:00Z'
        }
        self.post_and_verify(data, 15)
    
    def test_delivery_fee_for_small_delivery_distance(self):
        data = {
            'cart_value': 50,
            'delivery_distance': 1000,
            'number_of_items': 5,
            'time': '2023-01-31T15:00:00Z'
        }
        self.post_and_verify(data, 2.5)

    def test_delivery_fee_min_value(self):
        data = {
            'cart_value': 120,
            'delivery_distance': 10000,
            'number_of_items': 5,
            'time': '2023-01-31T15:00:00Z'
        }
        self.post_and_verify(data, 0)

    def test_delivery_fee_for_non_rush_hour(self):
        data = {
            'cart_value': 50,
            'delivery_distance': 5000,
            'number_of_items': 5,
            'time': '2023-01-31T12:00:00Z'
        }
        self.post_and_verify(data, 10.5)

    def test_delivery_fee_for_rush_hour(self):
        data = {
            'cart_value': 50,
            'delivery_distance': 1000,
            'number_of_items': 5,
            'time': '2023-01-28T15:00:00Z'
        }
        self.post_and_verify(data, 2.5)

    def test_delivery_fee_for_small_order_value(self):
        data = {
            'cart_value': 5,
            'delivery_distance': 1000,
            'number_of_items': 5,
            'time': '2023-01-31T15:00:00Z'
        }
        self.post_and_verify(data, 7.5)

if __name__ == '__main__':
    unittest.main()
