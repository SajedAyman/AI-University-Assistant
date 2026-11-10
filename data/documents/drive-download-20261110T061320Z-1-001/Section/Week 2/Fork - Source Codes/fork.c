#include<stdlib.h>
#include<unistd.h>
#include<stdio.h>
/*
    This code might produce an orphan process.
    If the parent exits before its child, the
    child becomes an orphan process and is adopted
    by the init process with PID=1
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
		printf("Parent Exiting...\n");
	}
return 0;
}
