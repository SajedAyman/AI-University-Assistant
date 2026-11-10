#include<stdlib.h>
#include<unistd.h>
#include<stdio.h>
/*
    This code always produces a zombie process.
*/
int main(){
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
		// Make sure the parent does not accept the exit return code of its child
		sleep(60);
		printf("Parent Exiting...\n");
	}
return 0;
}
