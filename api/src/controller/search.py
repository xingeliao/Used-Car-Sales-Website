from flask import Flask, request, render_template, g


# Function to execute raw SQL queries
def execute_query(query, parameters=None):
    conn = g.pop('conn') 
    with conn.cursor() as cursor:
        cursor.execute(query, parameters)
        result = cursor.fetchall()
        
    conn.close()
    return result


def vehicle_search():
    # Fetch data for dropdowns (example for manufacturer and vehicle type)
    conn = g.pop('conn') 

    # Query to fetch manufacturers
    with conn.cursor() as cursor:
        cursor.execute("SELECT manufacturer_name FROM VehicleManufacturer;")
        manufacturers = cursor.fetchall()

    # Query to fetch vehicle types
    with conn.cursor() as cursor:
        cursor.execute("SELECT vehicle_type FROM VehicleType;")
        vehicle_types = cursor.fetchall()
    
    # New query to fetch colors 
    with conn.cursor() as cursor:
        cursor.execute("SELECT DISTINCT color FROM VehicleColor;")
        colors = cursor.fetchall()

    # Close the connection
    conn.close()

    return render_template('vehicle_search.html', manufacturers=manufacturers, vehicle_types=vehicle_types, colors = colors)


def perform_vehicle_search():
    # Extract form data
    manufacturer = request.form.get('manufacturer')
    vehicle_type = request.form.get('vehicle_type')
    
    color = request.form.get('color')
    # Extract other form fields similarly

    # Connect to the database
    conn = g.pop('conn')

    # Construct and execute the search query
    query = """
        SELECT V.vin, V.vehicle_type, V.manufacturer_name, V.fuel_type, V.model_name, V.model_year, V.description, V.mileage, GROUP_CONCAT(VC.color) AS colors
        FROM Vehicle V 
        LEFT JOIN VehicleColor VC ON V.vin = VC.vin
        WHERE V.vehicle_type = %s AND V.manufacturer_name = %s AND VC.color = %s
        GROUP BY V.vin
        ORDER BY V.vin ASC
    """
    parameters = (vehicle_type, manufacturer, color)
    with conn.cursor() as cursor:
        cursor.execute(query, parameters)
        vehicles = cursor.fetchall()

    # Close the database connection
    conn.close()

    return render_template('vehicle_search_results.html', vehicles=vehicles)
