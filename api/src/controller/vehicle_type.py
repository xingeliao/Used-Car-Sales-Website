from flask import g

def get_vehicle_types():
    conn = g.pop('conn')
    base_query = f'''
        select *
        from vehicletype;
    '''
    cursor = conn.cursor()
    cursor.execute(base_query)

    response = {}
    columns = [desc[0] for desc in cursor.description]
    response['metadata'] = columns
    
    data = cursor.fetchall()
    response['data'] = data
    
    return response
