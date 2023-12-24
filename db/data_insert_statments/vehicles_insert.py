import re

def valOrEmptyString(obj, key):
    return obj.group(key) if obj.group(key) != None else ""

input_file = "vehicles.tsv"
output_file = "insert_vehicles.txt"

regex_string = "(?P<vin>\w+)\t(?P<model_name>[A-z| |0-9|\/|\-|&]+)\t(?P<year>\d+)\t(?P<description>[A-z| |0-9|;|\-|.|\\|\/|\)|\(]+){0,1}\t(?P<manufacturer_name>[A-z| |\-]+)\t(?P<condition>[A-z| ]+)\t(?P<vehicle_type>\w+)\t(?P<mileage>\d+.\d+)\t(?P<fuel_type>[A-z| ]+)\t(?P<colors>[A-z|,| ]+)\t(?P<purchase_date>\d+-\d{2}-\d{2})\t(?P<price>\d+.\d+)\t(?P<purchased_from_customer>[A-z| |\-|0-9]+)\t(?P<purchase_clerk>\w+)\t(?P<sale_date>\d+-\d{2}-\d{2}){0,1}\t(?P<sold_to_customer>[0-9|A-z|\-]+){0,1}\t(?P<salesperson>\w+){0,1}"

fin = open(input_file, "r")
fout = open(output_file, "w")



data = fin.readlines()
for line in data:
    # print(line)
    vehicle_res = re.search(regex_string,line)
    if(vehicle_res != None):
        vin = valOrEmptyString(vehicle_res, 'vin')
        model_name = valOrEmptyString(vehicle_res, 'model_name')
        year = valOrEmptyString(vehicle_res, 'year')
        description = valOrEmptyString(vehicle_res, 'description')
        manufacturer_name = valOrEmptyString(vehicle_res, 'manufacturer_name')
        condition = valOrEmptyString(vehicle_res, 'condition')
        vehicle_type = valOrEmptyString(vehicle_res, 'vehicle_type')
        mileage = valOrEmptyString(vehicle_res, 'mileage')
        fuel_type = valOrEmptyString(vehicle_res, 'fuel_type')
        colors = valOrEmptyString(vehicle_res, 'colors').split(",")
        purchase_date = valOrEmptyString(vehicle_res, 'purchase_date')
        price = valOrEmptyString(vehicle_res, 'price')
        purchased_from_customer = valOrEmptyString(vehicle_res, 'purchased_from_customer')
        purchase_clerk = valOrEmptyString(vehicle_res, 'purchase_clerk')
        sale_date = valOrEmptyString(vehicle_res, 'sale_date')
        sold_to_customer = valOrEmptyString(vehicle_res, 'sold_to_customer')
        salesperson = valOrEmptyString(vehicle_res, 'salesperson')
        description = vehicle_res.group('description') if vehicle_res.group('description') != None else None

        if(purchase_clerk == None):
            print("none")
        if(description == None):
            fout.write(f"INSERT INTO public.vehicle(vin, vehicle_type, manufacturer_name, fuel_type, model_name, model_year, description, mileage) VALUES ('{vin}','{vehicle_type}', '{manufacturer_name}', '{fuel_type}','{model_name}','{year}', NULL, '{mileage}');\n")
        else: 
            fout.write(f"INSERT INTO public.vehicle(vin, vehicle_type, manufacturer_name, fuel_type, model_name, model_year, description, mileage) VALUES ('{vin}','{vehicle_type}', '{manufacturer_name}', '{fuel_type}','{model_name}','{year}','{description}','{mileage}');\n")
        # for color in colors:
        #     fout.write(f"INSERT INTO public.vehiclecolor (color, vin) VALUES ('{color}','{vin}');\n")

        if "-" in purchased_from_customer:
            insert_query = f''' INSERT INTO public.sell(customer_id, vin, username, purchase_price, purchase_date, vehicle_condition)
            SELECT
                c.customer_id,
                '{vin}',
                '{purchase_clerk}',
                '{price}',
                '{purchase_date}',
                '{condition}'
            FROM customerbusiness c
            WHERE c.tax_id_number = '{purchased_from_customer}';\n            
            '''
        else:
            insert_query = f''' INSERT INTO public.sell(customer_id, vin, username, purchase_price, purchase_date, vehicle_condition)
            SELECT
                c.customer_id,
                '{vin}',
                '{purchase_clerk}',
                '{price}',
                '{purchase_date}',
                '{condition}'
            FROM customerindividual c
            WHERE c.drivers_license_number = '{purchased_from_customer}';\n           
            '''

        # fout.write(insert_query)
        if(salesperson and sold_to_customer and sale_date):
            if("-" in sold_to_customer):
                insert_query = f''' INSERT INTO public.buy(customer_id, vin, username, sale_date, sale_price)
                SELECT
                    c.customer_id,
                    '{vin}',
                    '{salesperson}',
                    '{sale_date}',
                    '0.0'
                FROM customerbusiness c
                WHERE c.tax_id_number = '{sold_to_customer}';\n            
                '''
            else:                
                insert_query = f''' INSERT INTO public.buy(customer_id, vin, username, sale_date, sale_price)
                SELECT
                    c.customer_id,
                    '{vin}',
                    '{salesperson}',
                    '{sale_date}',
                    '0.0'
                FROM customerindividual c
                WHERE c.drivers_license_number = '{sold_to_customer}';\n            
                '''
        # fout.write(insert_query)
                
        # values = f"VALUES ('{customer}', '{vin}', '{purchase_clerk}','{purchase_date}','{price}')"
        # fout.write("INSERT INTO public.sell (customer_id, vin, username, purchase_price, purchase_date, vehicle_condition) " + values + ";\n")

        # if(sale_date != None and sold_to_customer != None and salesperson != None):
        #     fout.write("INSERT INTO public.buy (customer_id, vin, username, purchase_price, purchase_date, vehicle_condition )")