#include<stdlib.h>
#include<unistd.h>
#include<stdio.h>
#include<sys/wait.h>
/*
    This code does not work as you might expect.
    When a process spawns a child process, the two
    processes continue executing after the fork statement.
*/
int main(){
    // Forking the current process
	pid_t pid1, pid2;
	pid1 = fork();
	pid2 = fork();
    // Four processes now exist with (pid1 = 0) in only one of the which is the first generation child
	if(pid1 < 0 || pid2 < 0){    // Error
		perror("Unable to fork the process\n");
		exit(1);
	}
	else if(pid1 == 0){    // First Child
		printf("This is the <FIRST> child with <PID=%d> and <PPID:%d>, (pid1=%d pid2=%d)\n", getpid(), getppid(), pid1, pid2);
		wait(NULL);
	}
	else{    // First Child's Parent
		printf("This is <FIRST_CHILD> parent with <PID:%d> and <PPID:%d>, (pid1=%d pid2=%d)\n", getpid(), getppid(), pid1, pid2);
		wait(NULL);
	}
	if(pid2 == 0){    // Second Child
        printf("This is the <SECOND> child with <PID=%d> and <PPID:%d>, (pid1=%d pid2=%d)\n", getpid(), getppid(), pid1, pid2);
        wait(NULL);
	}
	else{    // Second Child's Parent
		printf("This is <SECOND_CHILD> parent with <PID:%d> and <PPID:%d>, (pid1=%d pid2=%d)\n", getpid(), getppid(), pid1, pid2);
		wait(NULL);
	}
return 0;
}
