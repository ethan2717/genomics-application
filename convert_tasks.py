# This implementation makes certain assumptions about the input file
# For example, that it uses double quotation marks ("), instead of single ones (')

import sys # used to handle command line arguments

# store the unit abbreviations (without "b") in the proper order
base10units = ["k", "m", "g", "t", "p", "e", "z", "y"]
base2units = ["ki", "mi", "gi", "ti", "pi", "ei", "zi", "yi"]

for argNum in range(1, len(sys.argv)): # loop through every command line argument (except the first)
    try: # handles invalid file names
        inFile = open(sys.argv[argNum]) # open file in read mode
        outFile = open(sys.argv[argNum].replace("input", "output"), "w") # open file in write mode (clears existing text)
        outFile = open(sys.argv[argNum].replace("input", "output"), "a") # open file in append mode
        for line in inFile: # loop through every line of inFile
            if "mem" in line or "disk" in line: # if line contains "mem" or "disk"
                num = "".join(d for d in line if d.isdigit()) # store the numbers
                unit = "".join(a for a in line if a.isalpha()).lower() # store the letters
                # remove the irrelevant letters
                unit = unit.replace("mem", "")
                unit = unit.replace("disk", "")
                unit = unit.replace("b", "")
                bytes = 0
                # convert to bytes using the same method as in convert_size.py
                if unit.endswith("i"):
                    bytes = int(num) * (1024 ** (base2units.index(unit) + 1))
                else:
                    bytes = int(num) * (1000 ** (base10units.index(unit) + 1))
                # write the result to the output file
                if "mem" in line:
                    outFile.write("        \"mem\": \""+str(bytes)+"\",\n")
                else:
                    outFile.write("        \"disk\": \""+str(bytes)+"\",\n")
            else: # if the line does not need any conversion
                outFile.write(line) # copy the line over to outFile
        # close the files
        inFile.close()
        outFile.close()
    except: # does something inconsequential when the file name is invalid
        foo = "bar" # dummy line
