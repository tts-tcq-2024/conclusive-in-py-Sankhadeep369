# Constants for limits based on cooling type
cooling_limits = {
    'PASSIVE_COOLING': (0, 35),
    'HI_ACTIVE_COOLING': (0, 45),
    'MED_ACTIVE_COOLING': (0, 40)
}

def infer_breach(value, lowerLimit, upperLimit):
    if value < lowerLimit:
        return 'TOO_LOW'
    if value > upperLimit:
        return 'TOO_HIGH'
    return 'NORMAL'

def classify_temperature_breach(coolingType, temperatureInC):
    limits = cooling_limits.get(coolingType, (0, 0))  # default is 0,0 for unknown types
    return infer_breach(temperatureInC, limits[0], limits[1])

# Strategy pattern for alerting mechanism
def check_and_alert(alertTarget, batteryChar, temperatureInC):
    breachType = classify_temperature_breach(batteryChar['coolingType'], temperatureInC)
    alert_handlers = {
        'TO_CONTROLLER': send_to_controller,
        'TO_EMAIL': send_to_email
    }
    # Dispatch to the appropriate alert handler
    alert_handlers.get(alertTarget, lambda x: None)(breachType)

def send_to_controller(breachType):
    header = 0xfeed
    print(f'{header}, {breachType}')

def send_to_email(breachType):
    recepient = "a.b@c.com"
    message = {
        'TOO_LOW': 'Hi, the temperature is too low',
        'TOO_HIGH': 'Hi, the temperature is too high',
    }
    if breachType in message:
        print(f'To: {recepient}')
        print(message[breachType])
