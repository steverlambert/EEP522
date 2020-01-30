#include <stdio.h>

int main(void) {
	int num = 20;
	int steps = 0;
	int x;
	for (int i = 0; i < 500000000; i++) {
		x = num / 5;
		steps++;
	}

	printf("Program finished, iters = %d\n", steps);
	return 1; 
}
