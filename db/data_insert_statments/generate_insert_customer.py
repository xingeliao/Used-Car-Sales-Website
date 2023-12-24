import re

txt_file = "customers.tsv"
out_file = "insert_customer.txt"
fin = open(txt_file, 'r')

data = fin.readlines()
reg_string = "Person\t(?P<email>[A-z|@|\-|.]+){0,1}\t(?P<phone>\d+)\t(?P<street>.+)\t(?P<city>[A-z|\.| |\/|\\|\-]+)\t(?P<state>\w{2})\t(?P<postal>\d+)\t*(?P<driver_lic>\w+)\t(?P<person_first>\w+)\t(?P<person_last>\w+)"

fout = open(out_file, "w")
for line in data:
    reg_res = re.search(reg_string, line)
    if(reg_res):
        street = reg_res.group('street')
        city = reg_res.group('city')
        state = reg_res.group('state')
        postal_code = reg_res.group('postal')
        phone_number = reg_res.group('phone')
        email = reg_res.group('email')
        if (email):
            insert_query = f'''INSERT INTO customer (customer_id, street, city, state, postal_code, phone_number, email) VALUES (gen_random_uuid(), '{street}','{city}', '{state}', '{postal_code}','{phone_number}', '{email}');\n'''
        else:
            insert_query = f'''INSERT INTO customer (customer_id, street, city, state, postal_code, phone_number, email) VALUES (gen_random_uuid(), '{street}','{city}', '{state}', '{postal_code}','{phone_number}', NULL);\n'''

        fout.write(insert_query)
        drivers_license_no = reg_res.group('driver_lic')
        first_name = reg_res.group('person_first')
        last_name = reg_res.group('person_last')
        if (email):
            insert_query = f'''INSERT INTO customerindividual (drivers_license_number, customer_id, first_name, last_name) 
            SELECT 
                '{drivers_license_no}', 
                c.customer_id, 
                '{first_name}', 
                '{last_name}' 
            FROM customer c
            WHERE c.street = '{street}' AND c.city = '{city}' AND c.state = '{state}' AND c.postal_code = '{postal_code}' AND c.phone_number = '{phone_number}' AND email = '{email}';\n'''
        else:
            insert_query = f'''INSERT INTO customerindividual (drivers_license_number, customer_id, first_name, last_name) 
            SELECT 
                '{drivers_license_no}', 
                c.customer_id, 
                '{first_name}', 
                '{last_name}' 
            FROM customer c
            WHERE c.street = '{street}' AND c.city = '{city}' AND c.state = '{state}' AND c.postal_code = '{postal_code}' AND c.phone_number = '{phone_number}';\n'''
        fout.write(insert_query)

reg_string = "Business\t(?P<email>[A-z|@|\-|.]+){0,1}\t(?P<phone>\d+)\t(?P<street>.+)\t(?P<city>[A-z|\.| |\/|\\|\-]+)\t(?P<state>\w{2})\t(?P<postal>\d+)\t(?P<biz_tax_id>\d{2}\-\d+)\t(?P<biz_name>[A-z| |0-9|\-|\\|\/]+)\t(?P<biz_contact_name>[A-z| |0-9|\-|\\|\/]+\t[A-z| |0-9|\-|\\|\/]+)\t(?P<biz_contact_title>[A-z| |0-9|\-|\\|\/]+)"
# reg_res = re.findall(reg_string,line)
for line in data:
    reg_res = re.search(reg_string, line)
    if(reg_res):
        street = reg_res.group('street')
        city = reg_res.group('city')
        state = reg_res.group('state')
        postal_code = reg_res.group('postal')
        phone_number = reg_res.group('phone')
        email = reg_res.group('email')
        if (email):
            insert_query = f'''INSERT INTO customer (customer_id, street, city, state, postal_code, phone_number, email) VALUES (gen_random_uuid(), '{street}','{city}', '{state}', '{postal_code}','{phone_number}', '{email}');\n'''
        else:
            insert_query = f'''INSERT INTO customer (customer_id, street, city, state, postal_code, phone_number, email) VALUES (gen_random_uuid(), '{street}','{city}', '{state}', '{postal_code}','{phone_number}', NULL);\n'''

        fout.write(insert_query)

        tax_id_number = reg_res.group('biz_tax_id')
        biz_name = reg_res.group('biz_name')
        biz_contact = reg_res.group('biz_contact_name')
        biz_contact_title = reg_res.group('biz_contact_title')
        business_name = biz_name.replace("\t", " ")
        if(email):
            insert_query = f'''INSERT INTO customerbusiness (tax_id_number, customer_id, business_name, contact_name, title) 
            SELECT 
                '{tax_id_number}', 
                c.customer_id, 
                '{business_name}',
                '{biz_contact}', 
                '{biz_contact_title}' 
            FROM customer c
            WHERE c.street = '{street}' AND c.city = '{city}' AND c.state = '{state}' AND c.postal_code = '{postal_code}' AND c.phone_number = '{phone_number}' AND email = '{email}';\n'''
        else:
            insert_query = f'''INSERT INTO customerbusiness (tax_id_number, customer_id, business_name, contact_name, title) 
            SELECT 
                '{tax_id_number}', 
                c.customer_id, 
                '{business_name}',
                '{biz_contact}', 
                '{biz_contact_title}' 
            FROM customer c
            WHERE c.street = '{street}' AND c.city = '{city}' AND c.state = '{state}' AND c.postal_code = '{postal_code}' AND c.phone_number = '{phone_number}';\n'''
        fout.write(insert_query)
        # insert_query = f'''INSERT INTO customerbusiness (tax_id_number, customer_id, contact_name, title) VALUES ('{res[6]}','{res[0]}', '{business_name}', '{res[7]}' );\n'''
        fout.write(insert_query)
fin.close()
fout.close()