from flask import g

def get_part_order(order_number):
    conn = g.pop('conn')  

    base_query = f'''
        SELECT po.purchase_order_number, po.part_vendor_name, pv.street, pv.city, pv.state, pv.postal_code, pv.phone_number, p.part_number, p.description, p.cost, p.quantity, p.status
        FROM partorder po 
        JOIN partvendor pv ON po.part_vendor_name = pv.name 
        LEFT JOIN part p ON p.purchase_order_number = po.purchase_order_number
        WHERE po.purchase_order_number = %s;
    '''

    cursor = conn.cursor()
    cursor.execute(base_query,(order_number,))
    all_parts_of_order = cursor.fetchall()
    metadata = [desc[0] for desc in cursor.description]

    return {'data': all_parts_of_order, 'metadata': metadata}