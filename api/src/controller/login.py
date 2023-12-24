from datetime import datetime, timedelta, timezone
from flask import request, session, flash, g
import jwt

def login(user_id, password):
    conn = g.pop('conn', None)
    cursor = conn.cursor()

    query = f'''
        SELECT password, 'adminuser' as role FROM adminuser WHERE username=%s
        UNION
        SELECT password, 'clerk' as role FROM inventoryclerk WHERE username=%s
        UNION
        SELECT password, 'manager' as role FROM manager WHERE username=%s
        UNION
        SELECT password, 'owner' as role FROM owner WHERE username=%s; 
    '''
    
    cursor.execute(query,(user_id,user_id,user_id,user_id))
    if cursor.rowcount == 0:
        return {
            "error": "Username not found"
        }, 400

    user_info = cursor.fetchone()
    is_validated = (password == user_info.get('password'))
    if is_validated == False:
        return {
            "error": "Login credentials are not correct."
        }, 400
    
    # create jwt token
    user_token = jwt.encode(
        {
            "user_id": user_id,
            "user_role": user_info.get('role'),
            "iat": datetime.now(tz=timezone.utc), # Issued time
            "exp": (datetime.now(tz=timezone.utc) + timedelta(hours=72)) # Expiration time
        },
        "TEAM085_SECRET_KEY",
        algorithm="HS256"
    )

    return {"token": user_token}


def basic_auth(username, password):
    conn = g.pop('conn', None)
    cursor = conn.cursor()
    
    query = f"""
        select
            username,
            user_role
        from public.user
        where username = '{username}' and password = '{password}'
    """
    cursor.execute(query)
    if cursor.rowcount == 0:
        return None
    response = {}
    columns = [desc[0] for desc in cursor.description]
    response['metadata'] = columns
    
    data = cursor.fetchone()
    response['data'] = data
    return response
    
            