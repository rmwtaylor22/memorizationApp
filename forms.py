from flask import Flask, session, redirect, url_for, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import Email, Length, Regexp, EqualTo

import db  # if error, right-click parent directory "mark directory as" "sources root"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key for session application'

class Placeholder(FlaskForm):
    long = []
    long.append(Length(min=3))
    match=[]
    match.append(Regexp(r'.*[A-Za-z]')) #add more validators here.
    #firstBlankAnswer=this needs to be connected to the database's verse blank that gets pulled in to the activity.
    firstBlank= StringField('First blank', validators=long)#, match, [EqualTo("firstBlankAnswer")])
    secondBlank = StringField('Second blank', validators=long)#,match,[EqualTo("secondBlankAnswer")])
    thirdBlank = StringField('Third blank', validators=long)#,match, [EqualTo("thirdBlankAnswer")])
    forthBlank = StringField('Forth blank', validators=long)#,match, [EqualTo("forthBlankAnswer")])
    fifthBlank = StringField('Fifth blank', validators=long)#,match, [EqualTo("fifthBlankAnswer")])




    submit = SubmitField('All filled in!')


@app.route('/Test', methods=['GET', 'POST'])
def test():
    return render_template('module_selection.html')

@app.route('/Placeholder', methods=['GET', 'POST'])
def placeholder():
    placeholder_form = Placeholder()

    if placeholder_form.validate_on_submit():
        # this is supposed to send the information in the forms to
        # the database right now it is displaying the information at
        # the bottom of the website.
        session['firstBlank'] = placeholder_form.firstBlank.data
        session['secondBlank'] = placeholder_form.secondBlank.data
        flash('User reached the modules page from activity.')
        return redirect(url_for('test'))

    return render_template('placeholder.html', form=placeholder_form)
class RegisterForm(FlaskForm):
    valid_pword = []
    valid_pword.append(Length(min=8))
    valid_pword.append(Regexp(r'.*[A-Za-z]', message="Password must have at least one letter"))
    valid_pword.append(Regexp(r'.*[0-9]', message="Password must have at least one digit"))
    valid_pword.append(Regexp(r'.*[!@#$%^&*_+=]', message="Password must have at least one special character"))

    long = []
    long.append(Length(min=4))

    firstName = StringField('Update First Name', validators=long)
    lastName = StringField('Update Last Name', validators=long)
    email = StringField('Update Email', validators=[Email()])
    password = PasswordField('Update Password', validators=valid_pword)
    passwordCheck = PasswordField('Password confirmation', validators=[EqualTo('password')])

    submit = SubmitField('Update')


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


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/activities')
def activities():
    return render_template('activities.html')


@app.route('/modules')
def modules():
    return render_template('modules.html')


@app.route('/friends')
def friends():
    return render_template('friends.html')


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
            else:
                flash("The password does not match the username".format(login_form.email.data))

        return redirect(url_for('home'))

    return render_template('login.html', form=login_form)


@app.route('/verse_selection')
def verse_selection():
    return render_template('verse_selection.html')


@app.route('/module_selection')
def module_selection():
    return render_template('module_selection.html')


@app.route("/update", methods=['GET', 'POST'])
def update():
    update_form = RegisterForm()

    # if the info is valid
    if update_form.validate_on_submit():
        rowcount = db.update(update_form.email.data,
                             update_form.firstName.data,
                             update_form.lastName.data,
                             update_form.password.data)

        if rowcount is None:
            flash("Member {} updated".format(update_form.email.data))
            return redirect(url_for('index'))
        else:
            flash("New member not created")

        # fill the session in with the details
        session['firstName'] = update_form.firstName.data
        session['lastName'] = update_form.lastName.data
        session['email'] = update_form.email.data
        session['password'] = update_form.password.data

        flash('User updated')
        return redirect(url_for('profile'))

    return render_template('update.html', form=update_form)


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('remember', None)

    flash('Logged out')
    return redirect(url_for('index'))


app.run(debug=True)
