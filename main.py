import os
import requests
import csv
import json
from geopy.distance import geodesic
import pandas as pd

categorygoogle =  'address_component , adr_address , business_status , formatted_address , geometry , icon , icon_mask_base_uri , icon_background_color , name , permanently_closed ( deprecated ), photo , place_id , plus_code , type , url , utc_offset , vicinity , wheelchair_accessible_entrance, current_opening_hours , formatted_phone_number , international_phone_number , opening_hours , secondary_opening_hours , website, curbside_pickup , delivery , dine_in , editorial_summary , price_level , rating , reservable , reviews , serves_beer , serves_breakfast , serves_brunch , serves_dinner , serves_lunch , serves_vegetarian_food , serves_wine , takeout , user_ratings_total'
categorylist = categorygoogle.split(',')

line_length = 0
side_of_the_world = 1
work_line_length = 300


radius = float(input("pleas, input the radius   --   ") or "2000")
apikey = input("pleas, input the apikey   --   ") or "AIzaSyDiwTZu7jaaVRUQVzTx6iQeNpVn74HJh98"
step_in_one_side = int(input("pleas, input the step in one side   --   ") or "300")
latitude = input("pleas, input the latitude   --   ") or "5.3818939"
longitude = input("pleas, input the longitude   --   ") or "-3.9471632"
locationtype = input("pleas, input the location type --  ") or "restaurant"
plusstep = 0
radiusname = int(radius)
radius = pow((pow(radius, 2)+pow(radius, 2)), 0.5)



location = str(latitude)+"%2C"+str(longitude)
worklongitude = float(longitude)
worklatitude = float(latitude)
worklocation = str(worklatitude)+","+str(worklongitude)

url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + location +"&radius=" + str(step_in_one_side) + "&&type=" + str(locationtype) + "&key=AIzaSyDiwTZu7jaaVRUQVzTx6iQeNpVn74HJh98"
payload = {}
headers = {}

def data(workurl):
        response = requests.request("GET", workurl, headers=headers, data=payload)
        with open("data_file.json", "w",encoding='utf-8') as write_file:
             json.dump(response.text, write_file)
        with open('names.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

        testdic = json.loads (response.text)
        for item in testdic['results']:
            print(item['name'])

            with open('names.csv', 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


                link = 'https://www.google.com/maps/search/?api=1&query=Google&query_place_id='+item['place_id']
                writer.writerow({'name':  str(item['name']),
                                 'vicinity': str(item['vicinity']),
                                 'location': str(item['geometry']['location']),
                                 'viewport': str(item['geometry']['viewport']),
                                 'types': str(item['types']),
                                 'place_id': str(item['place_id']),
                                 'link': str(link),
                                 "business_status": str(item.get('business_status')),
                                 "geometry" : str(item.get('geometry')),
                                "plus_code": str(item.get('plus_code')),
                                "rating": str(item.get('rating')),

                                "user_ratings_total": str(item.get('user_ratings_total')),

                }

                                )
if __name__ == "__main__":

        with open('names.csv', 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['name', 'rating',  'user_ratings_total', 'types', 'link',  'location', 'place_id', 'geometry',  'icon', 'plus_code', 'viewport','vicinity',  'business_status']
        while (float(geodesic((str(latitude)+","+str(longitude)),(worklocation)).m)<float(radius)):
            if side_of_the_world == 1:
                while (work_line_length < line_length + step_in_one_side):
                    workurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(worklatitude) + "%2C" + str(worklongitude) + "&radius=" + str(step_in_one_side+plusstep) + "&&type=" + str(locationtype) + "&key=AIzaSyDiwTZu7jaaVRUQVzTx6iQeNpVn74HJh98"
                    worklatitude += (step_in_one_side / 111000)
                    side_of_the_world = 2
                    work_line_length+=step_in_one_side
                    data(workurl)


            if side_of_the_world == 2:
                while (work_line_length < line_length):
                    workurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(worklatitude) + "%2C" + str(worklongitude) +"&radius=" + str(step_in_one_side+plusstep)+ "&&type=" + str(locationtype)+ "&key=AIzaSyDiwTZu7jaaVRUQVzTx6iQeNpVn74HJh98"
                    worklongitude += (step_in_one_side / 111000)
                    side_of_the_world = 3
                    work_line_length += step_in_one_side
                    worklocationstr = str(worklatitude) + "%2C" + str(worklongitude)
                    data(workurl)

            if side_of_the_world == 3:
                while (work_line_length < line_length + step_in_one_side):
                    workurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(worklatitude) + "%2C" + str(worklongitude) +"&radius=" + str(step_in_one_side+plusstep) + "&&type=" + str(locationtype)+ "&key=AIzaSyDiwTZu7jaaVRUQVzTx6iQeNpVn74HJh98"
                    worklatitude -= (step_in_one_side / 111000)
                    work_line_length += step_in_one_side
                    side_of_the_world = 4
                    data(workurl)

            if side_of_the_world == 4:
                while (work_line_length < line_length):
                    workurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(worklatitude) + "%2C" + str(worklongitude) +"&radius=" + str(step_in_one_side+plusstep) + "&&type=" + str(locationtype)+ "&key=AIzaSyDiwTZu7jaaVRUQVzTx6iQeNpVn74HJh98"
                    worklongitude -= (step_in_one_side / 111000)
                    work_line_length += step_in_one_side
                    side_of_the_world = 1
                    data(workurl)

            line_length = work_line_length
            work_line_length = 0
            worklocation = str(worklatitude) + "," + str(worklongitude)



        df = pd.read_csv(r'names.csv', header=None,
                         names=['name', 'rating',  'user_ratings_total', 'types', 'link',  'location', 'place_id', 'geometry',  'icon', 'plus_code', 'viewport','vicinity',  'business_status']
                        , engine='python', encoding='utf-8')
        df.drop_duplicates(subset=['name']).to_csv(r'radius'+str(radiusname)+'meters.csv', header=None, index=False)
