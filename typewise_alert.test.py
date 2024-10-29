import unittest
from unittest.mock import patch
import typewise_alert

class TypewiseTest(unittest.TestCase):
    def test_infer_breach_as_per_limits(self):
        self.assertEqual(typewise_alert.infer_breach(20, 50, 100), 'TOO_LOW')
        self.assertEqual(typewise_alert.infer_breach(120, 50, 100), 'TOO_HIGH')
        self.assertEqual(typewise_alert.infer_breach(80, 50, 100), 'NORMAL')

    def test_classify_temperature_breach(self):
        self.assertEqual(typewise_alert.classify_temperature_breach("PASSIVE_COOLING", 36), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach("HI_ACTIVE_COOLING", 46), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach("MED_ACTIVE_COOLING", 41), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach("PASSIVE_COOLING", 25), 'NORMAL')
        
        # Check for ValueError with invalid cooling type
        with self.assertRaises(ValueError):
            typewise_alert.classify_temperature_breach("UNKNOWN_COOLING", 20)

@patch('builtins.print')
def test_check_and_alert(self, mock_print):
    battery_char = {'coolingType': 'PASSIVE_COOLING'}
    
    # Test controller alert for TOO_HIGH breach
    typewise_alert.check_and_alert('TO_CONTROLLER', battery_char, 40)
    mock_print.assert_any_call('65261, TOO_HIGH')

    # Test email alert for TOO_LOW breach
    typewise_alert.check_and_alert('TO_EMAIL', battery_char, 5)
    mock_print.assert_any_call('To: a.b@c.com')
    mock_print.assert_any_call('Hi, the temperature is too low')

if __name__ == '__main__':
    unittest.main()
