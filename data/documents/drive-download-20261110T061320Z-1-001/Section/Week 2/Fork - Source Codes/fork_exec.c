#include<stdlib.h>
#include<unistd.h>
#include<stdio.h>
#include<sys/wait.h>
/*
    exec() functions may be used to replace the child's
    process image with another process image.
    // Versions without p
    execl() -> L means it will receive the command line arguments as a list
    execv() -> V means it will receive the command line arguments as an array (vector)
    // Versions with p
    execlp()
    execvp()

    The versions with 'p' in there use the environment path variable to search for
    the executable file named to execute. The versions without the 'p' require an absolute or
    relative file path to be prepended to the filename of the executable if it is not in the current working directory.
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
		printf("Executing ls -a...\n");
		char *argv[] = {"ls", "-a", NULL};
		//execv("/bin/ls", argv);
		execvp("ls", argv);
		printf("Child Exiting...\n");
	}
	else{    // Parent
        int status;
		printf("This is parent with <PID:%d> and <PPID:%d>\n", getpid(), getppid());
		printf("My child is process with <PID:%d>\n", pid);
		// Waiting for child to exit
		waitpid(pid, &status, 0);// 0 is blocking
		printf("Child exit status=%d\n", status);

		printf("Parent Exiting...\n");
	}
return 0;
}
