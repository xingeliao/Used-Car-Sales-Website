from flask import jsonify, Blueprint, request, Response
import team85.controller.part as poc

part_bp = Blueprint('parts', __name__)

# CRUD operations - create, read, update, delete

@part_bp.route('/order', methods=['POST'])
def add_part_order():
    body = request.json
    added = poc.add_part_order(body)
    
    return jsonify(added)

@part_bp.route('/order', methods=['DELETE'])
def delete_part_order():
    params = request.args
    deleted = poc.delete_part_order(**params)
    return jsonify(deleted)

@part_bp.route('/total_part_cost/<vin>', methods=['GET'])
def get_total_part_cost(vin):
    cost = poc.get_total_part_cost(vin)
    
    return jsonify(cost)
    
# @vehicle_bp.route('/', methods=['POST'])
# def add_vehicle():
#     body = request.body
#     added = vc.add_vehicle(body)

#     return jsonify(added)


# @vehicle_bp.route('/', methods=['PUT'])
# def update_vehicle():
#     pass
