from flask import jsonify, Blueprint, request, g
import team85.controller.vehicle as vc
import team85.controller.part_order as po
import team85.controller.part as parts

vehicle_bp = Blueprint('vehicles', __name__)

@vehicle_bp.route('/', methods=['GET'])
def public_vehicle_search():
    response = None
    search_type = request.args.get('search-type', None)
    if search_type:
        if search_type == 'sold':
            response = vc.get_vehicle_sold()
        elif search_type == 'unsold':
            response = vc.get_vehicle_unsold()
        else:
            response = vc.get_vehicle_all()
    else:
        response = vc.get_vehicle()
    
    return jsonify(response)

@vehicle_bp.route('/<vin>', methods=['GET'])
def vehicle_search_by_vin_manager(vin):
    response = vc.get_vehicle_by_vin_manager(vin)
    return jsonify(response)


@vehicle_bp.route('/color/', methods=['GET'])
def get_vehicle_colors():
    response = vc.get_vehicle_color()
    
    return jsonify(response)


@vehicle_bp.route('/part-order/<order_id>', methods=['GET'])
def part_order(order_id):
    all_parts_order_for_vehicle = po.get_part_order(order_id)
    
    return jsonify(all_parts_order_for_vehicle)


@vehicle_bp.route('/update-part-status', methods=['POST'])
def update_part_status():
    content = request.json
    part_id = content.get("part_id")
    new_status =  content.get("status")
    updated = parts.update_part_status(part_id, new_status)
    return jsonify(updated)


@vehicle_bp.route('/', methods=['POST'])
def add_vehicle():
    body = request.json
    added = vc.add_vehicle(body)

    return jsonify(added)
