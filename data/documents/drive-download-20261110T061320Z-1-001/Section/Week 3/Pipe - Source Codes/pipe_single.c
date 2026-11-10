#include<stdlib.h>
#include<stdio.h>
#include<unistd.h>

#define MSG_SIZE 17
#define R 0
#define W 1

int main(){

    char *message = "Hello from pipe!";
    char in_buffer[MSG_SIZE];
    int pipefd[2];

    if(pipe(pipefd) < 0){
        perror("pipe error!\n");
        exit(1);
    }
    // No errors
    write(pipefd[W], message, MSG_SIZE);
    read(pipefd[R], in_buffer, MSG_SIZE);
    printf("Data read from pipe: \"%s\"\n", in_buffer);

return 0;
}
