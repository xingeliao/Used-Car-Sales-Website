from flask import jsonify, Blueprint, request
import team85.controller.business_customer as bcc

business_bp = Blueprint('businesscustomer', __name__)

@business_bp.route('/search/<tax_id_no>', methods=['GET'])
def get_customer(tax_id_no):
    customer = bcc.get_business_customer(tax_id_no)
    
    return jsonify(customer)

@business_bp.route('/add', methods=['POST'])
def add_customer():
    body = request.json
    added = bcc.add_business_customer(body)
    
    return jsonify(added)
