from flask import Flask, session, redirect, url_for, render_template, flash, g
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField
from wtforms.validators import Email, Length, Regexp, EqualTo, DataRequired

import db

def modules(chapter, verse):
    return render_template('module_base.html')

def get_module_verses(id):
