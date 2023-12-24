import logging
from flask import g, request

logger = logging.getLogger(__name__)


def valOrEmptyString(obj, key):
    return obj.pop(key) if key in obj.keys() else ""


def add_vehicle(vehicle_json):
    print('hello?')
    print(vehicle_json)
    vin = valOrEmptyString(vehicle_json, 'vin')
    vehicle_type = valOrEmptyString(vehicle_json, 'vehicle_type')
    manufacturer_name = valOrEmptyString(vehicle_json, 'manufacturer_name')
    fuel_type = valOrEmptyString(vehicle_json, 'fuel_type')
    model_name = valOrEmptyString(vehicle_json, 'model_name')
    model_year = valOrEmptyString(vehicle_json, 'model_year')
    description = valOrEmptyString(vehicle_json, 'description')
    mileage = valOrEmptyString(vehicle_json, 'mileage')
    customer_id = valOrEmptyString(vehicle_json, 'customer_id')
    username = valOrEmptyString(vehicle_json, 'username')
    purchase_price = valOrEmptyString(vehicle_json, 'purchase_price')
    purchase_date = valOrEmptyString(vehicle_json, 'purchase_date')
    vehicle_condition = valOrEmptyString(vehicle_json, 'vehicle_condition')    
    
    conn = g.conn
    cursor = conn.cursor()

    vehicle_query = f"""
        insert into vehicle (vin, vehicle_type, manufacturer_name, fuel_type, model_name, model_year, description, mileage) 
        values ('{vin}', '{vehicle_type}', '{manufacturer_name}', '{fuel_type}', '{model_name}', '{model_year}', '{description}', '{mileage}') returning vin;
    """
    cursor.execute(vehicle_query)
    vin = cursor.fetchone()['vin']
    
    sell_query = f"""
        insert into sell (customer_id, vin, username, purchase_price, purchase_date, vehicle_condition)
        values ('{customer_id}', '{vin}', '{username}', '{purchase_price}', '{purchase_date}', '{vehicle_condition}');
    """
    cursor.execute(sell_query)
    
    colors = valOrEmptyString(vehicle_json, 'colors')
    for color in colors:
        vc_query = f"""
            insert into vehiclecolor (color, vin)
            values ('{color}', '{vin}') returning vin;
        """
        cursor.execute(vc_query)
    conn.commit()
    return {'vin': vin}
    

def get_vehicle():
    conn = g.get("conn")  # retrieves psycopg2 connection object from flask g
    query = f"""
        with vins_available_for_purchase as (
            select
                v.vin
            from public.vehicle v
            except
            select
                b.vin
            from public.buy b  -- 202
            except 
            select
                po.vin
            from public.partorder po 
            join public.part p on po.purchase_order_number = p.purchase_order_number
            where p.status != 'installed'
        ),
        vins_pending_parts as (
            select distinct
                po.vin
            from public.partorder po 
            join public.part p on po.purchase_order_number = p.purchase_order_number
            where p.status in ('received', 'ordered')  -- 86
        ),
        vehicles_with_status_and_color as (
            select
                v.*,
                'available' as vin_status,
                array_agg(vc.color) as colors
            from public.vehicle v
            inner join vins_available_for_purchase avail on avail.vin = v.vin
            join vehiclecolor vc on vc.vin = v.vin
            group by v.vin
            union
            select
                v.*,
                'pending' as vin_status,
                array_agg(vc.color) as colors
            from public.vehicle v
            inner join vins_pending_parts pending on pending.vin = v.vin
            join vehiclecolor vc on vc.vin = v.vin
            group by v.vin
        )
        select *
        from vehicles_with_status_and_color v
    """
    clauses = []
    manufacturer_name = request.args.get("manufacturer-name", None) or request.args.get(
        "manufacturer", None
    )
    if manufacturer_name:
        clause = f"""v.manufacturer_name = '{manufacturer_name}'"""
        clauses.append(clause)
    vehicle_type = request.args.get("vehicle-type", None) or request.args.get(
        "type", None
    )
    if vehicle_type:
        clause = f"""v.vehicle_type = '{vehicle_type}'"""
        clauses.append(clause)
    fuel_type = request.args.get("fuel-type", None) or request.args.get("fuel", None)
    if fuel_type:
        clause = f"""v.fuel_type = '{fuel_type}'"""
        clauses.append(clause)
    model_name = request.args.get("model-name", None) or request.args.get("model", None)
    if model_name:
        clause = f"""v.model_name ilike '{model_name}'"""
        clauses.append(clause)
    model_year = request.args.get("model-year", None) or request.args.get("year", None)
    if model_year:
        clause = f"""v.model_year = '{model_year}'"""
        clauses.append(clause)
    kw = request.args.get("kw", None)
    if kw:
        clause = f"""v.description ilike '%{kw}%'"""
        clauses.append(clause)
    mileage = request.args.get("mileage", None)
    if mileage:
        clause = f"""v.mileage <= '{mileage}'"""
        clauses.append(clause)
    colors = request.args.get("colors", None)
    if colors:
        color_list = colors.split(',')
        color_list_str = str(color_list)
        clause = f"""v.colors::text[] @> array{color_list_str}"""
        clauses.append(clause)
    price = request.args.get("price", None)
    if price:
        clause = f"""(s.purchase_price * 1.25 + po.total_cost * 1.1) <= {price}"""
        clauses.append(clause)
    vin = request.args.get("vin", None)
    if vin:
        clause = f"""v.vin ilike '{vin}'"""
        clauses.append(clause)
    if len(clauses) > 0:
        query += " where "
        query += f"""{' and '.join(clauses)}"""

    print(query)
    cursor = conn.cursor()
    cursor.execute(query)

    response = {}
    columns = [desc[0] for desc in cursor.description]
    response["metadata"] = columns

    data = cursor.fetchall()
    response["data"] = data

    return response

def get_vehicle_color():
    query = f"""
        select *
        from public.color;
    """
    conn = g.pop('conn', None)
    cursor = conn.cursor()
    cursor.execute(query)
    
    response = {}
    columns = [desc[0] for desc in cursor.description]
    response['metadata'] = columns

    data = cursor.fetchall()
    response['data'] = data

    return response

def get_vehicle_by_vin_manager(vin):
    conn = g.get("conn")
    #basic info
    select = "v.vin, v.vehicle_type, v.manufacturer_name, v.model_name, v.model_year, v.fuel_type, vc.color, v.mileage, v.description, c.phone_number, s.purchase_price, s.purchase_date"
    tables = """ LEFT JOIN VehicleColor vc ON v.vin = vc.vin
                         LEFT JOIN Sell s ON v.vin = s.vin 
                         LEFT JOIN Customer c ON s.customer_id = c.customer_id """
    base_query = '''SELECT '''+ select +  ''' FROM Vehicle v ''' +  tables + ''' WHERE v.vin = %s;'''
    cursor = conn.cursor()
    cursor.execute(base_query, (vin,))
    data_veh = cursor.fetchone()
    metadata = [desc[0] for desc in cursor.description]
    vehicles_details = data_veh    
    #seller info
    vehicles_details["seller_info"] = {}
    query = '''SELECT CONCAT_WS(' ',ci.first_name, ci.last_name) AS contact_info, c.street, c.city, c.state, c.postal_code, c.phone_number, b.username, c.email
                FROM Vehicle v
                LEFT JOIN Sell b ON v.vin = b.vin
                LEFT JOIN Customer c ON b.customer_id = c.customer_id
                JOIN CustomerIndividual ci ON ci.customer_id = c.customer_id
                WHERE v.vin = %s
                UNION
                SELECT CONCAT_WS(' ',cb.contact_name, cb.title) AS contact_info, c.street, c.city, c.state, c.postal_code, c.phone_number, b.username, c.email
                FROM Vehicle v
                LEFT JOIN Sell b ON v.vin = b.vin
                LEFT JOIN Customer c ON b.customer_id = c.customer_id
                JOIN CustomerBusiness cb ON cb.customer_id = c.customer_id
                WHERE v.vin = %s ;  '''
    cursor = conn.cursor()
    cursor.execute(query, (vin,vin))
    data_veh_seller = cursor.fetchone()
    metadata.append('seller_info')
    vehicles_seller_info = data_veh_seller
    vehicles_details["seller_info"] = vehicles_seller_info
    #inventory clerk that purchased the car
    vehicles_details["clerk_name"] = {}
    query = '''SELECT CONCAT_WS(' ',ic.first_name, ic.last_name) as clerk_name
                FROM Vehicle v
                LEFT JOIN PartOrder po ON v.vin = po.vin
                LEFT JOIN InventoryClerk ic ON po.username = ic.username
                WHERE v.vin = %s'''
    cursor = conn.cursor()
    cursor.execute(query, (vin,))
    data_clerk = cursor.fetchone()
    metadata.append('clerk_name')
    vehicles_details["clerk_name"] = data_clerk['clerk_name']
    #part order info
    vehicles_details["parts_order"] = []
    query = '''SELECT p.purchase_order_number, p.part_vendor_name, p.total_cost
            FROM PartOrder p
            WHERE p.vin = %s
            ORDER BY p.purchase_order_number; '''
    cursor = conn.cursor()
    cursor.execute(query, (vin,))
    all_orders = cursor.fetchall()
    metadata.append('parts_order')
    for order in all_orders:
        vehicles_details["parts_order"].append(order)
    #buyer info
    vehicles_details["buyer_info"] = {}
    query = '''SELECT CONCAT_WS(' ',ci.first_name, ci.last_name) AS contact_info, c.street, c.city, c.state, c.postal_code, c.phone_number, b.username, c.email
                FROM Vehicle v
                LEFT JOIN Buy b ON v.vin = b.vin
                LEFT JOIN Customer c ON b.customer_id = c.customer_id
                JOIN CustomerIndividual ci ON ci.customer_id = c.customer_id
                WHERE v.vin = %s
                UNION
                SELECT CONCAT_WS(' ',cb.contact_name, cb.title) AS contact_info, c.street, c.city, c.state, c.postal_code, c.phone_number, b.username, c.email
                FROM Vehicle v
                LEFT JOIN Buy b ON v.vin = b.vin
                LEFT JOIN Customer c ON b.customer_id = c.customer_id
                JOIN CustomerBusiness cb ON cb.customer_id = c.customer_id
                WHERE v.vin = %s ;  '''
    cursor = conn.cursor()
    cursor.execute(query, (vin,vin))
    data_veh_buyer = cursor.fetchone()
    metadata.append('buyer_info')
    vehicles_details["buyer_info"] = data_veh_buyer
    #salesperson's information, sales date
    vehicles_details["salesperson"] = {}
    query = '''SELECT CONCAT_WS(' ',s.first_name, s.last_name) as salesperson, b.sale_date
                FROM Vehicle v
                LEFT JOIN Buy b ON v.vin = b.vin
                LEFT JOIN Salespeople s ON b.username = s.username
                WHERE v.vin = %s'''
    cursor = conn.cursor()
    cursor.execute(query, (vin,))
    data_veh_sales = cursor.fetchone()
    metadata.append('sale_info')
    vehicles_details["sale_info"] = data_veh_sales

    return {'data': vehicles_details, 'metadata': metadata}

def get_vehicle_sold():
    conn = g.conn
    query = f"""
        with vehicles_with_status_and_color as (
            select
                v.*,
                array_agg(vc.color) as colors
            from public.vehicle v
            join vehiclecolor vc on vc.vin = v.vin
            group by v.vin
        )
        select
            v.*
        from buy
        inner join vehicles_with_status_and_color v on v.vin = buy.vin;
    """
    cursor = conn.cursor()
    cursor.execute(query)

    response = {}
    columns = [desc[0] for desc in cursor.description]
    response["metadata"] = columns

    data = cursor.fetchall()
    response["data"] = data

    return response

def get_vehicle_unsold():
    conn = g.conn
    query = f"""
        with vehicles_with_status_and_color as (
            select
                v.*,
                array_agg(vc.color) as colors
            from public.vehicle v
            join vehiclecolor vc on vc.vin = v.vin
            group by v.vin
        )
        select 
            v1.*
        from vehicles_with_status_and_color v1
        except
        select
            v2.*
        from buy
        inner join vehicles_with_status_and_color v2 on v2.vin = buy.vin;
    """
    cursor = conn.cursor()
    cursor.execute(query)

    response = {}
    columns = [desc[0] for desc in cursor.description]
    response["metadata"] = columns

    data = cursor.fetchall()
    response["data"] = data

    return response

def get_vehicle_all():
    conn = g.conn
    query = f"""
        with vehicles_with_status_and_color as (
            select
                v.*,
                array_agg(vc.color) as colors
            from public.vehicle v
            join vehiclecolor vc on vc.vin = v.vin
            group by v.vin
        )
        select *
        from vehicles_with_status_and_color v;
    """
    cursor = conn.cursor()
    cursor.execute(query)

    response = {}
    columns = [desc[0] for desc in cursor.description]
    response["metadata"] = columns

    data = cursor.fetchall()
    response["data"] = data

    return response