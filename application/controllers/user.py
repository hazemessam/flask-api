from application import app
from application.models import db, User
from flask import render_template, request, redirect, jsonify, abort


# Get home page
@app.route('/')
def get_index():
    return redirect('/users')

# Get all users
@app.route('/users')
def get_users():
    users_query = User.query.order_by(User.name).all()
    return render_template('users.html', users=users_query)

# Get a specifc User by id
@app.route('/users/<int:id>')
def get_user(id):
    body = None
    error = False
    try:
        user = User.query.get(id)
        body = {
            'id': user.id,
            'name': user.name
        }
    except Exception as e:
        error = True
        print(e)

    if not error:
        return jsonify(body)
    else:
        return abort(500)

# Get add new user form
@app.route('/users/forms/add')
def get_add_user_form():
   return render_template('forms/add_user.html')

# Add new user
@app.route('/users', methods=['POST'])
def add_user():
    body = None
    error = False
    try:
        name = request.form.get('name')
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        body = {
            'success': True,
            'name': user.name,
            'id': user.id
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

# Delete a specific user by id
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    body = None
    error = False
    try:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        body = {
            'success': True,
            'name': user.name,
            'id': user.id
        }
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
