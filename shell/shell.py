import os, sys, time, re

input = ''
instant = ''
og_path = os.getcwd()
current_path = og_path




def program_fork(command):
    args = []
    pid = os.fork()

    if pid == 0:
        args.append(command)
        os.execvpe(command, args, os.environ)

    else:
        os.wait()


#######################################################################################################

def pipe_handler(value, input):   ##needs to recieve an input value and pipe it to next program
    os.write(1, "pipe_handler activated!!".encode())
    return
    



#######################################################################################################
############################ handles input

def command_handler(input, current_path):
    input = input.split(' ')
    returnVal = None;
    i = 0

    if input[0] == 'cd' and len(input) > 1:
        if input[1] == '..':
            if os.path.dirname(current_path):
                current_path = os.path.dirname(current_path)
                return current_path
            else:
                os.write(1, "directory change not valid".encode())

        else:
            if os.path.isdir(input[1]):
                return current_path + "/" + input[1]
            else:
                os.write(1, "directory change not valid".encode())


    else:

        while (i < len(input)):

            if input[i] == '|':

                pipe_handler(returnVal)

            elif (os.system(f'command -v {input[i]} > /dev/null 2>&1') == 0): ##if command exists

                returnVal = program_fork(input[i])

            else:
                os.write(1, "invalid command".encode())
                
            i+=1
        


        
        
    

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
