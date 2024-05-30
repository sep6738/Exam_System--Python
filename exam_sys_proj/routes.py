from flask import Blueprint, render_template, request, redirect, url_for, flash
from exam_sys_proj.models import db, Users

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        roleID = request.form['roleID']

        # Here you can add your logic to save the user to the database
        # For example:
        new_user = Users(userName=username, passWord=password, name=name, email=email, roleID=roleID)
        db.session.add(new_user)
        db.session.commit()

        flash('注册成功！')
        return redirect(url_for('main.index'))
    return render_template('register.html')