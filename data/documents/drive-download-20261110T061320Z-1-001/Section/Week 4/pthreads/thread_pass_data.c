#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define NUM_THREADS 5

typedef struct args_struct{
    char message[100];
    int thread_no;
}args_struct;

void *print_message(void *arguments){
    args_struct *args = (args_struct*) arguments;
    printf("<Message> %s from <Thread> #%d! with <ID> %ld\n", args->message, args->thread_no, pthread_self());
    pthread_exit(NULL);
}

int main (int argc, char *argv[]) {
    pthread_t threads[NUM_THREADS];
    args_struct args_arr[NUM_THREADS];

    char *messages[] = {"RED", "GREEN", "BLUE", "YELLOW", "BLACK"};
    int i;
    for(i=0; i<NUM_THREADS; i++){
        /* Initialize the arguments struct for each thread */
        strcpy(args_arr[i].message, messages[i]);
        args_arr[i].thread_no = i;

        printf("In main: creating thread #%d\n", i);
        pthread_create(&threads[i], NULL, print_message, &args_arr[i]);
    }

    /* Wait for each thread to finish and join */
    for(i=0; i<NUM_THREADS; i++){
        pthread_join(threads[i], NULL);
    }

    return 0;
}
