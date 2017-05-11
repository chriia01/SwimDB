from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField

from wtforms import validators, ValidationError

class SwimmerForm(Form):
    name = TextField("Name of swimmer",[validators.Required("Please enter the name")])
    gender = RadioField("Gender",[validators.Required("Please select a gender")] , choices=[("M","Male"),("F","Female")])
    team = TextField("Swimmer's Team",[validators.Required("Please enter a team")])
    date = TextField("Birthdate (YYYY,M,D)", [validators.Required("Please enter a birthdate")])
    submit = SubmitField("Submit")

class TimeForm(Form):
    events = [
        ('50 freestyle','50 Freestyle'),
        ('100 freestyle','100 Freestyle'),
        ('200 freestyle','200 Freestyle'),
        ('500 freestyle','500 Freestyle'),
        ('1000 freestyle','1000 Freestyle'),
        ('1650 freestyle','1650 Freestyle'),
        ('100 butterfly','100 Butterfly'),
        ('200 butterfly','200 Butterfly'),
        ('100 backstroke', '100 Backstroke'),
        ('200 backstroke', '200 Backstroke'),
        ('100 breaststroke', '100 Breaststroke'),
        ('200 breaststroke', '200 Breaststroke'),
        ('200 im', '200 IM'),
        ('400 im', '400 IM'),
    ]

    event = SelectField("Event", [ validators.Required("Please select an event")] ,choices = events )
    minutes = IntegerField("Time (min,sec,ms)", [validators.NumberRange(min=-1,max=59, message="Please enter a number between 0 and 59")], default=0)
    seconds = IntegerField("Seconds",[validators.Required("Please enter seconds"), validators.NumberRange(min=0,max=59, message="Please enter a number between 0 and 59")])
    milliseconds = IntegerField("Milliseconds",[validators.Required("Please enter milliseconds"), validators.NumberRange(min=0,max=59, message="Please enter a number between 0 and 59")])
    dateOfTime = TextField("Date of time (YYYY,M,D)", [validators.Required("Please enter a birthdate")])

    submit = SubmitField("Submit")