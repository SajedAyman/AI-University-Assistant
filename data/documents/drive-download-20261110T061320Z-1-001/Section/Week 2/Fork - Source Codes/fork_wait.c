#include<stdlib.h>
#include<unistd.h>
#include<stdio.h>
#include<sys/wait.h>
/*
    In this code the parent waits for the child
    and does not exit before child
*/
int main(){
    int status;
	printf("Before becoming a parent with <PID:%d> and <PPID:%d>\n", getpid(), getppid());
    // Forking the current process
	pid_t pid = fork();

	if(pid < 0){    // Error
		perror("Unable to fork the process\n");
		exit(1);
	}
	else if(pid == 0){    // Child
		printf("This is child: %d with <PID:%d>\n", pid, getpid());
		printf("My parent is process with <PID:%d>\n", getppid());
		printf("Child Exiting...\n");
	}
	else{    // Parent
		printf("This is parent with <PID:%d> and <PPID:%d>\n", getpid(), getppid());
		printf("My child is process with <PID:%d>\n", pid);
		printf("Parent waiting for child to return...\n");

        /* Waiting for child to exit */
		// wait(NULL);

		waitpid(pid, &status, 0);// 0 is blocking
		printf("Child exit status=%d\n", status);

        // waitpid(pid, &status, WNOHANG); // WNOHANG is non blocking, so the parent may again exit before child
        // printf("Child exit status=%d\n", status);

		printf("Parent Exiting...\n");
	}
return 0;
}
