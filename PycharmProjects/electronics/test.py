import time

LEDs = {
    'LEDred': 18,
    'LEDblue': 22,
    'LEDgreen': 24,
    'LEDyellow': 26
    }

try:
    while True:
        for k, v in LEDs.items():
            print(f'{k} turned on >>>')
            time.sleep(1)
            print(f'{k} turned off <<<')
            time.sleep(1)
except KeyboardInterrupt:
    print("\nProgram terminated by user")
