from flask import Blueprint, request, jsonify, make_response
from models import db
import models


turbines_bp = Blueprint('turbines', __name__, url_prefix='/turbines')
measurements_bp = Blueprint('measurements', __name__, url_prefix='/measurements')


@turbines_bp.route('/', methods=['GET', 'POST'])
def turbines():
    if request.method == 'GET':
        return jsonify([turbine.to_dict() for turbine in models.Turbine.query.all()])
    
    if request.method == 'POST':
        if not request.is_json:
            return make_response(jsonify("Bad request. Only application/json request body is accepted."), 400)
        try:
            data = request.get_json()
            serial = data['serial']
            turbine = models.Turbine(serial = serial)
            db.session.add(turbine)
            db.session.commit()
            return make_response(jsonify(turbine.id), 201)
        except KeyError:
            return make_response(jsonify("Bad request. Invalid json format."), 400)
        except Exception:
            return make_response(jsonify("Internal server error. Could not create new turbine record."), 500)
    return make_response(jsonify("Method not supported."), 404)


@turbines_bp.route('/<int:id>', methods=['GET', 'DELETE'])
def turbine(id):
    turbine = models.Turbine.query.filter_by(id=id).first()
    if turbine is None:
        return make_response(jsonify("Turbine with ID: {0} not found.".format(id)), 404)
    
    if request.method == 'GET':
        return jsonify(turbine.to_dict())
    
    if request.method == 'DELETE':
        try:
            db.session.delete(turbine)
            db.session.commit()
            return make_response('', 200)
        except Exception:
            return make_response(jsonify("Internal server error. Could not delete turbine record."), 500)
        
    return make_response(jsonify("Method not supported."), 404)


@measurements_bp.route('/', methods=['GET'])
def measurement():
    if request.method == 'GET':
        serial = request.args.get('serial')
        if serial is None:
            return jsonify([measurement.to_dict() for measurement in models.Measurement.query.all()])
            
        turbine = models.Turbine.query.filter_by(serial=serial).first()
        if turbine is None:
            return make_response(jsonify("Turbine with serial number: {0} does not exist".format(serial)), 404)
        
        return jsonify([measurement.to_dict() for measurement in turbine.measurements])
    
    return make_response(jsonify("Method not supported."), 404)