import argparse
import csv
import codecs
import json
from flask_script import Manager,Server
from models import *
from website import *


manager = Manager(app)

@manager.command
def db_init():
    db.create_all()    
    
@manager.command
def clear_db():
    db.session.query(Country).delete()
    db.session.commit()
    
@manager.command
def display_db():
    data = Country.query.all()
    for d in data:
        print(d.code3,d.currency)
    
    
def extract_values(data):
        list_of_years = ['2016']

        for year in list_of_years:            
            if data.get(year):
                    #print("SHRUTI GOEL",data.get(year))
                    return year, data.get(year)
                    
        return None, None
        
        
@manager.option('-f', '--file_name', required=True, help='Path to the CSV file')        
def parsecsv(file_name = None):
    '''Parse a CSV file from the World Bank'''     
    new_csv = []
    # The CSV file from world bank as a UTF-8 BOM necessating the following
    # code.
    with codecs.open(file_name, 'r', 'utf-8-sig') as csvfile:
        data_dict = csv.DictReader(csvfile)
        
        for row in data_dict:
            new_row = {}
            #print("PRINTING ROW" ,row)
            year, value = extract_values(row)
            if year is None or value is None:
                continue
            new_row = {'year': year, 'value': value, 'country':
                       row['Country Name'], 'code': row['Country Code']}
            new_csv.append(new_row)
    with open('parsed_data.csv', 'w', newline='') as csvfile:
        dict_writer = csv.DictWriter(csvfile, ['country', 'code', 'year',
                                     'value'])
        dict_writer.writerows(new_csv)
    print("Parsed CSV successfully")


@manager.option('--file_name', required=True, help='Path to the CSV file')
def importcsv(file_name):
    '''Import a CSV into the database'''
    with open(file_name) as f:
        ppp_data = csv.reader(f)
        for line in ppp_data:
            print(line)
            new_country = Country(name=line[0], code3=line[1],
                              year=line[2], ppp=line[3])
            db.session.add(new_country)
            db.session.commit()
    
            
    print("Imported CSV successfully")
    
@manager.option('--file_name', required=True, help='Path to the CSV file')
def addcurrencyname(file_name):
    '''Import a currency name into the database'''
    
    with open(file_name) as f:
        i = 1
        currency_data = csv.reader(f)
        for line in currency_data:
            country_instance = Country.query.filter_by(code3=line[3]).first()
            if country_instance:
                country_instance.currency = line[14]
                db.session.add(country_instance)
                db.session.commit()           
            print(line[1],line[14],"i",i,country_instance)            
            i= i+1    
     

if __name__ == '__main__':   
    manager.run()
