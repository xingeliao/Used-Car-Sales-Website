from flask import jsonify, Blueprint, request, Response
import team85.controller.sale as sc

sale_bp = Blueprint('sales', __name__)

# CRUD operations - create, read, update, delete

@sale_bp.route('/', methods=['POST'])
def add_sale():
    body = request.json
    added = sc.add_sale(body)
    
    return jsonify(added)


# @vehicle_bp.route('/', methods=['POST'])
# def add_vehicle():
#     body = request.body
#     added = vc.add_vehicle(body)

#     return jsonify(added)


# @vehicle_bp.route('/', methods=['PUT'])
# def update_vehicle():
#     pass
