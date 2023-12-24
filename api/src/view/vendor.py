from flask import jsonify, Blueprint, request
import team85.controller.vendor as vendorc

vendor_bp = Blueprint('vendors', __name__)

@vendor_bp.route('/', methods=['GET'])
def get_vendor():
    params = request.args
    all_vendors = vendorc.get_vendor(**params)
    
    return jsonify(all_vendors)


@vendor_bp.route('/', methods=['POST'])
def add_vendor():
    body = request.json
    added = vendorc.add_vendor(body)
    
    return jsonify(added)
