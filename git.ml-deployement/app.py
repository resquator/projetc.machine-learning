
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
import flask
import pickle
import sklearn
# Import the os module
import os
import numpy as np


app = Flask(__name__)

#@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if flask.request.method == 'GET':
        # Get the current working directory
        cwd = os.getcwd()
        print(f'CURRENT FOLDER {cwd}')
        # Use pickle to load in the pre-trained model.
        return(flask.render_template('predictorform.html'))

    if flask.request.method == 'POST':
        print('Loading model ....')
        cwd = os.getcwd()
        print(f'CURRENT FOLDER {cwd}')
        with open('finalized_odds.sav', 'rb') as f:
            model = pickle.load(f)
        print('MODEL LOADED successfully')
        hometeam = flask.request.form['hometeam']
        awayteam = flask.request.form['awayteam']

        odd_1  = np.float64(flask.request.form['1'])
        odd_N = np.float64(flask.request.form['N'])
        odd_2 = np.float(flask.request.form['2'])
        
        month = flask.request.form['month']

        v = [hometeam, awayteam, month, odd_1, odd_N, odd_2]
        result=model.predict_proba([v])

        html = '<html><body><h1>Pronostic for your request</h1><br><h3>V1.0f</h3>'
        html = html + f'<p>You request a pronostic validation for {hometeam} Vs. {awayteam}</p>'
        html = html + f'Odds given was {odd_1} {hometeam} to win, {odd_N} deuce, {odd_2} {awayteam} to win<br><hr>'
        html = html + f'(1) is {np.round(result[0][0],2)*100}%<br>'
        html = html + f'(N) is {np.round(result[0][1],2)*100}%<br>'
        html = html + f'(2) is {np.round(result[0][2],2)*100}%<br>'
        
        html = html + f'the game is going to played on  {month}%<br><hr>'

        result = model.predict([v])
        html = html + '<hr><h3>'
        if result[0] == 0:
            html = html + f'Pronostic is <b>{hometeam}</b> to <b>win</b>'
        if result[0] == 1:
            html = html + f'Pronostic is <b>{hometeam} Vs. {awayteam}</b> will <b>share</b>'
        if result[0] == 2:
            html = html + f'Pronostic is <b>{awayteam}</b> to <b>win</b>'
        html = html + '</h3>'


        return f'Hello from Resquator Predictions!<br>{html}'

    #return(flask.render_template('predictorform.html'))


