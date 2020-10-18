from flask.templating import render_template
from application import app
from application.models import db, User
from flask import request, redirect, jsonify, abort
from json import loads


# Get home page
@app.route('/')
def get_index():
    return redirect('/users')

# Get all users
@app.route('/users')
def get_users():
    users_query = User.query.order_by(User.name).all()
    return render_template('users.html', users=users_query)

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
        return jsonify(body)
    else:
        return abort(500)
