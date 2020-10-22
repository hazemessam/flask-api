from application import app
from application.models import db, User
from flask import request, jsonify, abort
from json import loads


# Get all users
@app.route('/api/users')
def get_users():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 5
    end = start + 5
    
    users_query = User.query.all()
    users = [user.format() for user in users_query]
    
    return jsonify({
        'success': True,
        'users': users[start:end],
        'total_users': len(users)
    })


# Get a specifc User by id
@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    body = None
    if user:
        body = {
            'success': True,
            'user':user.format()
        }
    else:
        body = {'success': False}
    return jsonify(body)


# Add new user
@app.route('/api/users', methods=['POST'])
def add_user():
    body = None
    error = False
    try:
        name = request.form.get('name')
        user = User(name=name)
        user.create()
        body = user.format()
    except Exception as e:
        error = True
        db.session.rollback()
        print(e)
    finally:
        db.session.close()

    if not error:
        return jsonify(body), 201
    else:
        return abort(500)


# update a specific user
@app.route('/api/users/<int:id>', methods=['PATCH'])
def update_user(id):
    body = None
    error = False
    try:
        data = loads(request.data)
        name = data.get('name')
        user = User.query.get(id)
        user.name = name
        user.update()
        body = {
            'success': True,
            'user': user.format()
        }
    except Exception as e:
        error = True
        db.session.rollback()
        print(e)
    finally:
        db.session.close()

    if error: 
        body = {'success': False}
    return jsonify(body)


# Delete a specific user by id
@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    body = None
    error = False
    try:
        user = User.query.get(id)
        user.delete()
        body = user.format()
    except Exception as e:
        error = True
        db.session.rollback()
        print(e)
    finally:
        db.session.close()

    if not error:
        return jsonify(body)
    else:
        return abort(500)


# Search users
@app.route('/api/users/search')
def search_users():
    search_term = request.args.get('q', '', type=str)
    search_result = User.query.filter(User.name.ilike(f'%{search_term}%'))
    
    body = None
    if search_result is not None:
        body = {
            'success': True,
            'users': [user.format() for user in search_result]
        }
    else:
        body = {
            'success': False
        }
    return jsonify(body)
