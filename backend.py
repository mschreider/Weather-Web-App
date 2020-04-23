import urllib.request, urllib.parse
from flask import Flask, render_template, request
import json, pandas
import sys, datetime

def get_IP():
    # url = "http://checkip.dyndns.org"
    # data = urllib.request.urlopen(url).read().decode('utf-8')   # .decode(utf-8) converts from 'bytes' to 'str'
    ip_address = str(request.remote_addr)
    # ip_address = data[76:90]    # Parse 76th to 90th index of str
    return ip_address

def get_information(ip_address):
    key = "key=d3dc97f5adf0499894b215338200504"
    url = "http://api.worldweatheronline.com/premium/v1/weather.ashx?" + key + "&q="+ ip_address + "&format=json&num_of_days=4&includelocation=yes"
    data = urllib.request.urlopen(url).read()   
    json_data = json.loads(data)    #converts to json file
    # with open("weather_data.json", 'x') as file:
    #     json.dump(json_data, file)
    return json_data

def get_location(json_data):
    location_json = json_data['data']['nearest_area'][0]
    location = "%s, %s" % (location_json['areaName'][0]['value'], location_json['region'][0]['value'])
    return location

def get_date(json_data):
    date = json_data['data']['weather'][0]['date']
    return date

def get_dayOfWeek(date):
    # Convert from YYYY-MM-DD to day of the week
    l = list(map(int, date.split('-')))
    x = datetime.datetime(l[0], l[1], l[2])
    day_of_week = x.strftime("%a")
    return day_of_week

def get_longDate(date):
    l = list(map(int, date.split('-')))
    x = datetime.datetime(l[0], l[1], l[2]) # (YEAR, MONTH, DATE)
    day_of_week = x.strftime("%A")
    month = x.strftime("%B")
    day = x.strftime("%d")
    year = x.strftime("%Y")
    long_date = "%s, %s %s, %s" % (day_of_week, month, day, year)
    return long_date


def get_currentweather(json_data):
    current_weather = json_data['data']['current_condition'][0]
    return current_weather

def get_currentconditions(current_weather):
    current_conditions = current_weather['weatherDesc'][0]['value']
    return current_conditions

def get_weathericon(current_conditions):
    df = pandas.read_csv("wwoConditionCodes.csv", sep=';')
    for x,y in zip(df.Condition, df.CSS_Icon):
        if x.lower() == current_conditions.lower():
            weather_icon = y
            return weather_icon

def get_currenttemp(current_weather):
    current_temp = current_weather['temp_F']
    return current_temp

def get_futureweather(json_data, dayIndex):
    future_weather = json_data['data']['weather'][dayIndex]
    future_weekday = get_dayOfWeek(future_weather['date'])
    future_conditions = future_weather['hourly'][4]['weatherDesc'][0]['value']
    future_high = future_weather['maxtempF']
    future_low = future_weather['mintempF']
    return future_weekday, future_conditions, future_high, future_low

def run():

    ip_address = get_IP()  # uncomment when ready to deploy
    json_data = get_information(ip_address)    # uncomment when ready to deploy
    #with open('data.json') as f:    #remove when ready to deploy
    #    json_data = json.load(f)    #remove when ready to deploy

    location = get_location(json_data)
    date = get_date(json_data)
    long_date = get_longDate(date)
    day_of_week_abv = get_dayOfWeek(date)

    current_weather = get_currentweather(json_data)
    current_conditions = get_currentconditions(current_weather)
    current_temp = get_currenttemp(current_weather)
    current_weathericon = get_weathericon(current_conditions)
    
    # FUTURE DATA
    future = []
    for dayIndex in range(1, 4):
        data={}
        future_dayofweek, future_conditions, future_high, future_low = get_futureweather(json_data, dayIndex)
        future_weathericon = get_weathericon(future_conditions)
        data["dayofweek"] = future_dayofweek
        data["weathericon"] = future_weathericon
        data["conditions"] = future_conditions
        data["high"] = future_high
        data["low"] = future_low
        future.append(data)

    return future, location, long_date, current_weathericon, current_temp, current_conditions