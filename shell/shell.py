import os, sys, time, re

input = ''
instant = ''
og_path = os.getcwd()
current_path = og_path




def program_fork(command, args):
    if(os.system(f'command -v {command} > /dev/null 2>&1') != 0): #if command does not exist
        os.write(1, 'invalid command!\n')
        return

    pid = os.fork()

    if pid == 0:
        os.execvpe(command, args, os.environ)

    else:
        os.wait()


#######################################################################################################

def pipe_handler(input, length):   ##needs to recieve an input value and pipe it to next program

    os.write(1, "pipe_handler activated!!\n".encode())

    if length == 0:
        return

    

    pid = os.fork()

    if pid != 0:  ##shell program
        os.wait()
        return

    iFd, oFd = os.pipe()

    pid = os.fork()

    if pid == 0:
        os.close(oFd)
        os.dup2(iFd, 0) ##duplicates stdin
        os.close(iFd)

        os.execvpe(input[1][0], input[1][0:], os.environ)

    else: 
         os.close(iFd)
         os.dup2(oFd, 1) ##duplicates stdout
         os.close(oFd)
         
         os.execvpe(input[0][0], input[0][0:], os.environ)

         os.wait()
            
    
    return
    



#######################################################################################################
############################ handles input

def command_handler(input, current_path):
    input = input.split('|')  ##seperates for potential piping

    for index in range(len(input)):
        input[index] = input[index].split(" ")
        if len(input) > 1:
            input[index].remove('')

    k = 0


    while (k < len(input)):
        if input[k][0] == 'cd' and len(input[k]) > 1:       #handles directory changes
            if input[k][1] == '..':
                if os.path.dirname(current_path):
                    current_path = os.path.dirname(current_path)
                    return current_path
                else:
                    os.write(1, "directory change not valid\n".encode())
                
            else:
                if os.path.isdir(input[k][1]):
                    return current_path + "/" + input[k][1]
                else:
                    os.write(1, "directory change not valid\n".encode())
                

        else:    #passes other commands to proper functions
            
            if (len(input) > 1): 
                    
                pipe_handler(input, len(input))
                
            else:
            
                program_fork(input[k][0], input[k][0:])

        
        k+=1 #iterates through all processes


        
        
    

    return current_path
    
#########################################################################################################
############################ main program:

os.write(1, (current_path.encode()+'$ '.encode()))
while(True):

        instant = os.read(0,1)
        if instant.decode() == '\n':

                if input == 'exit':
                        break

                current_path = command_handler(input, current_path)
                os.chdir(current_path)

                input = ''
                os.write(1, (current_path.encode()+'$ '.encode()))
        else:
            input += instant.decode()
















