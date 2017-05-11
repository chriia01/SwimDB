from flask import Flask, render_template, request, flash, redirect
from sqlalchemy import create_engine, MetaData, Table, func, literal
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from forms import SwimmerForm, TimeForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from datetime import date, time
from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey, create_engine, Time


#Create engine, allowing us to create tables
engine = create_engine('sqlite:///swim.db')
Base = declarative_base()

#Create a session, letting us add items to table
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

#A middle table for swimmers and races, including times
class swimmer_race(Base):
    __tablename__ = 'swimmer_race'
    swimmer_race_id = Column(Integer, primary_key=True, autoincrement=True)
    swimmer_id = Column(Integer, ForeignKey('swimmer.id'))
    race_id = Column(Integer, ForeignKey('race.id'))
    time = Column(Time)
    date_of_time = Column(Date)

    swimmer = relationship('swimmer')
    race = relationship('race')

#A list of all the swimmers, along with their birthday and team
class swimmer(Base):
    __tablename__ = 'swimmer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    gender = Column(String)
    team = Column(String)
    birthdate = Column(Date)
    swimmer = relationship('swimmer_race')

    def __repr__(self):
        return "swimmer({}, {}, {}, {})".format(self.name, self.gender,self.team, self.birthdate)

#A list of all the events
class race(Base):
    __tablename__= 'race'
    id = Column(Integer, primary_key=True)
    distance = Column(Integer)
    stroke = Column(String)
    race = relationship('swimmer_race')

    def __repr__(self):
        return "race ({}, {})".format(self.stroke, self.distance)

#Creates the tables
Base.metadata.create_all(engine)

#Add every race
if session.query(race.id).filter_by(id=1).count() == 0:
    session.add(race(id = 1, distance=50, stroke="freestyle")) #1
    session.add(race(id = 2, distance=100, stroke="freestyle")) #2
    session.add(race(id = 3, distance=200, stroke="freestyle")) #3
    session.add(race(id = 4, distance=500, stroke="freestyle")) #4
    session.add(race(id = 5, distance=1000, stroke="freestyle")) #5
    session.add(race(id = 6, distance=1650, stroke="freestyle")) #6

    session.add(race(id = 7, distance=100, stroke="butterfly")) #7
    session.add(race(id = 8, distance=200, stroke="butterfly")) #8

    session.add(race(id = 9, distance=100, stroke="breaststroke")) #9
    session.add(race(id = 10, distance=200, stroke="breaststroke")) #10

    session.add(race(id = 11, distance=100, stroke="backstroke")) #11
    session.add(race(id = 12, distance=200, stroke="backstroke")) #12

    session.add(race(id = 13, distance=200, stroke="im")) #13
    session.add(race(id = 14, distance=400, stroke="im")) #14

'''
#Ian's times. Time is the way it is because it goes time(hr, min, sec, ms)
session.add(swimmer_race(swimmer_id=1, race_id=1, time=time(0,0,21,66) , date_of_time=date(2017,2,9)))
session.add(swimmer_race(swimmer_id=1, race_id=2, time=time(0,0,47,85) , date_of_time=date(2017,2,11)))
session.add(swimmer_race(swimmer_id=1, race_id=5, time=time(0,11,11,9), date_of_time=date(2016, 11,5)))
session.add(swimmer_race(swimmer_id=1, race_id=7, time=time(0,0,56,44) , date_of_time=date(2017,2,10)))
 
#Gunnar's times. Time is the way it is because it goes time(hr, min, sec, ms)
session.add(swimmer_race(swimmer_id=2, race_id=1, time=time(0,0,22,58) , date_of_time=date(2017,2,9)))
session.add(swimmer_race(swimmer_id=2, race_id=7, time=time(0,0,52,78) , date_of_time=date(2017,2,10)))
session.add(swimmer_race(swimmer_id=2, race_id=8, time=time(0,1,59,26) , date_of_time=date(2017,2,11)))
session.add(swimmer_race(swimmer_id=2, race_id=4, time=time(0,4,59,93) , date_of_time=date(2016,2,11)))
'''

#Push additions
session.commit()


app = Flask(__name__)
app.secret_key = 'development key'

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/new_swimmer', methods=['GET', 'POST'])
def new_swimmer():
    form = SwimmerForm(request.form)
    if request.method == 'POST' and form.validate():

        sd = form.date.data
        sd = sd.split(',')

        session.add(swimmer(name=form.name.data, gender=form.gender.data, team=form.team.data, birthdate=date(int(sd[0]), int(sd[1]), int(sd[2]))))
        session.commit()

        return redirect('/')
    return render_template('new_swimmer.html', form=form)

@app.route('/add_times/<swim_id>', methods=['GET','POST'])
def add_times(swim_id):
    form = TimeForm()
    if request.method == 'POST' and form.validate():
        swim_date = form.dateOfTime.data
        swim_date = swim_date.split(',')
        #swim_date = date(int(swim_date[0]), int(swim_date[1]), int(swim_date[2]))


        if form.minutes.data == "":
            time_min = 0
        else:
            time_min = int(form.minutes.data)

        swimTime = time(0,time_min,int(form.seconds.data), int(form.milliseconds.data)*10000)
        
        distance, stroke = form.event.data.split()
        distance = int(distance)

        for cur in session.query(race).filter_by(distance=distance).filter_by(stroke=stroke):
            event_id = cur.id
        session.add(swimmer_race(swimmer_id=swim_id, race_id=event_id, time = swimTime, date_of_time = date(int(swim_date[0]), int(swim_date[1]), int(swim_date[2]))))        
        session.commit()

        return redirect('/swimmer_page='+swim_id)
    return render_template('new_time.html', form=form, swim_id=swim_id)

@app.route('/swimmer_page=<swim_id>')
def swimmer_page(swim_id):
    lst = (session.query(swimmer, swimmer_race, race)
    	.join(swimmer_race)
    	.join(race)
    	.filter(swimmer.id == swim_id)
    	).all()
    real_swim_name = []
    for item in session.query(swimmer).filter(swimmer.id == swim_id):
    	real_swim_name.append(item)
    return render_template('swimmer_page.html', swim_name=lst, real_swim_name = real_swim_name[0])

@app.route('/moreinfo=<swim_id>')
def moreinfo(swim_id):
    for name in session.query(swimmer).filter_by(id=1):
        swimLst = name
    print(swimLst.birthdate)
    age = calculate_age(swimLst.birthdate)

    return render_template('moreinfo.html', data=swimLst, age=age)


@app.route('/search_swimmer=<lookup_name>')
def get_swimmer(lookup_name):

    swimLst = []
    for cur in session.query(swimmer).filter(swimmer.name.contains(func.lower(lookup_name))):
        swimLst.append(cur)
    return render_template('search_swimmer.html', data=swimLst, team_or_name=lookup_name)

@app.route('/search_team=<lookup_name>')
def search_team(lookup_name):

    swimLst = []
    for cur in session.query(swimmer).filter(swimmer.team.contains(func.lower(lookup_name))):
        swimLst.append(cur)
    return render_template('search_swimmer.html', data = swimLst, team_or_name=lookup_name)

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

if __name__ == "__main__":
    app.run(debug=True)
