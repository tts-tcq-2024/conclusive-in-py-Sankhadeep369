BATTERY_LIMITS = {
    "PASSIVE_COOLING": (0, 35),
    "HI_ACTIVE_COOLING": (0, 45),
    "MED_ACTIVE_COOLING": (0, 40),
}


def infer_breach(value, lower_limit, upper_limit):

    if value < lower_limit:
        return 'TOO_LOW'
    elif value > upper_limit:
        return 'TOO_HIGH'
    return 'NORMAL'


def classify_temperature_breach(cooling_type, temperature_in_c):

    lower_limit, upper_limit = BATTERY_LIMITS[cooling_type]
    return infer_breach(temperature_in_c, lower_limit, upper_limit)


def check_and_alert(alert_target, battery_char, temperature_in_c):

    breach_type = classify_temperature_breach(battery_char['coolingType'], temperature_in_c)

    alert_functions = {
        'TO_CONTROLLER': send_to_controller,
        'TO_EMAIL': send_to_email,
    }

    alert_functions[alert_target](breach_type)


def send_to_controller(breach_type):
    """
    Sends the breach type to the controller.
    """
    header = 0xfeed
    print(f'{header}, {breach_type}')


def send_to_email(breach_type):
    """
    Sends an email notification about the breach type.
    """
    recipient = "a.b@c.com"
    if breach_type == 'TOO_LOW':
        print(f'To: {recipient}')
        print('Hi, the temperature is too low')
    elif breach_type == 'TOO_HIGH':
        print(f'To: {recipient}')
        print('Hi, the temperature is too high')
