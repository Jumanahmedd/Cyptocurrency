from wtforms import Form, StringField, DecimalField, IntegerField, TextAreaField, PasswordField, validators

class Registeration_form(Form):
    name = StringField('Full Name', [validators.Length(min=1,max=30)])
    username = StringField('Username', [validators.Length(min=4,max=30)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('Password',[validators.DataRequired(), validators.EqualTo('confirm', message='Password does not match')])
    confirm = PasswordField('Confirm Password')

class sendMoney_form(Form):
    username = StringField('Username', [validators.Length(min=4,max=30)])
    amount = StringField('Amount', [validators.Length(min=1,max=50)])

class buying_form(Form):
    amount = StringField('Amount', [validators.Length(min=1,max=50)])
