from flask import g

def get_business_customer(tax_id_number):
    conn = g.pop('conn')
    base_query = f'''
        select *
        from customerbusiness
        where tax_id_number ilike '%{tax_id_number}%'
    '''
    cursor = conn.cursor()
    cursor.execute(base_query)

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


def add_business_customer(customer_json):
    conn = g.pop('conn')  # retrieves psycopg2 connection object from flask g
    street = valOrEmptyString(customer_json, 'street')
    city = valOrEmptyString(customer_json, 'city')
    state = valOrEmptyString(customer_json, 'state')
    postal_code = valOrEmptyString(customer_json, 'postal_code')
    phone_number = valOrEmptyString(customer_json, 'phone_number')
    business_name = valOrEmptyString(customer_json, 'business_name')
    tax_id_number = valOrEmptyString(customer_json, 'tax_id_number')
    contact_name = valOrEmptyString(customer_json, 'contact_name')
    title = valOrEmptyString(customer_json, 'title')
    email = valOrEmptyString(customer_json, 'email')

    if(email):
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

    secondary_query = f'''
        INSERT INTO customerbusiness (tax_id_number, customer_id, business_name, contact_name, title) 
        VALUES ('{tax_id_number}', '{customer_id}', '{business_name}', '{contact_name}', '{title}')
        ;\n
    '''

    cursor.execute(secondary_query)

    response = { "customerid": customer_id,
                "taxId": tax_id_number}
    # columns = [desc[0] for desc in cursor.description]
    # response['metadata'] = columns
    
    # data = cursor.fetchall()
    # response['data'] = data
    conn.commit()
    return response


def valOrEmptyString(obj, key):
    return obj.pop(key) if key in obj.keys() else ""
