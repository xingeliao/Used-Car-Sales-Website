import re

input_file = "manufacturers.txt"
output_file = "insert_manufacturers.txt"

fin = open(input_file, "r")
fout = open(output_file, "w")

data = fin.read()

manus = re.findall("(\w+)",data)
for manu in manus:
    fout.write(f"INSERT INTO vehiclemanufacturer (manufacturer_name) VALUES ('{manu}');\n")

fout.close()
fin.close()