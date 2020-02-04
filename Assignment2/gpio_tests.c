#include <wiringPi.h>
#include <stdlib.h>
#include <sys/time.h>
#include <stdio.h>

void run_led(int pin);
struct timeval t1, t2;


int main (void) {
	wiringPiSetup();
	pinMode(0, OUTPUT); //pwr to led
	pinMode(2, INPUT); //button input

	for(;;) {
		int button = digitalRead(2);
		if (button) {
			run_led(0);
			delay(500);
			digitalWrite(0, LOW);
			break;
		}
	}
	return 0;
}

void run_led(int pin) {
	digitalWrite(pin, HIGH);
	gettimeofday(&t1, NULL);
	unsigned long init = 1000000 * t1.tv_sec + t1.tv_usec;
	system("raspistill -o testimg2.jpg -t 1 -h 64 -w 64 -n");
	gettimeofday(&t2, NULL);
	unsigned long aft = 1000000 * t2.tv_sec + t2.tv_usec;
	printf("Time to take picture: %lu ms\n", aft-init);
}

