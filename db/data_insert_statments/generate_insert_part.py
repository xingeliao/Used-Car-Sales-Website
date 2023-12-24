import re
import pandas as pd 

reg_string = "(?P<vin>\w+)\t(?P<order_num>\d+)\t(?P<vendor_name>[A-z| |\-]+)\t(?P<part_number>[A-z| |\-|0-9]+)\t(?P<description>[A-z| |\\|\/|\-|:|0-9]+)\t(?P<price>\d+\.\d+)\t(?P<status>[A-z| |\-|0-9]+)\t(?P<qty>\d+)"

txt_file = "parts.tsv"
calculated_txt_File = "parts_with_calculated_cost.csv"
out_file = "insert_parts.txt"
fin = open(txt_file, 'r')
fout = open(out_file, "w")

# df = pd.read_csv(txt_file, sep="\t")

# print(df.head())

fin2 = open(calculated_txt_File, "r")
calculated_data = fin2.read().split("\n")

for line in calculated_data:
    part_order_info = line.split(",")

    values = f"VALUES ('{part_order_info[4]}', '{part_order_info[0]}', '{part_order_info[1]}', '{part_order_info[2]}', 'user09', {part_order_info[3]})"
    insert_query = "INSERT INTO partorder (purchase_order_number, vin, order_number, part_vendor_name, username, total_cost) " + values + ";\n"
    fout.write(insert_query)
    # print(part_order_info)



data = fin.readlines()

# print(purchase_df)
for line in data:
    reg_res = re.search(reg_string, line)
    if (reg_res):
        vin = reg_res.group('vin')
        order_num = reg_res.group('order_num')
        part_number = reg_res.group('part_number')
        description = reg_res.group('description')
        status = reg_res.group('status')
        cost = reg_res.group('price')
        quantity = reg_res.group('qty')
        vendor_name = reg_res.group('vendor_name')

        purchase_order_number = vin + "-" + order_num

        values = f"VALUES ('{part_number}', '{purchase_order_number}', '{description}', '{status}', '{cost}', '{quantity}')"
        insert_query = "INSERT INTO part (part_number, purchase_order_number, description, status, cost, quantity) " + values + ";\n"
        fout.write(insert_query)



fin.close()
fin2.close()
fout.close()