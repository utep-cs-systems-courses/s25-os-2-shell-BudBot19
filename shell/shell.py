import os, sys, time, re

cmd_input = ''
instant = ''
og_path = os.getcwd()
current_path = og_path




def program_fork(command, args):

    pid = os.fork()


    if pid == 0:

        try:
            command = os.path.abspath("/bin/"+command)
            os.execve(command, args, os.environ)
        except:
            os.write(1, f"{command}: invalid command!\n".encode())

        sys.exit()
            
    else:
        os.wait()


#######################################################################################################

def pipe_handler(cmd_input):   ##needs to recieve an input value and pipe it to next program

    if len(cmd_input) > 2:
        os.write(1, "sorry, this shell program only handles simple pipes!\n".encode())
        return


    iFd, oFd = os.pipe()

    read_pid = os.fork()
    if read_pid == 0:
        os.close(oFd)
        os.dup2(iFd, 0) ##duplicates stdin
        os.close(iFd)

        try:
            command = os.path.abspath("/bin/"+cmd_input[1][0])
            os.execve(command, cmd_input[1][0:], os.environ)
        except:
            os.write(1, 'invalid command!\n'.encode())
            
        sys.exit()

    write_pid = os.fork()
    if write_pid == 0: 
        os.close(iFd)
        os.dup2(oFd, 1) ##duplicates stdout
        os.close(oFd)
         
        try:
            command = os.path.abspath("/bin/"+cmd_input[0][0])
            os.execve(command, cmd_input[0][0:], os.environ)
        except:
            os.write(1, 'invalid command!\n'.encode())

        sys.exit()


            
    os.close(iFd)
    os.close(oFd)
    os.waitpid(read_pid, 0)
    os.waitpid(write_pid, 0)
    return


#######################################################################################################
############################ checks for redirect

def try_redirect(cmd_input):
    hasRedirect = False
    i = 0
    while i < len(cmd_input[0]):
        if  cmd_input[0][i] == '>':
            os.write(1, "redirect found\n".encode())
            hasRedirect = True
            break
        i+=1

    if hasRedirect:
        iFd, oFd = os.pipe()

        write_pid = os.fork()
        if write_pid == 0:

            os.close(iFd)
            os.dup2(oFd, 1)
            os.close(oFd)

            try:
                command = os.path.abspath("/bin/"+cmd_input[0][0])
                os.execve(command, cmd_input[0][0:i], os.environ)
            except:
                os.write(1, f"{command}: invalid command!\n".encode())

            sys.exit(1)

        read_pid = os.fork()
        if read_pid == 0:
            os.close(oFd)

            try:
                writeFd = os.open(cmd_input[0][i+1], os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
            except:
                os.write(1, "could not redirect to file or stream\n".encode())
                writeFd = 1

            while True:
                bytes = os.read(iFd, 1024)
                if not bytes:
                    break
                os.write(writeFd, bytes)

            if writeFd != 1:   ###keeps program from closing stdout
                os.close(writeFd)

            os.close(iFd)
            sys.exit(0)

        os.close(iFd)
        os.close(oFd)
        os.waitpid(write_pid, 0)
        os.waitpid(read_pid, 0)
            


    return hasRedirect



#######################################################################################################
########################### checks for background

def try_background(cmd_input):
    last = len(cmd_input[0])-1
    if(cmd_input[0][last] == '&'):
        os.write(1, "this is a background task!\n".encode())

        pid = os.fork()

        if pid == 0:

            try:
                command = os.path.abspath("/bin/"+cmd_input[0][0])
                os.execve(command, cmd_input[0][0:last], os.environ)
            except:
                os.write(1, f"{command}: invalid command!\n".encode())

    return False


#######################################################################################################
############################ handles input

def command_handler(cmd_input, current_path):
    cmd_input = cmd_input.split('|')  ##seperates for potential piping

    for index in range(len(cmd_input)):
        cmd_input[index] = cmd_input[index].split(" ")
        if len(cmd_input) > 1:
            cmd_input[index].remove('')


    if cmd_input[0][0] == 'cd' and len(cmd_input[0]) > 1:       #handles directory changes
        if cmd_input[0][1] == '..':
            if os.path.dirname(current_path):
                current_path = os.path.dirname(current_path)
                return current_path
            else:
                os.write(1, "directory change not valid\n".encode())
                
        else:
            if os.path.isdir(cmd_input[0][1]):
                return current_path + "/" + cmd_input[0][1]
            else:
                os.write(1, "directory change not valid\n".encode())
                

    else:    #passes other commands to proper functions
            
        if (len(cmd_input) > 1): 
                    
            pipe_handler(cmd_input)

                
        elif try_redirect(cmd_input):
            return current_path

        elif try_background(cmd_input):
            return current_path

        else:
            program_fork(cmd_input[0][0], cmd_input[0][0:])
        


        
        
    

    return current_path
    
#########################################################################################################
############################ main program:

os.write(1, (current_path.encode()+'$ '.encode()))
cmd_input = ''
while(True):

        instant = os.read(0,1)
        if instant.decode() == '\n':

            if cmd_input == 'exit':
                break

            current_path = command_handler(cmd_input, current_path)
            os.chdir(current_path)

            cmd_input = ''
            os.write(1, (current_path.encode()+'$ '.encode()))
            
        else:
            cmd_input += instant.decode()
















