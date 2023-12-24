from flask import jsonify, Blueprint, request
import team85.controller.individual_customer as icc

individ_bp = Blueprint('individualcustomer', __name__)

@individ_bp.route('/search/<drivers_lino>', methods=['GET'])
def get_customer(drivers_lino):
    customer = icc.get_individual_customer(drivers_lino)
    
    return jsonify(customer)

@individ_bp.route('/add', methods=['POST'])
def add_customer():
    body = request.json
    added = icc.add_individual_customer(body)
    
    return jsonify(added)
