#!/usr/bin/env python
from flask import Flask, render_template, jsonify, redirect, request
from models import *
from manage import *
from forms import *

# Create an app and configure it

def get_ppp(from_country,to_country):  
    country_from_ppp = 1
    country_to_ppp = 1
    country_from = Country.query.filter_by(name=from_country)
    #country_from = db.session.query(Country).filter_by(name=from_country)
    
    for from_data in country_from:
        country_from_ppp = float(from_data.ppp)
        country_from_currency = from_data.currency
        
    country_to = Country.query.filter(Country.name==to_country)
    for to_data in country_to:
        country_to_ppp = float(to_data.ppp)
        country_to_currency = to_data.currency
        
    return  country_from_ppp,country_to_ppp,country_from_currency,country_to_currency
    

@app.route('/',methods=['POST','GET'])
def display_result():
    converted_amount = None
    country_from_ppp = None
    country_to_ppp = None
    tocountry = None
    country_to_currency = None
    country_from_currency = None
    form = CountryForm()
    if  request.method == "POST" and form.validate_on_submit():
        fromcountry = form.country_from.data
        tocountry = form.country_to.data
        print(fromcountry,tocountry)
        salary = form.salary.data
        country_from_ppp,country_to_ppp,country_from_currency,country_to_currency = get_ppp(fromcountry,tocountry)
        converted_amount = round((float(salary) /country_from_ppp)*country_to_ppp,2)
        
    d = {
    'form':form,
    'amount':converted_amount,
    'tocountry': tocountry,
    'country_to_currency':country_to_currency,
    'country_from_currency':country_from_currency
    }
    print(converted_amount)
    return render_template('main.html',**d)
    
@app.route('/json')
def jsondata():
    country_data = Country.query.all()         
    countrylist = []
    for country in country_data:
        countrylist.append({'id': country.id,
                'name': country.name,
                'ppp': str(country.ppp),
                'code3': country.code3
                #'currency': country.currency
                })  
    return jsonify({'countries': countrylist})

   
