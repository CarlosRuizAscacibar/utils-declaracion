import unittest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app import app


class TestInvestorDataRoute(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('subprocess.run')
    def test_get_investor_data_success(self, mock_subprocess):
        # Mock successful execution of both scripts
        mock_orders_result = MagicMock()
        mock_orders_result.returncode = 0
        mock_orders_result.stdout = 'Orders processed successfully'
        mock_orders_result.stderr = ''

        mock_movements_result = MagicMock()
        mock_movements_result.returncode = 0
        mock_movements_result.stdout = 'Movements processed successfully'
        mock_movements_result.stderr = ''

        mock_subprocess.side_effect = [mock_orders_result, mock_movements_result]

        # Test the route
        response = self.app.post('/get_investor_data',
                               data=json.dumps({'username': 'testuser', 'password': 'testpass'}),
                               content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('output', data)
        self.assertEqual(data['message'], 'MyInvestor data retrieved successfully')

        # Verify subprocess calls
        self.assertEqual(mock_subprocess.call_count, 2)
        calls = mock_subprocess.call_args_list

        # Check orders script call
        orders_call = calls[0]
        self.assertIn('get_my_investor_orders.py', orders_call[0][0])
        self.assertIn('--username', orders_call[0][0])
        self.assertIn('testuser', orders_call[0][0])
        self.assertIn('--password', orders_call[0][0])
        self.assertIn('testpass', orders_call[0][0])

        # Check movements script call
        movements_call = calls[1]
        self.assertIn('get_my_investor_movements.py', movements_call[0][0])
        self.assertIn('--username', movements_call[0][0])
        self.assertIn('testuser', movements_call[0][0])
        self.assertIn('--password', movements_call[0][0])
        self.assertIn('testpass', movements_call[0][0])

    @patch('subprocess.run')
    def test_get_investor_data_orders_failure(self, mock_subprocess):
        # Mock orders script failure
        mock_orders_result = MagicMock()
        mock_orders_result.returncode = 1
        mock_orders_result.stdout = ''
        mock_orders_result.stderr = 'Orders script error'

        mock_movements_result = MagicMock()
        mock_movements_result.returncode = 0
        mock_movements_result.stdout = 'Movements processed successfully'
        mock_movements_result.stderr = ''

        mock_subprocess.side_effect = [mock_orders_result, mock_movements_result]

        response = self.app.post('/get_investor_data',
                               data=json.dumps({'username': 'testuser', 'password': 'testpass'}),
                               content_type='application/json')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('Orders error:', data['error'])

    def test_get_investor_data_missing_credentials(self):
        # Test missing username
        response = self.app.post('/get_investor_data',
                               data=json.dumps({'password': 'testpass'}),
                               content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Username and password are required')

        # Test missing password
        response = self.app.post('/get_investor_data',
                               data=json.dumps({'username': 'testuser'}),
                               content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Username and password are required')

    def test_get_investor_data_invalid_json(self):
        # Test invalid JSON
        response = self.app.post('/get_investor_data',
                               data='invalid json',
                               content_type='application/json')

        self.assertEqual(response.status_code, 400)  # Flask should handle this


if __name__ == '__main__':
    unittest.main()