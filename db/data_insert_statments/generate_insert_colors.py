import re

input_file = "colors.txt"
output_file = "insert_colorss.txt"

fin = open(input_file, "r")
fout = open(output_file, "w")

data = fin.read()

colors = re.findall("(\w+)",data)
for color in colors:
    fout.write(f"INSERT INTO color (color) VALUES ('{color}');\n")

fout.close()
fin.close()