import unittest
from unittest.mock import patch
import typewise_alert

class TypewiseTest(unittest.TestCase):
    def test_infers_breach_as_per_limits(self):
        self.assertEqual(typewise_alert.infer_breach(20, 50, 100), 'TOO_LOW')
        self.assertEqual(typewise_alert.infer_breach(75, 50, 100), 'NORMAL')
        self.assertEqual(typewise_alert.infer_breach(150, 50, 100), 'TOO_HIGH')

    def test_classifies_temperature_breach(self):
        self.assertEqual(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', 20), 'NORMAL')
        self.assertEqual(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', 40), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 46), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', 39), 'NORMAL')

    @patch('sys.stdout')
    def test_check_and_alert_to_controller(self, mock_stdout):
        typewise_alert.check_and_alert('TO_CONTROLLER', {'coolingType': 'PASSIVE_COOLING'}, 40)
        output = mock_stdout.getvalue().strip()
        self.assertIn('65261, TOO_HIGH', output)

    @patch('sys.stdout')
    def test_check_and_alert_to_email(self, mock_stdout):
        typewise_alert.check_and_alert('TO_EMAIL', {'coolingType': 'PASSIVE_COOLING'}, 0)
        output = mock_stdout.getvalue().strip()
        self.assertIn('To: a.b@c.com', output)
        self.assertIn('Hi, the temperature is too low', output)

if __name__ == '__main__':
    unittest.main()
