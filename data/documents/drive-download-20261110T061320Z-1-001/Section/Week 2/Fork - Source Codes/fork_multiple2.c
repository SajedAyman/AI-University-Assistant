#include<stdlib.h>
#include<unistd.h>
#include<stdio.h>
#include<sys/wait.h>
/*
    This code spawns exactly 5 children.
*/

void do_some_work(){
    printf("[Child] process with <PID:%d> and <PPID:%d>\n", getpid(), getppid());
}

int main(){
    int i, nproc = 5;
	pid_t pids[5];

	printf("[Parent] process with <PID:%d> and <PPID:%d>\n", getpid(), getppid());

    /* Fork exactly 5 children */
    for(i=0; i<nproc; i++){
        pids[i] = fork();
        if(pids[i] < 0){
            perror("Unable to fork the process\n");
            exit(1);
        }
        else if(pids[i] == 0){  // Child
            do_some_work();
            exit(0);
        }
        else {  // Parent
            wait(NULL);
        }
    }

return 0;
}
