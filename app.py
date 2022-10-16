from flask import Flask, request
import json 
import random
import requests
import os
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return '{"Hello": "World!"}'

@app.route('/webhook',methods=['POST'])
def index():
    #Get the geo-city entity from the dialogflow fullfilment request.
    body = request.json
    city= body['queryResult']['parameters']['city']

    # reply = '{"fulfillmentMessages": [ {"text": {"text": ["The  temperature in '+ city +", "+ country +' it is ' + temperature + '"] } } ]}'

    # To openweather and return a real forcast note you will need to 
    # create an account at openweathermap.com and put your APPID below.
    appId = '58caf6662c02d461e624c303aac7cf68'

    #Connect to the API anf get the JSON file.
    api_url='https://api.openweathermap.org/data/2.5/weather?q='+ city + '&units=metric&appid='+ appId
    headers = {'Content-Type': 'application/json'} #Set the HTTP header for the API request
    response = requests.get(api_url, headers=headers) #Connect to openweather and read the JSON response.
    r=response.json() #Conver the JSON string to a dict for easier parsing.

    #Extract weather data we want from the dict and conver to strings to make it easy to generate the dialogflow reply.
    weather = str(r["weather"][0]["description"])
    temp = str(int(r['main']['temp']))
    humidity = str(r["main"]["humidity"])
    pressure = str(r["main"]["pressure"])  
    windSpeed = str(r["wind"]["speed"])
    windDirection = str(r["wind"]["deg"])
    country=str(r["sys"]["country"])
    #build the Dialogflow reply.
    reply = '{"fulfillmentMessages": [ {"text": {"text": ["Currently in '+ city + ', '+ country + ' it is ' + temp + ' degrees and ' + weather + '"] } } ]}'
    return reply

test_mode = 0
port = int(os.environ.get("PORT",5000))

if __name__ == "main":
    if test_mode == 1:
        app.run(debug=False,host='0.0.0.0',port=port)
    else:
        app.run(debug=True,use_reloader=True,host='0.0.0.0',port=port)