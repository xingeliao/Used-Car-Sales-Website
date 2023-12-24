from flask import g

def search_customer(*args, **kwargs):
    conn = g.pop('conn')

    phonenumber = kwargs.pop('phonenumber', None)
    name = kwargs.pop('name', None)
    id_number = kwargs.pop('id', None)
    print(id_number)

    phonenumber = f'%{phonenumber}%' if phonenumber else ''
    name = f'%{name}%' if name else ''
    id_number = f'%{id_number}%' if id_number else ''

    base_query = f'''
        SELECT c.*, cicb.id, cicb.contact_name, cicb.title from customer c JOIN
        (
            SELECT drivers_license_number id, CONCAT(first_name, ' ', last_name) contact_name, ' ' title, customer_id 
            FROM customerindividual
            UNION
            SELECT tax_id_number id, contact_name, title, customer_id
            FROM customerbusiness
        ) AS cicb ON cicb.customer_id = c.customer_id
        WHERE cicb.id ilike '{id_number}';
    '''
    
    print(base_query)

    cursor = conn.cursor()
    cursor.execute(base_query)
    
    response = {}
    columns = [desc[0] for desc in cursor.description]
    response['metadata'] = columns
    
    data = cursor.fetchall()
    response['data'] = data

    return response