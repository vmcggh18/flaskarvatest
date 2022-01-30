from arvaghdraft import app, db
from flask import render_template, request, session, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from sqlalchemy import desc
# import datetime
from datetime import datetime, date
# Import or_ from sqlalchemy,to enable us to use alternative columns for the search
# enable db search on alternative columns
from sqlalchemy import or_
import requests
import os
import configparser
import json
from arvaghdraft.forms import EventForm
from arvaghdraft.models import User, Event
import csv, operator
import pandas as pd
# todo
# set up administrative functionality
# -- administrator to approve item before being viewed (seems to be working)
# -- authentication and authorisation (ongoing testing with anonymous and admin user)
# -- notification when item uploaded (not yet)
# -- email (not yet)
# -- event email should not be unique as several events can be associated with an email 
# -- check should approve redirect to eventslist rather than event also 
# -- check if more db cols can be added to search function 
# -- edit and delete (seems to be working)
# -- user request function (is  this Required?)
# -- prevent adjusting the text area size
# check there is no conflict with strftime conversion in event.html (with update function)


# render home page. Also calls visit counter and loads weather and events data
@app.route("/",  methods=['get', 'post'])
def index(): 
    # calculate site hits
    readdata = 0
    with open("arvaghdraft/static/visits.txt", "r") as readfile:
        for i in readfile:
            if i.isdigit() == True:
                readdata = int(i)
        # print(f"Read data is: {readdata}")
    totalvisits = str(readdata +1)
    with open("arvaghdraft/static/visits.txt", "w+") as file:
        file.write(totalvisits)
        # print(f"Written data is: {totalvisits}")
        sitevisits = int(totalvisits)
    # load weather info 
    with open("arvaghdraft/static/weatherData.json", "r") as datafile:
        weather_dict = json.load(datafile)
        icon = weather_dict["weather"][0]["icon"]  
    # summary list of events [return 5 events (by date desc)]
    events =  Event.query.order_by(Event.date.desc()).limit(5).all()
    total_events = Event.query.count()
    # use session to get sitevisits for transfer to about page
    session["sitevisits"] = sitevisits
    return render_template("public/index.html", sitevisits=sitevisits, weather_dict=weather_dict, icon=icon, events=events, total_events=total_events)  
    
    
# function to render the about page
@app.route("/about")
def about():
    # site_visits
    visit = session.get("sitevisits",None)
    return render_template("public/about.html", visit=visit)

# function to render the things to do page
@app.route("/things")
def things():
    # site_visits
    visit = session.get("sitevisits",None)
    return render_template("public/things_to_do.html", visit=visit)


# function to retrieve api_key
def get_api_key():
    api = os.environ.get('api')
    # config = configparser.ConfigParser()
    # config.read('config.ini')
    # return config['openweathermap']['api']
    return api
   

# function to call api
@app.route('/get-data', methods=['GET','POST'])
def get_weather_data():
    # reference the name on the form to access the city
    api_key = get_api_key()
    location = request.form['location']
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(location, api_key)
    # save response in a variable and return in json format
    r = requests.get(api_url).json()
    if r['cod'] != 200:
        return redirect(url_for('handle_errors'))
        # return redirect(url_for('index'))
    else:
        with open("arvaghdraft/static/weatherData.json", "w") as outfile:
            json.dump(r, outfile, indent="")
        return redirect(url_for('index'))


# create a new event
@app.route('/event/new',  methods=['GET', 'POST'])
def new_event():
    visit = session.get("sitevisits",None)
    form = EventForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data, name=form.name.data, date=form.date.data, venue=form.venue.data, eventtime=form.eventtime.data, message = form.message.data, email=form.email.data )
        db.session.add(event)
        db.session.commit()
        flash('Your event has been submitted!', 'success')
        return redirect(url_for('success'))
    return render_template("public/eventform.html", title='New Event', form=form, legend='New Event', visit=visit)

     
# list all events
@app.route('/eventlist', methods=['GET', 'POST'])
def eventlist():
    visit = session.get("sitevisits",None)
    events =Event.query.order_by(Event.date_posted.desc()).all()
    # set up countdown 
    # current = datetime.now()
    current = date.today()
   
    # for val in target:
    #     remaining = val - current
    #     if remaining <= current:
    #         result = "Event Completed"
    #     else:
    #         result = f"Days remaining:  {remaining}"
    #     print(f"The result is {result}")
    return render_template("public/eventlist.html", events=events, visit=visit, current=current)  


# success page on successful submission of event 
@app.route('/success')
def success():
    visit = session.get("sitevisits",None)
    return render_template('public/success.html', visit=visit)


# 404 code below not working so create custom
# handle pages not found 
@app.route('/errors')
def handle_errors():
    return render_template("public/404.html")


# search the database based on title and date      
@app.route('/search', methods=['GET', 'POST'])
def search():
    visit = session.get("sitevisits",None)
    query = request.form['searched']
    events = Event.query.filter(or_(Event.title.ilike(f'%{query}%'), Event.date.ilike(f'%{query}%'))).all()
    print(f"query is {query}")
    print(type(f"query type is{query}"))
    print(f"Events are {events}")
    print(type(f"events type is{events}"))
    if query == '' or events == []:
        return redirect(url_for('handle_errors'))
    return render_template('public/search.html', events=events, visit=visit)

        
# view an individual event
# use int: as we are specifically looking for an int value (number)
@app.route('/event/<int:event_id>',  methods=['GET', 'POST'])
def event(event_id):
    # use get as below so it returns 404 if not found
    event = Event.query.get_or_404(event_id)
    visit = session.get("sitevisits",None)
    return render_template('public/event.html', title=event.title, event=event, visit=visit)
# request an edit       

# approve an event
@app.route('/event/<int:event_id>/approve',  methods=['GET', 'POST'])
@login_required
def approve_event(event_id):
    # visit=session.get("sitevisits",None)
    event=Event.query.get(event_id)
    event.approved_event = True
    db.session.commit()
    print(f"Event approved is {event.approved_event}")
    flash("The event has been Approved!", 'success')
    return redirect(url_for('eventlist'))
  
# edit event
@app.route('/event/<int:event_id>/update',  methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if not current_user.is_authenticated:
        abort(403)
    form = EventForm()
    if form.validate_on_submit():
        event.name = form.name.data
        event.email = form.email.data
        event.title = form.title.data
        event.date = form.date.data
        event.venue = form.venue.data
        event.eventtime = form.eventtime.data
        event.message = form.message.data
        db.session.commit()
        flash("The event has been Updated!", 'success')
        return redirect(url_for('event', event_id = event.id))
    elif request.method == 'GET':
        form.name.data = event.name
        form.email.data = event.email
        form.title.data = event.title
        # event.date = datetime.strptime(form.date.data, "%Y-%m-%d").date()
        form.date.data= event.date
        form.venue.data = event.venue
        form.eventtime.data = event.eventtime
        form.message.data = event.message
    visit = session.get("sitevisits",None)
    return render_template("public/eventform.html", title='Update Event', form=form, legend='Update Event', visit=visit, event=event)
  
# delete event
@app.route('/event/<int:event_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if not current_user.is_authenticated:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('The event has been deleted!', 'success')
    return redirect(url_for('index'))

  # handle errors
@app.errorhandler(404)
def error_404(error):
    return render_template('public/404.html'), 404

@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

    
# pass stuff to layout template    
# @app.context_processor
# def layout():
#     form = SearchForm
#     return dict(form=form)
# custom filter
# @app.template_filter('strftime')
# def _jinja2_filter_datetime(date, fmt=None):
#     date = dateutil.parser.parse(date)
#     native = date.replace(tzinfo=None)
#     format='%Y-%m-%d'
#     return native.strftime(format)
# def datetime_format(value, format="%H:%M %d-%m-%y"):
#     return value.strftime(format)

# environment.filters["datetime_format"] = datetime_format
# error message on strftime str on str
# @app.template_filter('formatdatetime')
# def format_datetime(value, format="%Y-%m-%d"):
#     """Format a date time to  YYYY-m-d P"""
#     if value is None:
#         return ""
#     return value.strftime(format)