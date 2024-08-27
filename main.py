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
class Restaurant:
    def __init__(self, name, address, price, rating, latitude, longitude, is_closed, distance, delivers):
        self.name = name
        self.address = address
        self.price = price
        self.rating = float(rating)
        self.latitude = latitude
        self.longitude = longitude
        self.is_closed = is_closed
        self.distance = distance
        self.delivers = delivers


    def __repr__(self):
        return f"{self.name} ({self.price}) - {self.rating} stars - {self.address} - {'Closed' if self.is_closed else 'Open'} - {self.distance} meters away"

    def __eq__(self, other):
        if isinstance(other, Restaurant):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)


api_url = 'https://api.yelp.com/v3/businesses/search'
api_key = '87qjzUYSUt1gI7_aZKUsEtOkafLQirJaXPiSdMVdNKJYS7f0HvaasYRJtx10VCjaPhAS4DxZVmC2VSUVjKfMUaZ9gw47usy_hOsQ15lJH4G5m24PfiRj-7ydD7K7ZnYx'
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


temp_list = {
    'mexican': {'weight': 3, 'related_terms': ['casita', 'la ', 'tacos', 'el ']},
    'tacos': {'weight': 2, 'related_terms': []},
    'latin': {'weight': 0, 'related_terms': []},
    'indian': {'weight': 0, 'related_terms': ['taj', 'palace', 'royal', 'mahal', 'mirchi', 'chaat', 'dosa', 'masala']},
    'vietnamese': {'weight': 0, 'related_terms': ['pho', 'viet', 'dan', 'saigon']},
    'chinese': {'weight': 0, 'related_terms': ['dan', 'din', 'chiang', 'xian', 'noodle', 'dumpling', 'hong kong', 'shangai']},
    'sandwich': {'weight': 1, 'related_terms': ['sub', 'deli']},
    'deli': {'weight': 0, 'related_terms': []},
    'soup': {'weight': 0, 'related_terms': []},
    'sushi': {'weight': 0, 'related_terms': ['kura', 'revolving', 'nori']},  
    'italian': {'weight': 0, 'related_terms': ['pizzeria', 'luigi', 'italiano', 'traditional']},
    'pizza': {'weight': 0, 'related_terms': ['stone', 'pagliacci', 'domino', 'papa', 'mod']},
    'burgers': {'weight': 0, 'related_terms': ['cow', 'fat', 'big', 'chick', 'chicken', 'hungry']},
    'thai': {'weight': 0, 'related_terms': ['khao', 'kai', '65', 'thai', 'bai tong', 'ginger', 'basil', 'bangkok', 'noodle']},
    'noodles': {'weight': 0, 'related_terms': []},
    'ramen': {'weight': 0, 'related_terms': ['izayaka', 'noodle']},
    'japanese': {'weight': 0, 'related_terms': ['izayaka', 'sushi', 'ramen']},
    'curry': {'weight': 0, 'related_terms': []},
    'pho': {'weight': 0, 'related_terms': ['pho']},
    'salad': {'weight': 1, 'related_terms': ['green', 'wild']},
    'sit down': {'weight': 0, 'related_terms': ['house', 'tavern']},
    'fast food': {'weight': 0, 'related_terms': []},
    'dim sum': {'weight': 0, 'related_terms': ['dim sum', 'dumpling', 'dumpling house']},
    'byo': {'weight': 0, 'related_terms': ['bowl', 'salad', 'chipotle', 'sandwich', 'sub', 'mod']},
    'fries': {'weight': 0, 'related_terms': []},
    'rice': {'weight': 0, 'related_terms': []},
    'asian': {'weight': 0, 'related_terms': ['teriyaki']},
    'korean': {'weight': 0, 'related_terms': ['bbq', 'barbeque', 'authentic']}
}

restaurant_options = {}

needDelivery = False
priceRange = ['$','$$']
maxPrice = priceRange[-1]

# !!!! I THINK THE WAY WE ARE DOING IT HERE IS NOT AS SPECIFIC TO CUISINE - need to really drastically change the value based on the cuisine here
#first population of the possible list(the broadest version, we will narrow down from here after this)
additionalPosSearchTerms = {}
additionalNegSearchTerms = {}

for key, value in temp_list.items():
    if (value['weight'] != 0):
        if (len(value['related_terms']) != 0):
            additionalPosSearchTerms[key] = value['related_terms']
        # now we search yelp
        params['term'] = key
        print(params) # testing
        # Make a request to the Yelp API
        response = requests.get(api_url, headers=HEADERS, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            for business in data.get('businesses', []):
                restaurant = Restaurant(
                    name=business['name'],
                    address=business['location']['address1'],
                    price=str(business.get('price', 'N/A')),
                    rating=business.get('rating', 0),
                    latitude=business['coordinates']['latitude'],
                    longitude=business['coordinates']['longitude'],
                    is_closed=business.get('is_closed', True),
                    distance=business.get('distance', 0),
                    delivers='delivery' in business.get('transactions', [])
                )
                if restaurant in restaurant_options:
                    # Add the value to the existing value
                    restaurant_options[restaurant] *= value['weight']
                else:
                    # Add the restaurant to the dictionary with the value
                    restaurant_options[restaurant] = value['weight']
        else:
            print(response.status_code)
    else:
        if (len(value['related_terms']) != 0):
            additionalNegSearchTerms[key] = value['related_terms']


print(restaurant_options) # idk what format this is going to print in
print('pos: ', additionalPosSearchTerms)
print('neg: ', additionalNegSearchTerms)


    



