#!/usr/bin/env python3

from sys import argv, stdin, stdout

try:
    cells = bytearray(30000) # Memory (30kb)
    dp = 0 # Data pointer
    
    try:
        with open(argv[1], "r") as f:
            code = f.read()
    except IndexError:
        print("Enter code here:")
        code = stdin.read()
        print("")

    def segfaulthandler(dp, f, cellamount):
        if dp < 0 or dp > 29999:
            print("Brainf**k segmentation fault (core dumped)")
        
            f.write(f"Program: {code}\n")
            
            f.write("------- Memory -------\n")
            for i in range(0, cellamount):
                f.write(f"{cells[i]} ")

            f.write("\n--- End of memory ---\n")
            f.write(f"Data pointer: {dp}\n")
        
            return 1
        return 0

    stack = [] # Bracket nest stack
    jump = [None]*len(code)
    ip = 0 # Instruction pointer

    # totally not taken from https://stackoverflow.com/a/3041005
    for i,o in enumerate(code):
        if o=='[':
            stack.append(i)
        elif o==']':
            jump[i] = stack.pop()
            jump[jump[i]] = i

    while ip < len(code):
        match code[ip]:
            case "+":
                cells[dp] = (cells[dp] + 1) % 255
            case "-":
                cells[dp] = (cells[dp] - 1) % 255
            case ">":
                dp+=1
                if dp < -1 or dp > 29999:
                    with open("core", "w") as f:
                        if segfaulthandler(dp, f, 0):
                            exit(1)
            case "<":
                dp-=1
                if dp < -1 or dp > 29999:
                    with open("core", "w") as f:
                        if segfaulthandler(dp, f, 0):
                            exit(1)
            case ".":
                print(chr(cells[dp]), end="")
            case ",":
                theinput = input("\nInput: ")
                if theinput != "":
                    cells[dp] = ord(theinput[0])
                else:
                    cells[dp] = 0
            case "[":
                if not cells[dp]:
                    ip = jump[ip]
            case "]":
                if cells[dp]:
                    ip = jump[ip]
                    continue
    
            case "#":
                segfaulthandler(-1, stdout, 9)

        ip+=1
except KeyboardInterrupt:
    print("Interrupted")
    exit(1)

print("")
