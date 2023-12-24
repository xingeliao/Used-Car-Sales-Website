import re

input_file = "types.txt"
output_file = "insert_types.txt"

fin = open(input_file, "r")
fout = open(output_file, "w")

data = fin.read()

types = re.findall("(\w+)",data)
for type in types:
    fout.write(f"INSERT INTO vehicletype (vehicle_type) VALUES ('{type}');\n")

fout.close()
fin.close()