#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

/*
 * Using fork to create child process to perform functionality
 * Using main process to time the process execution, using the
 * pid saved by child process, main process kills execution after
 * 20 seconds
 *
 * Expanded upon initial setup to allow command line args input,
 * Using cmd line args to determine time waiting 
 */
int main(int argc, char *argv[]){
	// Process ID
	int pid, child_pid, sleep_time_arg;
	int count = 0;
	char buff[128],file_name[128],buff1[128];

	// Cmd line args processing
	for( int i=0; i < argc; i++ ){
		if( i == 1 ){
			strcpy(file_name, argv[i]);
			// printf("%s\n",file_name);
			
			sprintf(buff, "bash data_collection.sh %s", file_name);
			// system(buff);
			// system("bash data_collection.sh");
		}
		else if( i == 2 ){
			sleep_time_arg = atoi(argv[i]);
		}
	}
	
	// New process created
	pid = fork();

	// Child process
	if( pid == 0 ){
		child_pid = getpid();
		
		// Opening/Creating a file to save the pid of the child process
		FILE *file;
		file = fopen("child_process_id.txt", "w");

		if( file != NULL ){
			fprintf(file, "%d", child_pid);
		}
		fclose(file);
		
		/*
		while(1){
			count++;
			printf("Child process #%d, PID: %d\n", count, child_pid);
			sleep(1);
		}*/
		system(buff);
		exit(0);
	}
	else{
		sleep(sleep_time_arg);
		int pid_kill = 0;
		
		// Opening the file to read the child process ID 
		FILE *file;
		file = fopen("child_process_id.txt", "r");
		
		if ( file != NULL ){
			fscanf(file, "%d", &pid_kill);
		}
		fclose(file);
		
		printf("Main process obtaining child process ID: %d\n", pid_kill);
		// kill(pid_kill, SIGINT);
		kill(pid_kill, 0);
		printf("Exit main process\n");
		
		remove("child_process_id.txt");
		sleep(2);
		
		printf("Completed process");
		exit(0);
	}
	return EXIT_SUCCESS;
}
