from flask import Flask, session, redirect, url_for, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import Email, Length, Regexp, EqualTo

import db  # if error, right-click parent directory "mark directory as" "sources root"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key for session application'


class LoginForm(FlaskForm):
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


def authenticate_user(fname, lname, email, pword):
    if len(fname) < 5:
        return False

    if len(lname) < 5:
        return False

    ## fake_user_database = {}
    ## fake_user_database['ds@cse.taylor.edu'] = 'Pa$$word123'
    ## fake_user_database['bnroller@taylor.edu'] = 'Gr3atteach!'

    # if email in db.login(email):
    #    if db[email] == pword:  ## how do I do this?
    #        return True

    return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # provide user a login form
    register_form = LoginForm()

    # if the info is valid
    if register_form.validate_on_submit():
        member = db.find_member(register_form.email.data)

        if member is not None:
            flash("Member {} already exists".format(register_form.email.data))
        else:
            rowcount = db.create_member(register_form.email.data,
                                        register_form.first_name.data,
                                        register_form.last_name.data,
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
@app.route('/login')
def login():
    login_form = LoginForm()
    # if the info is valid
    if login_form.validate_on_submit():
        member = db.find_member(login_form.email.data)

        if member is None:
            flash("Member {} does not exist".format(login_form.email.data))
        else:
            # fill the session in with the details
            session['firstName'] = login_form.firstName.data
            session['lastName'] = login_form.lastName.data
            session['email'] = login_form.email.data
            session['password'] = login_form.password.data

            flash("Member {} logged in".format(login_form.email.data))
            return redirect(url_for('index'))

        flash('User logged in')
        return redirect(url_for('confirmation'))

    return render_template('login.html', form=login_form)


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('remember', None)

    flash('Logged out')
    return redirect(url_for('index'))


app.run(debug=True)
