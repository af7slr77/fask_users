from flask import Flask, render_template, request, flash, session, redirect, url_for, abort
from models import db, User
import os
from werkzeug.security import generate_password_hash, check_password_hash # functions for encoding and password verification
from flask_login import LoginManager, login_user
from user_login import UserLogin

sk = os.urandom(20).hex() # gen SECRET_KEY
SALT = "salt4747646767876"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db" # payh to db
app.config["SECRET_KEY"] = "f5308d1071cf547745010e636a99be835c085cfa" # need for session
db.init_app(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
	return UserLogin().from_db(user_id, db)


@app.route("/reg_user", methods=['POST','GET'])
def reg_user():
	if request.method == "GET":
		return render_template("reg_user.html")
	if len(request.form['username'])> 1 and len(request.form['password'])> 1:
		new_user = User(request.form['username'], generate_password_hash(request.form['password'] + SALT))
		db.create_all()
		db.session.add(new_user)
		db.session.commit()
		flash('User created!')
		return redirect(url_for('login'))
	else:
		flash('Sending error')


@app.route("/login", methods=['POST','GET'])
def login():
	
	# if 'userLogged' in session:
	# 	return redirect(url_for('profile', username=session['userLogged']))
	
	if request.method == 'POST' and \
		request.form['username'] == db.one_or_404(db.select(User).filter_by(username=request.form['username'])).username:
		password = request.form['password']
		db_password = db.one_or_404(db.select(User).filter_by(username=request.form['username'])).password
		if check_password_hash(db_password, password + SALT):
			user = db.one_or_404(db.select(User).filter_by(username=request.form['username']))
			userlogin = UserLogin().crate(user)
			print(user)
			login_user(userlogin)
			# session['userLogged'] = request.form['username']
			return redirect(url_for('profile'))
	return render_template("login.html")



@app.route('/profile')
def profile():
	user_id = session.get('_user_id')
	if user_id is None:
		abort(401)
	user = db.one_or_404(db.select(User).filter_by(id=user_id))
	# if 'userLogged' not in session or session['userLogged'] != username: # checks whether the user is correct if not returns a 401 error
	if user is None:
		abort(404)
	return render_template('profile.html', username=user.username)


if __name__ == "__main__":
	app.run(debug=True)