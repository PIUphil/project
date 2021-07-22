#include <stdio.h>
#include <wiringPi.h>

#define LED 20

int main(void)
{
    if(wiringPiSetupGpio()==-1)
    return 1;

    pinMode(LED, OUTPUT);

    while(TRUE)
    {
        printf("LED HIGH\n");
        digitalWrite(LED, HIGH);
        delay(1000);


        printf("LED LOW\n");
        digitalWrite(LED, LOW);
        delay(1000);
    }

    return 0;
}
