from flask import current_app as app, jsonify, request
from .auth import basic_auth, token_auth
from .models import Employee, Item, db, error_handling, admin_only
from werkzeug.security import generate_password_hash
import uuid  # to generate random public id


# to create a new account, no authentication is required here, employee's id is protected by generating random public id
@app.route('/employee', methods=['POST'])
def create_employee():
    # get import json data
    data = request.get_json()
    # hash a password
    password_hash = generate_password_hash(data['password'], method='sha256')

    # if username already exists
    if Employee.query.filter_by(username=data['username']).first():
        return error_handling(400, 'Username already exists')
    # otherwise, create new employee in the database
    new_employee = Employee(public_id=str(uuid.uuid4()), username=data['username'], password=password_hash,
                            admin=data['admin'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'New employee is now created'}), 201


# basic authentication is required for login route and token authentication is required for all other routes
# each employee will receive a token upon signing in
@app.route('/login')
@basic_auth.login_required
def login():
    # if login
    if basic_auth.current_user():
        # then generate the token for current employee
        token = basic_auth.current_user().generate_token()
        db.session.commit()
        return jsonify({'Here is your token number': token})


# to get all employees, token authentication is required so at least one account must be created
# for Admin users only
@app.route('/employee', methods=['GET'])
@token_auth.login_required
def get_employee_list():
    # if not admin
    if not basic_auth.current_user().admin:
        return admin_only()

    # otherwise, query the 'employee' table to access employees data in the database
    employees = Employee.query.all()
    # create a list to store all employees data
    employees_data = []
    # to display messages on 'Response Body'
    for employee in employees:
        data = {'public_id': employee.public_id, 'username': employee.username, 'password': employee.password,
                'admin': employee.admin}
        employees_data.append(data)

    return jsonify({'employees': employees_data}), 200


# to get a particular employee, token authentication is required - for Admin users only
@app.route('/employee/<public_id>', methods=['GET'])
@token_auth.login_required
def get_employee(public_id):
    if not basic_auth.current_user().admin:
        return admin_only()

    # query for one particular employee from the database
    employee = Employee.query.filter_by(public_id=public_id).first()

    if not employee:
        return jsonify({'message': 'No employee found!'})
    employee_data = {'public_id': employee.public_id, 'username': employee.username, 'password': employee.password,
                     'admin': employee.admin}

    return jsonify({'employee': employee_data}), 200


# to delete one particular employee from the database, token authentication is required - for Admin users only
@app.route('/employee/<public_id>', methods=['DELETE'])
@token_auth.login_required
def delete_employee(public_id):
    if not basic_auth.current_user().admin:
        return admin_only()

    # query for one particular employee from the database by their public id
    employee = Employee.query.filter_by(public_id=public_id).first()

    if not employee:
        return jsonify({'message': 'No employee found or employee is already deleted'})
    db.session.delete(employee)
    db.session.commit()
    return {'message': 'This employee is now deleted'}, 200


# to create a new item, token authentication is required - for both Employee and Admin users
@app.route('/item', methods=['POST'])
@token_auth.login_required
def create_item():
    # get import json data
    data = request.get_json()
    # if item's name already exists
    if Item.query.filter_by(name=data['name']).first():
        return error_handling(400, 'Duplicate Name')
    # Otherwise, create a new item in the database
    new_item = Item(name=data['name'], price=data['price'], employee_id=basic_auth.current_user().id)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': "New item is now created!"}), 201


# to get all items, token authentication is required - for both Employee and Admin users
@app.route('/item', methods=['GET'])
@token_auth.login_required
def get_all_items():
    # query the 'item' table to access items data in the database
    items = Item.query.filter_by(employee_id=basic_auth.current_user().id).all()
    # create a list to store all items data
    items_data = []
    # to display messages on 'Response Body'
    for item in items:
        data = {'id': item.id, 'name': item.name, 'price': item.price}
        items_data.append(data)
    if not items_data:
        return jsonify({'message': 'No item has been created'})
    return jsonify({'items': items_data}), 200


# to get a particular item, token authentication is required- for both Employee and Admin users
@app.route('/item/<item_id>', methods=['GET'])
@token_auth.login_required
def get_item(item_id):
    # query for a particular item from the database
    item = Item.query.filter_by(id=item_id, employee_id=basic_auth.current_user().id).first()

    # if this item does not exist
    if not item:
        return jsonify({'message': 'No item found!'})
    item_data = {'id': item.id, 'name': item.name, 'price': item.price}
    return jsonify(item_data), 200


# to delete a particular item from the database, token authentication is required - for both Employee and Admin users
@app.route('/item/<item_id>', methods=['DELETE'])
@token_auth.login_required
def delete_item(item_id):
    # query for a particular item of current Employee or Admin user from the database by id
    item = Item.query.filter_by(id=item_id, employee_id=basic_auth.current_user().id).first()

    #  if this item does not exist
    if not item:
        return jsonify({'message': 'No item found or item is already deleted'})
    # otherwise, delete this item
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'This item is now deleted!'}), 200
