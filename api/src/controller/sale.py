from flask import g


def add_sale(sale_json):
    conn = g.pop('conn')  # retrieves psycopg2 connection object from flask g
    customer_id = sale_json.pop('customer_id')
    vin = sale_json.pop('vin')
    username = sale_json.pop('username')
    saledate = sale_json.pop('sale_date')
    base_query = f'''
        INSERT INTO buy (customer_id, vin, username, sale_date) VALUES ('{customer_id}', '{vin}', '{username}', '{saledate}');
    '''
    
    print(base_query)
    cursor = conn.cursor()
    cursor.execute(base_query)
    
    res = cursor.description
    print(res)
    conn.commit()

    return True


