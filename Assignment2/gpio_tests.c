# include <wiringPi.h>

void run_led(int pin);

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
		}
	}
	return 0;
}

void run_led(int pin) {
	digitalWrite(pin, HIGH);
}
