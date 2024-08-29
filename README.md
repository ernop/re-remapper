Zillow's UI is so awful. You can't:
* see the fields you care about
* track things (like... new properties) coming in over time

This tool re-remapper at least does the first one. Here's how to use it:

1. open zillow
2. hit f12
3. find the network tab
4. find the items labelled "PUT" and click
5. on the right there's request, response mini tabs
6. response has an option "show raw"
7. click that
8. save the full thing into a folder like "city-data"
9. it might be big like 100k chars
10. do that af ew times - those are the points well show you later on
11. (we don't auto-query - you get all data manually yourself through legit means, this just makes a new UI to view them in a sane way)
12. run the python program to aggregate them all (you have to edit the src a bit to have it find the folder)
13. now edit map2.html to reference the file
14. (this is annoying, but so is "security") run python -m simple.httpserver 8008 from the project folder
15. visit http://localhost:8008/map2.html
16. now you can see a sane UI

Later one most of these steps will be removabale but for now it's just a proof of concept.

![image](https://github.com/user-attachments/assets/b3048694-a843-46a3-83f4-ab0250c962f0)

(I put this into the cursor hint)

This is your guide information for the project of making a zillow custom persomal map system.

rules:
never show "$" in price always show like 310k or 1.4m. with lowercase M.

always use green good => red (bad) gradients with banded colors, not continuous gradients. 
The colors don't need to be max intensity, but clear that light pure green is good, pure red is bad (i.e. high price)

remember to always handle data very generically. for a filter set of data, it must have a list of ranges with a description for each one. for example size would be small, min_value=1, max_value=3, etc. You must never mix data into html as part of the source, or into js. 
store data in dictionaries or lists and create filters at runtime, when the user clicks etc.

wheneever a user changes a filter value, the legend items beneath must adjust to display the meaning
of the values displayed.

let's create a class for a colorfilter. each one should have: a name, a mapping function which
 takes a POI and returns an evaluation. the evaluation is: should display at all, color.  
 Then, each colorfilter is an instance of this class. priceColor filter is a color filter 
 which splits up points by price, and tells you which color it is.  
 Each filter instance also has to reveal its classification system also so that we can 
 toggle each group off. For example for price, we can toggle showing houses which cost 
 250k to 500k off and on.

The user must be able to easily drag to toggle off and on whole sections of the filter in the most natural
and good clear way.

The format of the popups must be this, with no labels, just data.
* first line lists price then size in acres
second line: 3b - 2ba (bedrooms and bathrooms count), then sqf of house
3rd line: city, then zip
4th line: sold date

the popup is a table with rows, each row has two TDs in it.

The popups MUST appear immediately when moused over with no close box. Then they disappear as soon as mouse out.

exmple points
    {
      "zpid": 59734602,
      "latitude": 40.239094,
      "longitude": -75.889946,
      "price": 430000.0,
      "address": "8 Willow St, Birdsboro, PA 19508",
      "city": "Birdsboro",
      "state": "PA",
      "zipcode": "19508",
      "bedrooms": 3.0,
      "bathrooms": 3.0,
      "living_area": 2100.0,
      "lot_area_value": 1.52,
      "lot_area_unit": "acres",
      "sale_date": 1723791600000,
      "zestimate": 430400.0,
      "rent_zestimate": 2555.0,
      "home_type": "SINGLE_FAMILY"
    },
    {
      "zpid": 82200966,
      "latitude": 40.27842,
      "longitude": -75.84031,
      "price": 700000.0,
      "address": "211 Dennis Dr, Reading, PA 19606",
      "city": "Reading",
      "state": "PA",
      "zipcode": "19606",
      "bedrooms": 3.0,
      "bathrooms": 2.0,
      "living_area": 2378.0,
      "lot_area_value": 20.15,
      "lot_area_unit": "acres",
      "sale_date": 1723618800000,
      "zestimate": 679400.0,
      "rent_zestimate": 2321.0,
      "home_type": "SINGLE_FAMILY"
    },
area
