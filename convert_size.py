import sys # used to handle input and output

inStr = sys.argv[1] # store command line argument in the variable inStr

# seperate the number and the unit into 2 variables
num = "".join(d for d in inStr if d.isdigit())
unit = "".join(a for a in inStr if a.isalpha())
unit = unit.lower() # convert all letters to lowercase

# if unit is already bytes, just output the number
if unit == "b":
    sys.stdout.write(num)

# store the unit abbreviations in the proper order
base10units = ["kb", "mb", "gb", "tb", "pb", "eb", "zb", "yb"]
base2units = ["kib", "mib", "gib", "tib", "pib", "eib", "zib", "yib"]

# I noticed in the Part 4 input files that not all the unit abbreviations ended with a "b"
# Hence, I've included this extra check to add a "b" if there is none
if not unit.endswith("b"):
    unit = unit + "b"

# if using base 10 units, output the number times 1000 to the power of the corresponding exponent
if unit in base10units:
    sys.stdout.write(str(int(num) * (1000 ** (base10units.index(unit) + 1))))

# if using base 2 units, output the number times 1024 to the power of the corresponding exponent
if unit in base2units:
    sys.stdout.write(str(int(num) * (1024 ** (base2units.index(unit) + 1))))
