from flask import jsonify, Blueprint, request
import team85.controller.customer as c
import team85.controller.individual_customer as icc
import team85.controller.business_customer as bcc

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/search', methods=['GET'])
def search_customer():
    params = request.args
    customers = c.search_customer(**params)
    
    return jsonify(customers)

# Copied from Business and Individual view (not routed there)
@customer_bp.route('/add_individual', methods=['POST'])
def add_individual_customer():
    body = request.json
    added = icc.add_individual_customer(body)
    
    return jsonify(added)

@customer_bp.route('/add_business', methods=['POST'])
def add_business_customer():
    body = request.json
    added = bcc.add_business_customer(body)
    
    return jsonify(added)
