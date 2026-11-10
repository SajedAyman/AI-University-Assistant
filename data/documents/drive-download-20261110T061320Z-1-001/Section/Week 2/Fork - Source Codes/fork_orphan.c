#include<stdlib.h>
#include<unistd.h>
#include<stdio.h>
/*
    This code always produces an orphan process.
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
		// Make sure the parent process exits before child
		sleep(5);
		printf("Child Exiting...\n");
	}
	else{    // Parent
		printf("This is parent with <PID:%d> and <PPID:%d>\n", getpid(), getppid());
		printf("My child is process with <PID:%d>\n", pid);
		printf("Parent Exiting...\n");
	}
return 0;
}
