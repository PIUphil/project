#include <wiringPi.h>

const int LEDS[] = {15, 16, 17, 6, 19, 20, 21, 22};

int main()
{
    wiringPiSetupGpio();
    
    for(int i=0 ; i<sizeof(LEDS)/sizeof(LEDS[0]) ; ++i) {
        pinMode(LEDS[i], OUTPUT);    
    }

    // for(int i=0 ; i<8 ; ++i) {
    //     digitalWrite(LEDS[i], HIGH);        // HIGH = 1
    //     delay(100);
    //     digitalWrite(LEDS[i], LOW);
    //     delay(50);
    // }

    // for(int i=0 ; i<sizeof(LEDS)/sizeof(LEDS[0]) ; ++i) {
    for(int i=0 ; i<8 ; ++i) {
        digitalWrite(LEDS[i], HIGH);        // HIGH = 1
    }
    delay(2000);

    for(int i=0 ; i<8 ; ++i) {  
        digitalWrite(LEDS[i], LOW);
    }

    return 0;
}
