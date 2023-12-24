import re

regex_string = "(?P<vendor_name>.+)\t(?P<phone>\d+)\t(?P<street>.+)\t(?P<city>.+)\t(?P<state>\w+)\t(?P<postal_code>\d+)"

input_file = "vendors.tsv"
output_file = "insert_vendors.txt"

fin = open(input_file, "r")
fout = open(output_file, "w")

lines = fin.readlines()
for line in lines:
    reg_res = re.search(regex_string,line)
    if(reg_res != None):
        vendor_name = reg_res.group('vendor_name')
        phone = reg_res.group('phone')
        street = reg_res.group('street')
        city = reg_res.group('city')
        state = reg_res.group('state')
        postal_code = reg_res.group('postal_code')

        values_string = f"VALUES ('{vendor_name}', '{phone}', '{street}', '{city}', '{state}', '{postal_code}')"
        query_string = "INSERT INTO partvendor (name, phone_number, street, city, state, postal_code) " + values_string + ";\n"
        fout.write(query_string)

fin.close()
fout.close()
