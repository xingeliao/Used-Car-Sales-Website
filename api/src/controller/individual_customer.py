from flask import g

def get_individual_customer(drivers_license_number):
    conn = g.pop('conn')
    base_query = f'''
        SELECT drivers_license_number, customer_id, first_name, last_name
        FROM customerindividual
        WHERE drivers_license_number ilike '%{drivers_license_number}%';
    '''
    cursor = conn.cursor()
    cursor.execute(base_query)

    response = {}
    customers = []
    for customer in cursor:
        customers.append(customer)

    columns = [desc[0] for desc in cursor.description]
    response['metadata'] = columns
    response['data'] = customers
    return response


def add_individual_customer(customer_json):
    conn = g.pop('conn')  # retrieves psycopg2 connection object from flask g
    street = valOrEmptyString(customer_json, 'street')
    city = valOrEmptyString(customer_json, 'city')
    state = valOrEmptyString(customer_json, 'state')
    postal_code = valOrEmptyString(customer_json, 'postal_code')
    phone_number = valOrEmptyString(customer_json, 'phone_number')
    drivers_license_number = valOrEmptyString(customer_json, 'drivers_license_number')
    first_name = valOrEmptyString(customer_json, 'first_name')
    last_name = valOrEmptyString(customer_json, 'last_name')
    email = valOrEmptyString(customer_json, 'email')

    if (email):
        base_query = f'''
            INSERT INTO customer (customer_id, street, city, state, postal_code, phone_number, email)
            VALUES (gen_random_uuid(), '{street}', '{city}', '{state}', '{postal_code}', '{phone_number}', '{email}') RETURNING customer_id;
        '''
    else:
        base_query = f'''
            INSERT INTO customer (customer_id, street, city, state, postal_code, phone_number, email)
            VALUES (gen_random_uuid(), '{street}', '{city}', '{state}', '{postal_code}', '{phone_number}', NULL) RETURNING customer_id;
        '''

    cursor = conn.cursor()
    cursor.execute(base_query)
    customer_id = cursor.fetchone()['customer_id']
    secondary_query = f'''INSERT INTO customerindividual (drivers_license_number, customer_id, first_name, last_name) 
        VALUES ('{drivers_license_number}', '{customer_id}', '{first_name}', '{last_name}')
    '''
        # # SELECT 
    # #     '{drivers_license_number}', 
    # #     c.customer_id, 
    # #     '{first_name}', 
    # #     '{last_name}' 
    # #     FROM customer c
    # #     WHERE c.street = '{street}' AND c.city = '{city}' AND c.state = '{state}' AND c.postal_code = '{postal_code}' AND c.phone_number = '{phone_number}';
    # # '''

    cursor.execute(secondary_query)
    conn.commit()
    print(customer_id, flush=True)

    # cursor.execute(secondary_query)
    # conn.commit()
    return {"customerid": customer_id,
            "driversLicenseNumber": drivers_license_number}


def valOrEmptyString(obj, key):
    return obj.pop(key) if key in obj.keys() else ""
