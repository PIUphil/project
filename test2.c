#include <stdio.h>
#include <wiringPi.h>

#define LED0 15
#define LED7 22
#define SW1 7
#define SW2 27

int main(void)
{
    if(wiringPiSetupGpio()==-1)
    return 1;

    pinMode(LED0, OUTPUT);
    pinMode(LED7, OUTPUT);
    pinMode(SW1, INPUT);
    pinMode(SW2, INPUT);


    while(TRUE)
    {
        if (digitalRead(SW1)==HIGH)
        {
            printf("LED0 HIGH\n");
            digitalWrite(LED0, HIGH);
            delay(1000);
        }
        else
        {
            //printf("LED LOW\n");
            digitalWrite(LED0, LOW);
            delay(1000);
        }


        if (digitalRead(SW2)==HIGH)
        {
            printf("LED7 HIGH\n");
            digitalWrite(LED7, HIGH);
            delay(1000);
        }
        else
        {
            //printf("LED LOW\n");
            digitalWrite(LED7, LOW);
            delay(1000);
        }
    }

    return 0;
}
