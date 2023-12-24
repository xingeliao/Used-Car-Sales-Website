import re

input_file = "users.tsv"
output_file = "insert_users.txt"

fin = open(input_file, "r")
fout = open(output_file, "w")

lines = fin.readlines()


regex_string = "(?P<username>\w+)\t(?P<password>\w+)\t(?P<first_name>\w+)\t(?P<last_name>\w+)\t(?P<roles>.+)\n"
for line in lines:
    re_match = re.search(regex_string,line)
    if(re_match):
        username = re_match.group('username')
        password = re_match.group('password')
        first_name = re_match.group('first_name')
        last_name = re_match.group('last_name')

        values = f"VALUES ('{username}','{password}','{first_name}','{last_name}')"
        # insert_query = "INSERT INTO adminuser (username,password,first_name,last_name) " + values + "\n"
        # fout.write(insert_query)
        roles = re_match.group('roles').strip().split(',')
        if('inventory clerk' in roles and 'salesperson' in roles and 'manager' in roles):
            insert_query = "INSERT INTO owner (username,password,first_name,last_name) " + values + ";\n"
            fout.write(insert_query)
        elif('inventory clerk' in roles):
            insert_query = "INSERT INTO inventoryclerk (username,password,first_name,last_name) " + values + ";\n"
            fout.write(insert_query)
        elif('salesperson' in roles):
            insert_query = "INSERT INTO salespeople (username,password,first_name,last_name) " + values + ";\n"
            fout.write(insert_query)
        elif('manager' in roles):
            insert_query = "INSERT INTO manager (username,password,first_name,last_name) " + values + ";\n"
            fout.write(insert_query)

fin.close()
fout.close()