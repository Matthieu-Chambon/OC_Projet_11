print(">> Flask app loaded")

import json
import time
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions
     
     
def total_places_booked(competition, club):
    """
    Returns the total number of places booked by a club for a specific competition.
    If no bookings exist, returns 0.
    """
    if "bookings" not in competition:
        competition["bookings"] = []
    
    bookings = competition["bookings"]
    for b in bookings:
        if b["club"] == club["name"]:
            return b["places"]
    return 0


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club,competitions=competitions)
    except IndexError:
        flash("Adresse email inconnue, veuillez réessayer.")
        return redirect(url_for('index'))

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    
    if foundClub and foundCompetition:        
        return render_template(
            'booking.html',
            club=foundClub,
            competition=foundCompetition,
            total_places_booked=total_places_booked(foundCompetition, foundClub)
        )

    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    
    placesRequired = int(request.form['places'])
    placesBooked = total_places_booked(competition, club)
    
    current_datetime = datetime.now()
    competition_datetime = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    
    if competition_datetime < current_datetime:
        flash("Impossible to book places for a past competition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    elif placesRequired <= 0 :
        flash('You must book at least one place.')
        return render_template('booking.html', club=club, competition=competition, total_places_booked=placesBooked)
    
    elif placesRequired > int(club['points']):
        flash('You do not have enough points to book this competition.')
        return render_template('booking.html', club=club, competition=competition, total_places_booked=placesBooked)

    elif placesBooked + placesRequired > 12:
        flash('You cannot book more than 12 places for a single competition.')
        return render_template('booking.html', club=club, competition=competition, total_places_booked=placesBooked)

    elif placesRequired > int(competition['numberOfPlaces']):
        flash('There are not enough places available for this competition.')
        return render_template('booking.html', club=club, competition=competition, total_places_booked=placesBooked)
    
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        clubs[clubs.index(club)]['points'] = str(int(club['points'])-placesRequired)

        for booking in competition.get('bookings', []):
            if booking['club'] == club['name']:
                booking['places'] += placesRequired
                break
        else:
            competition['bookings'].append({
                "club": club['name'],
                "places": placesRequired
            })
        
        with open('clubs.json', 'w') as f:
            json.dump({'clubs': clubs}, f, indent=4)
        
        with open('competitions.json', 'w') as f:
            json.dump({'competitions': competitions}, f, indent=4)
                
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/pointsDisplay',methods=['GET'])
def pointsDisplay():
    return render_template('points_display.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))