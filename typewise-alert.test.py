import unittest
import typewise_alert

class TypewiseTest(unittest.TestCase):

    def test_infer_breach_as_per_limits(self):
        self.assertEqual(typewise_alert.infer_breach(20, 50, 100), 'TOO_LOW')
        self.assertEqual(typewise_alert.infer_breach(80, 50, 100), 'NORMAL')
        self.assertEqual(typewise_alert.infer_breach(55, 50, 100), 'NORMAL')

    def test_classify_temperature_breach(self):
        self.assertEqual(typewise_alert.classify_temperature_breach("PASSIVE_COOLING", 36), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach("HI_ACTIVE_COOLING", 46), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach("MED_ACTIVE_COOLING", 41), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach("PASSIVE_COOLING", 25), 'NORMAL')

    def test_check_and_alert(self):
        # Test with different alert targets and breach types
        battery_char = {'coolingType': 'PASSIVE_COOLING'}
        typewise_alert.check_and_alert('TO_CONTROLLER', battery_char, 40)
        typewise_alert.check_and_alert('TO_EMAIL', battery_char, 5)

if __name__ == '__main__':
    unittest.main()
