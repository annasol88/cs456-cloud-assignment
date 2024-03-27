from flask import Blueprint, request, jsonify, make_response
from models import db
import models

'''
This package defines all the routes supported by the Turbine web service.  
'''


# The Supported Blueprints.
turbines_bp = Blueprint('turbines', __name__, url_prefix='/turbines')
measurements_bp = Blueprint('measurements', __name__, url_prefix='/measurements')


'''
Base turbine route for fetching all turbines and creating new ones
GET - returns a list of all turbines stored in the DB
POST - Creates a new Turbine record in the DB
Other HTTP methods are not accepted
'''
@turbines_bp.route('/', methods=['GET', 'POST'])
def turbines():
    if request.method == 'GET':
        # Query and return all turbine's in DB.
        return jsonify([turbine.to_dict() for turbine in models.Turbine.query.all()])
    
    if request.method == 'POST':
        if not request.is_json:
            # Do not proceed and return 400 if request format is invalid.
            return make_response(jsonify("Bad request. Only application/json request body is accepted."), 400)
        
        try:
            data = request.get_json()
            serial = data['serial']
            # Create a new turbine Object
            turbine = models.Turbine(serial = serial)
            # Commit new Turbine to DB
            db.session.add(turbine)
            db.session.commit()
            return make_response(jsonify(turbine.id), 201)
        
        except KeyError:
            # If request body does not contain 'serial' key return 400.
            return make_response(jsonify("Bad request. Invalid json format."), 400)
        
        except Exception:
            # If an error occurs when saving to the DB return a 500.
            return make_response(jsonify("Internal server error. Could not create new turbine record."), 500)
    
    # Return 404 for invalid method type in request.    
    return make_response(jsonify("Method not supported."), 404)


'''
Base Turbine route with path paramater for fetching and deleting individual turbines by their ID
GET - returns a turbine object identified by the id path parameter 
DELETE - deletes the turbine object identified by the id path parameter
Other HTTP methods are not accepted
'''
@turbines_bp.route('/<int:id>', methods=['GET', 'DELETE'])
def turbine(id):
    # Get turbine object that corresponds to the id path parameter in the database.
    turbine = models.Turbine.query.filter_by(id=id).first()
    
    if turbine is None:
        # Do not proceed and return 400 if the turbine does not exist.
        return make_response(jsonify("Turbine with ID: {0} not found.".format(id)), 404)
    
    if request.method == 'GET':
        # return the turbine object that was fetched.
        return jsonify(turbine.to_dict())
    
    if request.method == 'DELETE':
        try:
            # Try to delete Turbine object that was fetched.
            db.session.delete(turbine)
            db.session.commit()
            return make_response('', 200)
        
        except Exception:
            # If a DB error occurs return 500.
            return make_response(jsonify("Internal server error. Could not delete turbine record."), 500)
    
    # Return 404 for invalid method type in request.   
    return make_response(jsonify("Method not supported."), 404)


'''
Base Measurement route for fetching all measurements in the DB 
with the option to specify a turine serial to limit results.
GET - Retruns all measurements recorded in the DB 
or all measurements corresponding to a given turbine serial if provided
Other HTTP methods are not accepted
'''
@measurements_bp.route('/', methods=['GET'])
def measurement():
    if request.method == 'GET':
        # Get turbine serial if it is present as a qury parameter.
        serial = request.args.get('serial')
        
        if serial is None:
            # Return all measurements in the DB if no turbine serial provided.
            return jsonify([measurement.to_dict() for measurement in models.Measurement.query.all()])
        
        # Verify that a turbine with the provided serial exists.
        turbine = models.Turbine.query.filter_by(serial=serial).first()
        if turbine is None:
            # Return 400 if invalid serial is provided in request.
            return make_response(jsonify("Turbine with serial number: {0} does not exist".format(serial)), 404)
        
        # Return all measurements associated with the turbine.
        return jsonify([measurement.to_dict() for measurement in turbine.measurements])
    
    # Return 404 for invalid method type in request.  
    return make_response(jsonify("Method not supported."), 404)