from application import app
from application.models.user import db, User
from flask import request, jsonify, abort
from json import loads



def paginate_users(users, page):
    users_per_page = 5
    start = (page - 1) * users_per_page
    end = start + users_per_page
    current_users = [user.format() for user in users]
    return current_users[start:end]


# Get users
@app.route('/api/users')
def get_users():
    users = User.query.order_by(User.id).all()
    page = request.args.get('page', 1, type=int)
    current_users = paginate_users(users, page)
    
    if len(current_users) == 0:
        return abort(404)

    return jsonify({
        'success': True,
        'users': current_users,
        'total_users': len(users)
    })


# Get a specifc User by id
@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        return abort(404)
    return jsonify({
        'success': True,
        'user':user.format()
    })


# Add new user
@app.route('/api/users', methods=['POST'])
def add_user():
    body = None
    error = False
    try:
        name = request.form.get('name')
        user = User(name=name)
        user.create()
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
        name = data.get('name', None)
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
        return abort(500)
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
    
    if search_result is not None:
        return jsonify({
            'success': True, 
            'users': [user.format() for user in search_result]
        })
    else:
        return abort(404)
