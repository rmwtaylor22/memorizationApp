from flask import Flask, session, redirect, url_for, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import Email, Length, Regexp, EqualTo

import db  # if error, right-click parent directory "mark directory as" "sources root"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key for session application'


class RegisterForm(FlaskForm):
    valid_pword = []
    valid_pword.append(Length(min=8))
    valid_pword.append(Regexp(r'.*[A-Za-z]', message="Password must have at least one letter"))
    valid_pword.append(Regexp(r'.*[0-9]', message="Password must have at least one digit"))
    valid_pword.append(Regexp(r'.*[!@#$%^&*_+=]', message="Password must have at least one special character"))

    long = []
    long.append(Length(min=4))

    firstName = StringField('First Name', validators=long)
    lastName = StringField('Last Name', validators=long)
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=valid_pword)
    passwordCheck = PasswordField('Password confirmation', validators=[EqualTo('password')])

    submit = SubmitField('Log in')


class LoginForm(FlaskForm):
    valid_pword = []
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=valid_pword)

    submit = SubmitField('Log in')


def authenticate_user(email, pword):
    thepw = db.passw_check(email)
    if thepw[0] == pword:
        return True
    return False

@app.before_request
def before_request():
    db.open_db_connection()


@app.teardown_request
def teardown_request(exception):
    db.close_db_connection()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # provide user a login form
    register_form = RegisterForm()

    # if the info is valid
    if register_form.validate_on_submit():
        member = db.find_member(register_form.email.data)

        if member is not None:
            flash("Member {} already exists".format(register_form.email.data))
        else:
            rowcount = db.create_member(register_form.email.data,
                                        register_form.firstName.data,
                                        register_form.lastName.data,
                                        register_form.password.data)

            if rowcount == 1:
                flash("Member {} created".format(register_form.email.data))
                return redirect(url_for('index'))
            else:
                flash("New member not created")
            # fill the session in with the details
            session['firstName'] = register_form.firstName.data
            session['lastName'] = register_form.lastName.data
            session['email'] = register_form.email.data
            session['password'] = register_form.password.data

        flash('User registered')
        return redirect(url_for('confirmation'))

    return render_template('register.html', form=register_form)


# @app.route('/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    # if the info is valid
    if login_form.validate_on_submit():
        member = db.find_member(login_form.email.data)
        if member is None:
            flash("Member {} does not exist".format(login_form.email.data))
        else:
            if authenticate_user(login_form.email.data, login_form.password.data):
                # fill the session in with the details
                session['firstName'] = member[1]
                session['lastName'] = member[2]
                session['email'] = login_form.email.data
                session['password'] = login_form.password.data

                flash("Member {} logged in".format(member[1]))
                return redirect(url_for('index'))
            else:
                flash("The password does not match the username".format(login_form.email.data))

        # flash('User logged in')
        # return redirect(url_for('confirmation'))

    return render_template('login.html', form=login_form)


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('remember', None)

    flash('Logged out')
    return redirect(url_for('index'))


app.run(debug=True)
