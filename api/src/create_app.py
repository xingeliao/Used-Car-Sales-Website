from flask import Flask, g, request
from flask_cors import CORS

import logging
import psycopg2 as pg
import psycopg2.extras as extras

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    
    conn_info = {
        'host': 'omscs-postgres-flex.postgres.database.azure.com',
        'user': 'yzheng486',
        'password': 'TTDream_2023',
        'database': 'cs6400'
    }

    @app.before_request
    def establish_db_conn():
        conn = None
        try:
            conn = pg.connect(**conn_info, cursor_factory=extras.RealDictCursor)
        except:
            logger.error('something went wrong when establishing db connection')
        else:
            g.conn = conn

    @app.before_request
    def get_user_role():
        print(request.cookies)
        user_role = request.cookies.get('user_role', None)
        if user_role:
            g.user_role = user_role

    @app.after_request
    def close_db_conn(response):
        conn = g.pop('conn', None)
        if conn:
            conn.close()
        return response

    from team85.view.report import reports_bp
    from team85.view.vehicle import vehicle_bp
    from team85.view.sale import sale_bp
    from team85.view.part import part_bp
    from team85.view.vendor import vendor_bp
    from team85.view.manufacturer import manu_bp
    from team85.view.vehicle_type import vehicle_type_bp
    from team85.view.login import login_bp
    from team85.view.customer import customer_bp
    from team85.view.business_customer import business_bp
    from team85.view.individual_customer import individ_bp
    

    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(reports_bp, url_prefix='/report')
    app.register_blueprint(vehicle_bp, url_prefix='/vehicle')
    app.register_blueprint(sale_bp, url_prefix='/sale')
    app.register_blueprint(part_bp, url_prefix='/part')
    app.register_blueprint(vendor_bp, url_prefix='/vendor')
    app.register_blueprint(manu_bp, url_prefix='/manufacturer')
    app.register_blueprint(vehicle_type_bp, url_prefix='/vehicle-type')
    app.register_blueprint(customer_bp, url_prefix='/customer')
    app.register_blueprint(business_bp, url_prefix='/customer-business')
    app.register_blueprint(individ_bp, url_prefix='/customer-individual')
    
    return app