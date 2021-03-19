from flask import Flask, session, redirect, url_for, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import Email, Length, Regexp, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key for session application'


class LoginForm(FlaskForm):
    valid_pword = []
    valid_pword.append(Length(min=8))
    valid_pword.append(Regexp(r'.*[A-Za-z]', message="Must have at least one letter"))
    valid_pword.append(Regexp(r'.*[0-9]', message="Must have at least one digit"))
    valid_pword.append(Regexp(r'.*[!@#$%^&*_+=]', message="Must have at least one special character"))

    long = []
    long.append(Length(min=5))

    firstName = StringField('First Name', validators=long)
    lastName = StringField('Last Name', validators=long)
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=valid_pword)
    passwordCheck = PasswordField('Password confirmation', validators=[EqualTo('password')])

    submit = SubmitField('Register')


def authenticate_user(fname, lname, email, pword):
    if len(fname) < 5:
        return False

    if len(lname) < 5:
        return False

    fake_user_database = {}
    fake_user_database['ds@cse.taylor.edu'] = 'Pa$$word123'
    fake_user_database['bnroller@taylor.edu'] = 'Gr3atteach!'

    if email in fake_user_database:
        if fake_user_database[email] == pword:
            return True

    return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def login():
    register_form = LoginForm()

    if register_form.validate_on_submit():
        ##if not authenticate_user(register_form.firstName.data, register_form.lastName.data, register_form.email.data, register_form.password.data):
        ##   flash('There are errors in your registration form:')
        ##else:
        session['firstName'] = register_form.firstName.data
        session['email'] = register_form.email.data

        flash('User registered')
        return redirect(url_for('confirmation'))

    return render_template('register.html', form=register_form)


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('remember', None)

    flash('Logged out')
    return redirect(url_for('index'))

app.run(debug=True)