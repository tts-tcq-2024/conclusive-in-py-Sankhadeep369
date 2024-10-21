# Refactored typewise_alert.py
COOLING_LIMITS = {
    'PASSIVE_COOLING': (0, 35),
    'HI_ACTIVE_COOLING': (0, 45),
    'MED_ACTIVE_COOLING': (0, 40)
}

ALERT_TARGETS = {
    'TO_CONTROLLER': 'send_to_controller',
    'TO_EMAIL': 'send_to_email'
}

def infer_breach(value, lower_limit, upper_limit):
    if value < lower_limit:
        return 'TOO_LOW'
    if value > upper_limit:
        return 'TOO_HIGH'
    return 'NORMAL'


def classify_temperature_breach(cooling_type, temperature):
    if cooling_type not in COOLING_LIMITS:
        raise ValueError(f"Unknown cooling type: {cooling_type}")
    lower_limit, upper_limit = COOLING_LIMITS[cooling_type]
    return infer_breach(temperature, lower_limit, upper_limit)


def check_and_alert(alert_target, battery_char, temperature):
    breach_type = classify_temperature_breach(battery_char['coolingType'], temperature)
    if alert_target in ALERT_TARGETS:
        globals()[ALERT_TARGETS[alert_target]](breach_type)
    else:
        raise ValueError(f"Unknown alert target: {alert_target}")


def send_to_controller(breach_type):
    header = 0xfeed
    print(f'{header}, {breach_type}')


def send_to_email(breach_type):
    recepient = "a.b@c.com"
    if breach_type == 'TOO_LOW':
        print(f'To: {recepient}\nHi, the temperature is too low')
    elif breach_type == 'TOO_HIGH':
        print(f'To: {recepient}\nHi, the temperature is too high')


# Reflect the refactored and cleaner code handling more cases with less complexity
