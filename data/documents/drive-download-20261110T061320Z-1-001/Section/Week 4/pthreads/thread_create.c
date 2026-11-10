#include <pthread.h>
#include <stdio.h>
/* Prints Xs. The parameter is unused. Does not return. */
void* print_xs(void* unused){
    int i;
    for(i=0; i<1000; i++)
        printf("X");
    printf("\n");
    return NULL;
}
/* The main program. */
int main () {
    pthread_t thread_id;
    /* Create a new thread. The new thread will run the print_xs
    function. */
    pthread_create (&thread_id, NULL, print_xs, NULL);
    /* Main thread prints 1000 Os*/
    int i;
    for(i=0; i<1000; i++)
        printf("O");

    printf("\n");
    /* If not called, the main thread may finish execution
    and terminate before waiting for other threads to finish */
    pthread_exit(NULL);
    return 0;
}
