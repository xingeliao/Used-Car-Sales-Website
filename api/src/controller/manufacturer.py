from flask import g

def get_manufacturers():
    conn = g.pop('conn')
    query = f'''
        select *
        from vehiclemanufacturer;
    '''
    cursor = conn.cursor()
    cursor.execute(query)

    response = {}
    columns = [desc[0] for desc in cursor.description]
    response['metadata'] = columns
    
    data = cursor.fetchall()
    response['data'] = data
    return response
