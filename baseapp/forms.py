from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField,PasswordField



class AddForm(FlaskForm):

    name = StringField("Title of Book    ")
    auther = StringField("Auther of Book    ")
    price = StringField("Price of the Book ")
    image = StringField("url for image ")
    submit = SubmitField("Add Book")