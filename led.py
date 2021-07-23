from wiringpi import wiringPiSetupGpio, digitalWrite, pinMode, delay
from wiringpi import OUTPUT, HIGH, LOW

LEDS = [15, 16, 17, 6, 19, 20, 21, 22]


def main():
    wiringPiSetupGpio()
    
    for i in LEDS:
        pinMode(i, OUTPUT)

    for i in LEDS:
        digitalWrite(i, HIGH)        # HIGH = 1
    
    delay(2000)

    for i in LEDS: 
        digitalWrite(i, LOW)


if __name__ == "__main__":
    main()
