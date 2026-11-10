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
	else if(pid1 > 0 && pid2 > 0){    //Original parent process
		printf("[ORIGINAL PARENT] with <PID=%d> and <PPID:%d>, (pid1=%d pid2=%d)\n", getpid(), getppid(), pid1, pid2);
		wait(NULL);
	}
	else if(pid1 == 0 && pid2 > 0){    // Child created by first fork only
		printf("This is [CHILD created by FIRST fork only] with <PID:%d> and <PPID:%d>, (pid1=%d pid2=%d)\n", getpid(), getppid(), pid1, pid2);
		wait(NULL);
	}
	else if(pid1 > 0 && pid2 == 0){    // Child created by second fork
        printf("This is [CHILD created by SECOND fork only] with <PID=%d> and <PPID:%d>, (pid1=%d pid2=%d)\n", getpid(), getppid(), pid1, pid2);
        wait(NULL);
	}
	else{     // Child created by both forks
		printf("This is Child created by both forks with <PID:%d> and <PPID:%d>, (pid1=%d pid2=%d)\n", getpid(), getppid(), pid1, pid2);
		wait(NULL);
	}
return 0;
}
