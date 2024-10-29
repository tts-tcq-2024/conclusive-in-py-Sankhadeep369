import unittest
import typewise_alert

class TypewiseTest(unittest.TestCase):
    def test_infer_breach_as_per_limits(self):
        # Test boundaries and NORMAL cases
        self.assertEqual(typewise_alert.infer_breach(20, 50, 100), 'TOO_LOW')
        self.assertEqual(typewise_alert.infer_breach(80, 50, 100), 'TOO_HIGH')
        self.assertEqual(typewise_alert.infer_breach(55, 50, 100), 'NORMAL')

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

    def test_check_and_alert(self):
        battery_char = {'coolingType': 'PASSIVE_COOLING'}
        
        # Test controller alert for TOO_HIGH breach
        with self.assertLogs() as captured:
            typewise_alert.check_and_alert('TO_CONTROLLER', battery_char, 40)
            self.assertIn('65261, TOO_HIGH', captured.output[0])

        # Test email alert for TOO_LOW breach
        with self.assertLogs() as captured:
            typewise_alert.check_and_alert('TO_EMAIL', battery_char, 5)
            self.assertIn('To: a.b@c.com', captured.output[0])
            self.assertIn('Hi, the temperature is too low', captured.output[1])

        # Test normal condition email
        with self.assertLogs() as captured:
            typewise_alert.check_and_alert('TO_EMAIL', battery_char, 30)
            self.assertIn('To: a.b@c.com', captured.output[0])
            self.assertIn('Hi, the temperature is normal', captured.output[1])

        # Invalid alert target
        with self.assertRaises(ValueError):
            typewise_alert.check_and_alert('TO_SMS', battery_char, 30)

if __name__ == '__main__':
    unittest.main()
