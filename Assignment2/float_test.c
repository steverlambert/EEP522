#include <stdio.h>

int main(void) {
	float num = 5.167;
	float x;
	int steps = 0;
	for (int i = 0; i < 500000000; i++) {
		x = num / 1.4;
		steps++;
	}

	printf("Program finished, iters = %d\n", steps);
	return 1; 

}
