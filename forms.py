from flask import Flask, session, redirect, url_for, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField
from wtforms.validators import Email, Length, Regexp, EqualTo, DataRequired

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


class VerseForm(FlaskForm):
    book = SelectField(
        'Book',
        [DataRequired()],
        choices=[
            ('Genesis', 'gen'),
            ('Exodus', 'exo'),
            ('Leviticus', 'lev'),
            ('Numbers', 'num'),
            ('Deuteronomy', 'duet'),
            ('Joshua', 'jos')
        ]
    )

    chapter = SelectField(
        'Chapter',
        [DataRequired()],
        choices=[
            ('1', '.1'),
            ('2', '.2'),
            ('3', '.3')
        ]
    )

    verse = SelectField(
        'Verse',
        [DataRequired()],
        choices=[
            ('1', '.1'),
            ('2', '.2'),
            ('3', '.3')
        ]
    )
    submit = SubmitField('Submit')


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

@app.route('/selectVerse', methods=['GET'])
def dropdown():
    colours = ['Red', 'Blue', 'Black', 'Orange']
    return render_template('test.html', colours=colours)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # provide user a login form
    signup_form = RegisterForm()

    # if the info is valid
    if signup_form.validate_on_submit():
        member = db.find_member(signup_form.email.data)

        if member is not None:
            flash("Member {} already exists".format(signup_form.email.data))
        else:
            rowcount = db.create_member(signup_form.email.data,
                                        signup_form.firstName.data,
                                        signup_form.lastName.data,
                                        signup_form.password.data)

            if rowcount == 1:
                flash("Member {} created".format(signup_form.email.data))
                return redirect(url_for('index'))
            else:
                flash("New member not created")

        flash('Verse found')
        return redirect(url_for('home'))

    return render_template('register.html', form=signup_form)


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
    verse_form = VerseForm()
    # if the info is valid
    if verse_form.validate_on_submit():
        verse = db.find_verse(verse_form.book.data, verse_form.chapter.data, verse_form.verse.data)
        if verse is None:
            flash("verse does not exist")
        else:
            session['verse'] = verse[1]  # hopefully this returns the text. Might need to use index 0
        return render_template('verse_selection.html')

    return render_template('login.html', form=verse_form)


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
