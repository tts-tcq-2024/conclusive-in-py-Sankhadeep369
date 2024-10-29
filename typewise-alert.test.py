import unittest
import typewise_alert


class TypewiseTest(unittest.TestCase):
    def test_infers_breach_as_per_limits(self):
        self.assertEqual(typewise_alert.infer_breach(20, 50, 100), 'TOO_LOW')
        self.assertEqual(typewise_alert.infer_breach(80, 50, 100), 'TOO_HIGH')
        self.assertEqual(typewise_alert.infer_breach(55, 50, 100), 'NORMAL')

    def test_classify_temperature_breach(self):
        self.assertEqual(typewise_alert.classify_temperature_breach("PASSIVE_COOLING", 36), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach("HI_ACTIVE_COOLING", 46), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach("MED_ACTIVE_COOLING", 41), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach("PASSIVE_COOLING
