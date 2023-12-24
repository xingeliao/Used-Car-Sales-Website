from flask import g


def get_vendor(*args, **kwargs):
    conn = g.pop('conn')

    phonenumber = kwargs.pop('phonenumber', None)
    name = kwargs.pop('name', None)

    base_query = f'''
        SELECT name FROM PartVendor
    '''
    if phonenumber and name:
        base_query += f" WHERE phonenumber ilike '%{phonenumber}%' OR name = '%{name}%';"
    elif phonenumber:
        base_query += f" WHERE phonenumber ilike '%{phonenumber}%';'"
    elif name:
        base_query += f" WHERE name ilike '%{name}%';"
    else:
        base_query += f";"

    cursor = conn.cursor()
    cursor.execute(base_query)
    
    response = {}
    columns = [desc[0] for desc in cursor.description]
    response['metadata'] = columns
    
    data = cursor.fetchall()
    response['data'] = data

    return response


def add_vendor(body_json):
    conn = g.pop('conn')

    name = body_json.pop('name')
    phonenumber = body_json.pop('phonenumber')
    street = body_json.pop('street')
    city = body_json.pop('city')
    state = body_json.pop('state')
    postal_code = body_json.pop('postal_code')

    base_query = f'''
        INSERT INTO PartVendor (name, phone_number, street, city, state, postal_code) VALUES ('{name}', 
        '{phonenumber}', '{street}', '{city}', '{state}', '{postal_code}')
        RETURNING name;
    '''
    
    print(base_query)
    cursor = conn.cursor()
    cursor.execute(base_query)
    
    res = cursor.fetchone()
    conn.commit()

    return res
