from flask import Flask, render_template, request, jsonify, url_for, redirect
import requests
import json
import subprocess
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import logging
from flask_debugtoolbar import DebugToolbarExtension
import sys


app = Flask(__name__)

toolbar = DebugToolbarExtension(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Names(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    secondname = db.Column(db.String(100), nullable=False)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, primary_key=False)
    foot = db.Column(db.String(100), nullable=False)
    nation = db.Column(db.String(100), nullable=False)
    currClub = db.Column(db.String(100), nullable=False)
    playerPic = db.Column(db.String(100), nullable=False)
    nationFlag = db.Column(db.String(100), nullable=False)
    clubBadge = db.Column(db.String(100), nullable=False)
    goals = db.Column(db.Integer, primary_key=False)
    assists = db.Column(db.Integer, primary_key=False)
    xG = db.Column(db.Float, nullable=False)
    xA = db.Column(db.Float, nullable=False)
    g_a = db.Column(db.Integer, primary_key=False)
    goalsPer90 = db.Column(db.Float, nullable=False)
    assistsPer90 = db.Column(db.Float, nullable=False)
    matchesPlayed = db.Column(db.Integer, primary_key=False)
    minutesPlayed = db.Column(db.Integer, primary_key=False)
    yellowCards = db.Column(db.Integer, primary_key=False)
    redCards = db.Column(db.Integer, primary_key=False)
    trophiesWon = db.Column(db.Integer, primary_key=False)
    shotsOnTarget = db.Column(db.Integer, primary_key=False)
    penalties = db.Column(db.Integer, primary_key=False)
    takeOns = db.Column(db.Integer, primary_key=False)
    takeOnPerc = db.Column(db.Float, nullable=False)
    dribbles = db.Column(db.Integer, primary_key=False)
    finalThirdTouches = db.Column(db.Integer, primary_key=False)
    keyPasses = db.Column(db.Integer, primary_key=False)
    progPasses = db.Column(db.Integer, primary_key=False)
    crosses = db.Column(db.Integer, primary_key=False)
    fouls = db.Column(db.Integer, primary_key=False)
    tackles = db.Column(db.Integer, primary_key=False)
    blocks = db.Column(db.Integer, primary_key=False)
    interceptions = db.Column(db.Integer, primary_key=False)
    clearances = db.Column(db.Integer, primary_key=False)
    totalPasses = db.Column(db.Integer, primary_key=False)
    passAccuracy = db.Column(db.Float, nullable=False)
    aerialDuelPerc = db.Column(db.Float, nullable=False)
    saves = db.Column(db.Integer, primary_key=False)
    savePerc = db.Column(db.Float, nullable=False)
    cleanSheets = db.Column(db.Integer, primary_key=False)
    cleanSheetPerc = db.Column(db.Float, nullable=False)
    goalsAgainst = db.Column(db.Integer, primary_key=False)
    xgAgainst = db.Column(db.Float, nullable=False)
    penFaced = db.Column(db.Integer, primary_key=False)
    penSaved = db.Column(db.Integer, primary_key=False)
    totalPasses = db.Column(db.Integer, primary_key=False)
    passAccuracy = db.Column(db.Float, nullable=False)
    longBallCompPerc = db.Column(db.Float, nullable=False)
    recoveries = db.Column(db.Integer, primary_key=False)

    

players = []
playerLeft = None
playerRight = None

@app.route('/search', methods=['POST'])
def search_players():
    db.session.query(Names).delete()
    db.session.commit()
    data = request.get_json()
    searchTerms = data['searchTerms']
    playerLeft = searchTerms[0]
    playerRight = searchTerms[1]
    newNames = Names(firstname=playerLeft, secondname=playerRight)
    db.session.add(newNames)
    db.session.commit()
    return jsonify({"message": "Search successful"})

@app.route('/search', methods=['GET'])
def searchget_players():
     return render_template('first.html')

@app.route('/players', methods=['POST'])
def add_players():
    data = request.get_json()
    realdata = json.loads(data)
    playerA = realdata[0]
    playerB = realdata[1]
    app.logger.info(f"data: {data}")
    app.logger.info(f"playerA: {playerA}")
    app.logger.info(f"playerB: {playerB}")
    players.append(playerA)
    players.append(playerB)
    return jsonify({"message": "Players added successfully"})

@app.route('/players', methods=['GET'])
def get_players():
    playerA = players[0]
    playerB = players[1]
    return render_template('website.html', playerA=playerA, playerB=playerB)

if __name__ == '__main__':
    app.run(debug=True)

