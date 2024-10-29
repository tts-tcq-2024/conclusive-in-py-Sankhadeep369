import unittest
import typewise_alert


class TestTypewiseAlert(unittest.TestCase):

    def test_infer_breach(self):
        self.assertEqual(typewise_alert.infer_breach(20, 50, 100), 'TOO_LOW')
        self.assertEqual(typewise_alert.infer_breach(120, 50, 100), 'TOO_HIGH')
        self.assertEqual(typewise_alert.infer_breach(60, 50, 100), 'NORMAL')

    def test_classify_temperature_breach(self):
        self.assertEqual(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', 20), 'NORMAL')
        self.assertEqual(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 46), 'TOO_HIGH')
        self.assertEqual(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', -1), 'TOO_LOW')
        with self.assertRaises(ValueError):
            typewise_alert.classify_temperature_breach('UNKNOWN_COOLING', 20)

    def test_check_and_alert(self):
        battery_char = {'coolingType': 'PASSIVE_COOLING'}
        with self.assertRaises(ValueError):
            typewise_alert.check_and_alert('UNKNOWN_TARGET', battery_char, 25)

        typewise_alert.check_and_alert('TO_CONTROLLER', battery_char, 20)  # This should print the alert to controller
        typewise_alert.check_and_alert('TO_EMAIL', battery_char, 40)  # This should send a TOO_HIGH alert to email

    def test_send_to_controller(self):
        with self.assertLogs() as captured:
            typewise_alert.send_to_controller('TOO_HIGH')
        self.assertIn('0xfeed, TOO_HIGH', captured.output[0])

    def test_send_to_email(self):
        with self.assertLogs() as captured:
            typewise_alert.send_to_email('TOO_HIGH')
        self.assertIn('Hi, the temperature is too high', captured.output[0])

if __name__ == '__main__':
    unittest.main()
