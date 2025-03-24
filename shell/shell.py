import os, sys, time, re

input = ''
instant = ''
og_path = os.getcwd()
current_path = og_path


def command_handler(input, current_path):
    input = input.split(' ')

    if input[0] == 'cd' and len(input) > 1:
        if input[1] == '..':
            if os.path.dirname(current_path):
                current_path = os.path.dirname(current_path)
            else:
                os.write(1, "directory change not valid".encode())

        else:
            if os.path.dirname(input[1].encode()):
                current_path = os.path.dirname(input[1].encode())
            else:
                os.write(1, "directory change not valid".encode())


        
        
    

    return current_path
        


os.write(1, (current_path.encode()+'$ '.encode()))
while(True):

        instant = os.read(0,1)
        if instant.decode() == '\n':

                if input == 'exit':
                        break

                current_path = command_handler(input, current_path)
                os.chdir(current_path)
                print(os.listdir())

                input = ''
                os.write(1, (current_path.encode()+'$ '.encode()))
        else:
                input += instant.decode()
