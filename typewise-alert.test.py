import unittest
from unittest.mock import patch
import typewise_alert

class TypewiseTest(unittest.TestCase):
    def test_infer_breach_as_per_limits(self):
        # Test boundaries and NORMAL cases
        self.assertEqual(typewise_alert.infer_breach(20, 50, 100), 'TOO_LOW')
        self.assertEqual(typewise_alert.infer_breach(120, 50, 100), 'TOO_HIGH')
        self.assertEqual(typewise_alert.infer_breach(80, 50, 100), 'NORMAL')  # Corrected expected output

    def test_classify_temperature_breach(self):
        # High temperature breaches
        self.assertEqual(typewise_alert.classify_temperature_breach("PASSIVE_COOLING", 36), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach("HI_ACTIVE_COOLING", 46), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach("MED_ACTIVE_COOLING", 41), 'TOO_HIGH')
        
        # Normal temperatures
        self.assertEqual(typewise_alert.classify_temperature_breach("PASSIVE_COOLING", 25), 'NORMAL')
        self.assertEqual(typewise_alert.classify_temperature_breach("HI_ACTIVE_COOLING", 35), 'NORMAL')
        self.assertEqual(typewise_alert.classify_temperature_breach("MED_ACTIVE_COOLING", 38), 'NORMAL')
        
        # Invalid cooling type
        with self.assertRaises(ValueError):
            typewise_alert.classify_temperature_breach("UNKNOWN_COOLING", 20)

    @patch('sys.stdout')  # Mock sys.stdout for capturing print output
    def test_check_and_alert(self, mock_stdout):
        battery_char = {'coolingType': 'PASSIVE_COOLING'}
        
        # Test controller alert for TOO_HIGH breach
        typewise_alert.check_and_alert('TO_CONTROLLER', battery_char, 40)
        output = mock_stdout.getvalue().strip().splitlines()
        self.assertIn('65261, TOO_HIGH', output[0])

        # Test email alert for TOO_LOW breach
        typewise_alert.check_and_alert('TO_EMAIL', battery_char, 5)
        output = mock_stdout.getvalue().strip().splitlines()
        self.assertIn('To: a.b@c.com', output[1])
        self.assertIn('Hi, the temperature is too low', output[2])

        # Test normal condition email
        typewise_alert.check_and_alert('TO_EMAIL', battery_char, 30)
        output = mock_stdout.getvalue().strip().splitlines()
        self.assertIn('To: a.b@c.com', output[3])
        self.assertIn('Hi, the temperature is normal', output[4])

        # Invalid alert target
        with self.assertRaises(ValueError):
            typewise_alert.check_and_alert('TO_SMS', battery_char, 30)

if __name__ == '__main__':
    unittest.main()
