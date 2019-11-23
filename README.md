# Geocoding project for Ironhack

I was given a challenge: I needed to find a place for a startup to locate its offices.

I had to deal with multiple requirements:

- The CEO of the company is vegan.
- The company needs to be located near successfull startups (raised >1M$).
- No big old companies (more than 10 years old) around.
- Need of schools around, as 30% of the employees have children.
- They all LOVE Starbucks.
- There has to be an Airport around.

I dealt with a csv from Angel.io and a json database from Crunchbase, which I managed using pymongo. Information about restaurants, schools, and Starbucks was obtained from Google Places API. I decided to focus on the city of Montreal, and to use existing vegan restaurants locations as the potential home to the startup. We need to keep the CEO happy and well-fed...

Using GeoQueries, I created a ranking based on the mutiple criteria explained above. I produced a map with Folium representing the location who performed the best in my punctuation system. It is located in the Mile End, a nice neighborhood in Montreal where some of my friends live in :')

