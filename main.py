import requests 


# ################################################
# api_key2 = 'd1e6067d83cdf4'
# # Get the user's public IP address
# ip_response = requests.get('https://api.ipify.org?format=json')
# user_ip = ip_response.json()['ip']
# print('my ip: ' + user_ip)

# # Make the API request to get geolocation
# geo_response = requests.get(f'http://ipinfo.io/{user_ip}/json?token={api_key2}')

# # Check if the request was successful
# if geo_response.status_code == 200:
#     data = geo_response.json()
#     loc = data.get('loc', '').split(',')
#     if len(loc) == 2:
#         latitude = loc[0]
#         longitude = loc[1]
#         print(f"Latitude: {latitude}")
#         print(f"Longitude: {longitude}")
#     else:
#         print("Location data not available")
# else:
#     print("Error: Could not retrieve data")


###############################################
api_url = 'https://api.yelp.com/v3/businesses/search'
api_key = 'TEDWqCrmKb_w37qkJjS426xfoUGpBF1EQBdjxcJtKeXHgJEvAmCW4zFKrHFDvuUGN_ELrNQgEOzaK9taFY-DwvpjiPx1d7xtM5cZ3vnXA2gfEeCgAsAa32_cZY1rZnYx'

HEADERS = {'Authorization': f'Bearer {api_key}'}


latitude = 47.656610017739375 
longitude = -122.31540319155656 


params = {
	'term': 'tacos',
	'latitude': latitude,
    'longitude': longitude,
    'radius': 800,  # Radius in meters (5 miles)
    'limit': 20  # Number of results to return (maximum is 50)
}
    
# Make a request to the Yelp API
response = requests.get(api_url, headers=HEADERS, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    for business in data.get('businesses', []):
    	if business.get('price') == "$": 
    		print(business['name'], business['location']['address1'])
    	if business.get('price') == "$$": 
    		print(business['name'], business['location']['address1'])
    	
    	
        
else:
    print(f'Error: {response.status_code}')


#### first attempt at algorithm: 
#### factors we are taking BEFORE we make the request: cuisine preference, vegan / vegetarian, healthy, distance 
#### factors we are sorting AFTER we get the data: price range, deliverable?, rating, distance FROM current location (need to do this via comparing the two lat/long pairs) 

# need to make sure this list is sorted by value in descending order 
temp_list = {
    'mexican': 4,
    'tacos': 3,
    'latin': 2,
    'indian': 1,
    'vietnamese': 0,
    'chinese': 0, 
    'sandwich': 0, 
    'deli': 0, 
    'soup': 0, 
    'sushi': 0,  
    'italian': 0, 
    'pizza': 0, 
    'burgers': 0, 
    'thai': 0, 
    'noodles': 0,
    'ramen': 0,
    'japanese': 0,
    'curry': 0,
    'pho': 0,
    'salad': 0,
    'sit down': 0,
    'fast food': 0, 
    'dim sum': 0,
    'byo': 0, #translate to many separate yelp lookups: byo bowl, salad, chipotle, sandwich, sub, mod
    'fries': 0,
    'rice': 0
} 

restaurant_options = {}
secondary_options = {}

needDelivery = False 
priceRange = ['$','$$']
maxPrice = priceRange[-1]

#first population of the possible list(the broadest version, we will narrow down from here after this)
for key, value in temp_list.items():
    if (value != 0):
        # now we search yelp
        params['term'] = key
        print(params) # testing 
        # Make a request to the Yelp API
        response = requests.get(api_url, headers=HEADERS, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            for business in data.get('businesses', []):
                if business['name'] in restaurant_options:
                    # Add the value to the existing value
                    restaurant_options[business['name']] += value
                else:
                    # Add the restaurant to the dictionary with the value
                    restaurant_options[business['name']] = value
        else:
            print(response.status_code)

print(restaurant_options)

# next: go through restaurant_options and change the score for each restaurant depending on the other factors: 
    # Factors: price range, distance (need a separate function to calculate this), ratings/stars 

final_restaurant_list = {}

for key, value in restaurant_options.items():
    params['term'] = key
    response = requests.get(api_url, headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        for business in data.get('businesses', []):
            if business['price'] in priceRange:
                if business['rating'] >= 3.5: 
                    final_restaurant_list[key] = value
                else:
                    if business['rating'] >= 3:
                        secondary_options[key] = value -1
            else:
                if maxPrice+'$' == business['price']:  # this is how i'm trying to say it's ONE more $ sign, idk if it's right 
                    secondary_options[key] = value

print(final_restaurant_list)
print(secondary_options)


    



