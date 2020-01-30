#include <time.h>
#include <stdio.h>
#include <unistd.h>

int main(void) {
	clock_t start = clock();
	sleep(5); 
	clock_t end = clock();
	double elapsed = (double) (end - start);

	printf("time was %d\n", elapsed / CLOCKS_PER_SEC);
	return 1; 

}
